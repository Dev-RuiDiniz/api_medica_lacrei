# users/tests/test_views.py
from .test_setup import TestSetUp
from django.urls import reverse

class TestProfissionalViews(TestSetUp):
    def test_cannot_create_profissional_without_auth(self):
        """Valida que sem token o acesso é negado (401)"""
        self.client.credentials() # Limpa o token para este teste específico
        res = self.client.post(reverse('profissional-list'), self.profissional_data)
        self.assertEqual(res.status_code, 401)

    def test_can_create_profissional_with_auth(self):
        """Valida a criação de profissional com usuário autenticado"""
        res = self.client.post(reverse('profissional-list'), self.profissional_data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['nome_social'], self.profissional_data['nome_social'])