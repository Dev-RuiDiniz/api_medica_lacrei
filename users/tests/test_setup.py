from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profissional

class TestSetUp(APITestCase):
    def setUp(self):
        """
        Configura o ambiente antes de cada teste:
        Cria usuário, obtém token e configura o cabeçalho de autenticação.
        """
        self.user_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create_superuser(**self.user_data)
        
        # URL para obter o token
        self.token_url = reverse('token_obtain_pair')
        
        # Obtendo o token JWT
        response = self.client.post(self.token_url, self.user_data, format="json")
        self.access_token = response.data['access']
        
        # Configura o cliente para usar o Token em todas as requisições
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Dados de exemplo para uso nos testes
        self.profissional_data = {
            "nome_social": "Dr. Teste Sanitizado",
            "nome_registro": "Teste Registro",
            "profissao": "M",
            "registro_profissional": "123456",
            "email": "teste@lacrei.com",
            "telefone": "11999999999",
            "cep": "01234567",
            "logradouro": "Rua Teste",
            "cidade": "São Paulo",
            "estado": "SP"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()