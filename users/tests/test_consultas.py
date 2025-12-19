from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .test_setup import TestSetUp
from users.models import Profissional, Consulta


class TestConsultaViews(TestSetUp):
    def setUp(self):
        """
        Configuração inicial para cada teste de consulta.
        Cria um profissional para vincular às consultas e prepara o payload.
        """
        super().setUp()

        # Criamos o profissional que será o 'Pai' (FK) das consultas nos testes
        self.profissional = Profissional.objects.create(
            **self.profissional_data
        )
        self.consulta_url = reverse('consulta-list')

        # Definimos uma data futura válida (2 dias à frente)
        self.data_valida = timezone.now() + timedelta(days=2)

        # Payload padrão para criação de consultas via POST
        self.payload = {
            'profissional': self.profissional.id,
            'paciente_nome': 'João Silva',
            'data_hora': self.data_valida.isoformat(),
            'status': 'AGENDADO',
        }

    def test_can_create_consulta_vincular_profissional(self):
        """Sucesso: Garante que a consulta é vinculada corretamente ao ID do profissional"""
        res = self.client.post(self.consulta_url, self.payload, format='json')

        self.assertEqual(
            res.status_code, 201, msg=f'Erro retornado: {res.data}'
        )
        self.assertEqual(res.data['profissional'], self.profissional.id)
        self.assertEqual(res.data['status'], 'AGENDADO')

    def test_cannot_create_consulta_with_invalid_profissional(self):
        """Integridade: Impede vincular consulta a um profissional que não existe"""
        self.payload['profissional'] = 99999  # ID inexistente
        res = self.client.post(self.consulta_url, self.payload, format='json')

        self.assertEqual(res.status_code, 400)
        self.assertIn('profissional', res.data)

    def test_can_list_consultas(self):
        """Sucesso: Listagem de consultas (Garante que o endpoint GET funciona)"""
        Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome='Maria Teste',
            data_hora=timezone.now() + timedelta(days=2),
        )
        res = self.client.get(self.consulta_url)
        self.assertEqual(res.status_code, 200)
        # Verifica se o resultado está dentro da chave 'results' da paginação
        self.assertGreaterEqual(len(res.data['results']), 1)

    def test_delete_profissional_cascade_behavior(self):
        """Integridade: Verifica se a consulta é removida ao deletar o profissional (CASCADE)"""
        consulta = Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome='Paciente Excluido',
            data_hora=timezone.now() + timedelta(days=2),
        )
        # Deleta o 'Pai'
        self.profissional.delete()

        # Verifica se o 'Filho' (Consulta) deixou de existir
        exists = Consulta.objects.filter(id=consulta.id).exists()
        self.assertFalse(
            exists, 'A consulta deveria ter sido removida em cascata.'
        )

    def test_update_consulta_status(self):
        """Sucesso: Alterar status da consulta (ex: de AGENDADA para REALIZADA)"""
        consulta = Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome='Status Teste',
            data_hora=timezone.now() + timedelta(days=2),
        )
        url = reverse('consulta-detail', kwargs={'pk': consulta.id})

        # Realizamos um PATCH para mudar apenas o status
        res = self.client.patch(url, {'status': 'REALIZADO'}, format='json')

        self.assertEqual(
            res.status_code, 200, msg=f'Erro retornado: {res.data}'
        )
        self.assertEqual(res.data['status'], 'REALIZADO')

    def test_cannot_schedule_in_past(self):
        """Regra de Negócio: Impede agendamento em data/hora passada"""
        data_passada = (timezone.now() - timedelta(days=1)).isoformat()
        self.payload['data_hora'] = data_passada

        res = self.client.post(self.consulta_url, self.payload, format='json')

        self.assertEqual(res.status_code, 400)
        # O erro deve ser reportado no campo data_hora ou vindo da validação global
        self.assertTrue(
            'data_hora' in str(res.data) or 'non_field_errors' in res.data
        )
