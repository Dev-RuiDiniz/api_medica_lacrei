from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestSetUp(APITestCase):
    def setUp(self):
        """
        Configura o ambiente antes de cada teste:
        Cria usuário, obtém token e configura o cabeçalho de autenticação.
        """
        self.user_data = {'username': 'testuser', 'password': 'password123'}
        self.user = User.objects.create_superuser(**self.user_data)

        # URL para obter o token
        self.token_url = reverse('token_obtain_pair')

        # Obtendo o token JWT
        response = self.client.post(
            self.token_url, self.user_data, format='json'
        )
        self.access_token = response.data['access']

        # Configura o cliente para usar o Token em todas as requisições
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        # Dados de exemplo para uso nos testes
        self.profissional_data = {
            'nome_social': 'Dr. Rui Teste',
            'nome_registro': 'Rui Francisco',  # Se for o nome civil
            'profissao': 'MED',  # 'M' para Médico
            'registro_profissional': 'CRM-SP 123456',
            'email': 'dr_rui_teste@exemplo.com',
            'telefone': '11988887777',
            'cep': '01234567',
            'logradouro': 'Avenida Paulista',
            'cidade': 'São Paulo',
            'estado': 'SP',
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
