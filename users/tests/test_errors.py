from django.urls import reverse
from .test_setup import TestSetUp

class TestErrorHandling(TestSetUp):

    def test_create_profissional_missing_fields(self):
        """Erro: Tenta criar profissional sem campos obrigatórios (ex: email e nome)"""
        # Enviamos um payload vazio
        res = self.client.post(reverse('profissional-list'), {})
        
        self.assertEqual(res.status_code, 400)
        # Verifica se a API aponta quais campos faltam
        self.assertIn('email', res.data)
        self.assertIn('nome_social', res.data)

    def test_create_profissional_invalid_email(self):
        """Erro: Tenta criar profissional com formato de e-mail inválido"""
        invalid_data = self.profissional_data.copy()
        invalid_data['email'] = 'email_que_nao_existe.com' # Sem o @
        
        res = self.client.post(reverse('profissional-list'), invalid_data)
        
        self.assertEqual(res.status_code, 400)
        self.assertIn('email', res.data)

    def test_create_consulta_invalid_status(self):
        """Erro: Tenta criar consulta com status que não existe nas opções (Choices)"""
        invalid_consulta = {
            "profissional": 1, # ID hipotético
            "paciente_nome": "Teste",
            "data_hora": "2025-12-25T10:00:00Z",
            "status": "STATUS_INVENTADO" # Não está no nosso Model
        }
        
        res = self.client.post(reverse('consulta-list'), invalid_consulta)
        
        self.assertEqual(res.status_code, 400)
        self.assertIn('status', res.data)

    def test_update_non_existent_resource(self):
        """Erro: Tenta editar um profissional que não existe (404)"""
        url = reverse('profissional-detail', kwargs={'pk': 99999})
        res = self.client.patch(url, {'nome_social': 'Novo Nome'})
        
        self.assertEqual(res.status_code, 404)