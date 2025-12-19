from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .test_setup import TestSetUp
from users.models import Profissional

class TestConsultaViews(TestSetUp):
    def setUp(self):
        super().setUp()
        # Criamos um profissional no banco de testes para vincular à consulta
        self.profissional = Profissional.objects.create(**self.profissional_data)
        
        self.consulta_url = reverse('consulta-list')
        
        # Dados de uma consulta válida (amanhã às 14h)
        self.data_valida = timezone.now() + timedelta(days=1)
        self.consulta_data = {
            "profissional": self.profissional.id,
            "paciente_nome": "Paciente de Teste",
            "data_hora": self.data_valida,
            "status": "AGENDADA"
        }

    def test_can_create_consulta(self):
        """Valida agendamento de consulta com sucesso"""
        res = self.client.post(self.consulta_url, self.consulta_data)
        self.assertEqual(res.status_code, 201)

    def test_cannot_schedule_in_past(self):
        """Regra de Negócio: Impede agendamento em data passada"""
        data_passada = timezone.now() - timedelta(days=1)
        self.consulta_data['data_hora'] = data_passada
        
        res = self.client.post(self.consulta_url, self.consulta_data)
        self.assertEqual(res.status_code, 400)
        self.assertIn('data_hora', res.data or str(res.data))

    def test_cannot_schedule_conflict(self):
        """Regra de Negócio: Impede conflito de horário para o mesmo profissional"""
        # 1. Cria a primeira consulta
        self.client.post(self.consulta_url, self.consulta_data)
        
        # 2. Tenta criar outra exatamente no mesmo horário para o mesmo médico
        res = self.client.post(self.consulta_url, self.consulta_data)
        
        self.assertEqual(res.status_code, 400)