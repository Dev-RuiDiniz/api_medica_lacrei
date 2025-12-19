from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .test_setup import TestSetUp
from users.models import Profissional, Consulta

class TestConsultaViews(TestSetUp):
    def setUp(self):
        super().setUp()
        # Criamos o profissional que será o 'Pai' da consulta
        self.profissional = Profissional.objects.create(**self.profissional_data)
        self.consulta_url = reverse('consulta-list')
        
        self.data_valida = timezone.now() + timedelta(days=2)
        self.payload = {
            "profissional": self.profissional.id,
            "paciente_nome": "João Silva",
            "data_hora": self.data_valida,
            "status": "AGENDADA"
        }

    def test_can_create_consulta_vincular_profissional(self):
        """Sucesso: Garante que a consulta é vinculada corretamente ao ID do profissional"""
        res = self.client.post(self.consulta_url, self.payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['profissional'], self.profissional.id)

    def test_cannot_create_consulta_with_invalid_profissional(self):
        """Integridade: Impede vincular consulta a um profissional que não existe (ID inexistente)"""
        self.payload['profissional'] = 9999 # ID que não existe no banco de testes
        res = self.client.post(self.consulta_url, self.payload)
        
        self.assertEqual(res.status_code, 400)
        self.assertIn('profissional', res.data)

    def test_can_list_consultas(self):
        """Sucesso: Listagem de consultas"""
        Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome="Maria Teste",
            data_hora=self.data_valida
        )
        res = self.client.get(self.consulta_url)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data['results']), 1)

    def test_delete_profissional_cascade_behavior(self):
        """Integridade/Regra: O que acontece com a consulta se o profissional for deletado?"""
        # Cria a consulta
        consulta = Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome="Paciente Excluido",
            data_hora=self.data_valida
        )
        # Deleta o profissional
        self.profissional.delete()
        
        # Verifica se a consulta ainda existe ou foi removida (dependendo do seu on_delete no Model)
        # Se você usou models.CASCADE, a consulta deve sumir:
        exists = Consulta.objects.filter(id=consulta.id).exists()
        self.assertFalse(exists, "A consulta deveria ter sido deletada em cascata.")

    def test_update_consulta_status(self):
        """Sucesso: Alterar status da consulta (ex: de AGENDADA para REALIZADA)"""
        consulta = Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome="Status Teste",
            data_hora=self.data_valida
        )
        url = reverse('consulta-detail', kwargs={'pk': consulta.id})
        res = self.client.patch(url, {"status": "REALIZADA"})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], "REALIZADA")