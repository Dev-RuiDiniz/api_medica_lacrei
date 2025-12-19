from django.conf import settings


class AsaasService:
    """
    Integração com a API do Asaas para cobrança de consultas.
    """

    def __init__(self):
        self.api_key = getattr(settings, 'ASAAS_API_KEY', 'mock_key')
        self.url = 'https://sandbox.asaas.com/api/v3'
        self.headers = {'access_token': self.api_key}

    def criar_cliente(self, paciente_nome):
        """
        Simula a criação de um cliente no Asaas.
        """
        # No cenário real: payload = {'name': paciente_nome}
        # requests.post(f"{self.url}/customers", json=payload, headers=self.headers)
        return {'id': 'cus_000001'}  # Mock para o desafio

    def gerar_cobranca(self, consulta):
        """
        Simula a geração de uma cobrança PIX.
        """
        cliente_id = self.criar_cliente(consulta.paciente_nome)['id']

        return {
            'id': f'pay_{consulta.id}',
            'status': 'PENDING',
            'invoiceUrl': 'https://asaas.com/i/mock_pix',
            'value': 150.00,
            'customer': cliente_id
        }