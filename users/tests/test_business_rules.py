from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .test_setup import TestSetUp
from users.models import Profissional, Consulta


class TestBusinessRules(TestSetUp):
    def setUp(self):
        super().setUp()
        # Criamos o profissional para os testes de agendamento
        self.profissional = Profissional.objects.create(
            **self.profissional_data
        )
        self.consulta_url = reverse('consulta-list')

    def test_cannot_schedule_in_past(self):
        """Regra 1: Impede agendamento em data/hora retroativa"""
        data_passada = (timezone.now() - timedelta(hours=5)).isoformat()

        payload = {
            'profissional': self.profissional.id,
            'paciente_nome': 'Paciente Erro',
            'data_hora': data_passada,
            'status': 'AGENDADO',
        }

        res = self.client.post(self.consulta_url, payload, format='json')

        # Esperamos 400 Bad Request
        self.assertEqual(res.status_code, 400)
        self.assertIn('data_hora', str(res.data))

    def test_cannot_schedule_conflict_same_professional(self):
        """Regra 2: Impede dois agendamentos no mesmo horário para o mesmo médico"""
        horario_comum = (timezone.now() + timedelta(days=10)).replace(
            minute=0, second=0, microsecond=0
        )

        # 1. Criar a primeira consulta com sucesso
        Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome='Paciente 1',
            data_hora=horario_comum,
            status='AGENDADO',
        )

        # 2. Tentar agendar outra para o MESMO profissional no MESMO horário
        payload_conflito = {
            'profissional': self.profissional.id,
            'paciente_nome': 'Paciente 2',
            'data_hora': horario_comum.isoformat(),
            'status': 'AGENDADO',
        }

        res = self.client.post(
            self.consulta_url, payload_conflito, format='json'
        )

        self.assertEqual(res.status_code, 400)
        # Verifica se a mensagem de erro de conflito retornou (ajuste conforme sua mensagem no Serializer)
        self.assertTrue('detail' in res.data or 'non_field_errors' in res.data)

    def test_can_schedule_same_time_different_professionals(self):
        """Regra 3: Permite agendamentos no mesmo horário se os profissionais forem diferentes"""
        horario_comum = timezone.now() + timedelta(days=5)

        # Profissional 1 já tem consulta
        Consulta.objects.create(
            profissional=self.profissional,
            paciente_nome='Paciente A',
            data_hora=horario_comum,
        )

        # Criamos um Profissional 2
        outro_profissional_data = self.profissional_data.copy()
        outro_profissional_data['email'] = 'outro@medico.com'
        outro_prof = Profissional.objects.create(**outro_profissional_data)

        # Tenta agendar para o Profissional 2 no mesmo horário
        payload = {
            'profissional': outro_prof.id,
            'paciente_nome': 'Paciente B',
            'data_hora': horario_comum.isoformat(),
            'status': 'AGENDADO',
        }

        res = self.client.post(self.consulta_url, payload, format='json')

        # Deve permitir (201 Created)
        self.assertEqual(res.status_code, 201)
