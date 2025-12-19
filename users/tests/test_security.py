from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp
from users.models import Profissional


class TestSecurity(TestSetUp):
    def setUp(self):
        super().setUp()
        # Criamos um registro para testar endpoints de detalhe
        self.prof = Profissional.objects.create(**self.profissional_data)
        self.list_url = reverse('profissional-list')
        self.detail_url = reverse(
            'profissional-detail', kwargs={'pk': self.prof.id}
        )

    def test_should_deny_list_profissionais_without_token(self):
        """Segurança: Bloqueia listagem (GET) para usuários não autenticados"""
        self.client.credentials()  # Limpa qualquer token do header
        res = self.client.get(self.list_url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            res.data['detail'],
            'As credenciais de autenticação não foram fornecidas.',
        )

    def test_should_deny_create_profissional_without_token(self):
        """Segurança: Bloqueia criação (POST) para usuários não autenticados"""
        self.client.credentials()
        res = self.client.post(
            self.list_url, self.profissional_data, format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_deny_update_profissional_without_token(self):
        """Segurança: Bloqueia edição (PATCH) para usuários não autenticados"""
        self.client.credentials()
        res = self.client.patch(
            self.detail_url, {'nome_social': 'Invasor'}, format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_deny_delete_profissional_without_token(self):
        """Segurança: Bloqueia deleção (DELETE) para usuários não autenticados"""
        self.client.credentials()
        res = self.client.delete(self.detail_url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_deny_access_with_invalid_token(self):
        """Segurança: Bloqueia acesso se o token for malformado ou expirado"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer token_totalmente_errado'
        )
        res = self.client.get(self.list_url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['code'], 'token_not_valid')
