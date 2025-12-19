from django.urls import reverse
from .test_setup import TestSetUp
from users.models import Profissional

class TestProfissionalViews(TestSetUp):
    
    def test_can_create_profissional_with_auth(self):
        """Sucesso: Criação de profissional"""
        res = self.client.post(reverse('profissional-list'), self.profissional_data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['nome_social'], self.profissional_data['nome_social'])

    def test_can_list_profissionais(self):
        """Sucesso: Listagem de profissionais"""
        # Primeiro, garantimos que existe um profissional no banco
        Profissional.objects.create(**self.profissional_data)
        
        res = self.client.get(reverse('profissional-list'))
        self.assertEqual(res.status_code, 200)
        # Verifica se o retorno é uma lista e se tem pelo menos 1 item
        self.assertIsInstance(res.data['results'], list)
        self.assertGreaterEqual(len(res.data['results']), 1)

    def test_can_retrieve_single_profissional(self):
        """Sucesso: Detalhe de um profissional específico"""
        prof = Profissional.objects.create(**self.profissional_data)
        url = reverse('profissional-detail', kwargs={'pk': prof.id})
        
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['nome_social'], prof.nome_social)

    def test_can_update_profissional(self):
        """Sucesso: Edição (PATCH) de um profissional"""
        prof = Profissional.objects.create(**self.profissional_data)
        url = reverse('profissional-detail', kwargs={'pk': prof.id})
        
        novo_nome = "Dr. Rui Francisco Editado"
        res = self.client.patch(url, {'nome_social': novo_nome})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['nome_social'], novo_nome)

    def test_cannot_create_profissional_without_auth(self):
        """Segurança: Bloqueio de acesso anônimo"""
        self.client.credentials() 
        res = self.client.post(reverse('profissional-list'), self.profissional_data)
        self.assertEqual(res.status_code, 401)