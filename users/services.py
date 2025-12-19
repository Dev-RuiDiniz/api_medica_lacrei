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
        # No cenário real, buscaríamos o email/CPF do paciente
        payload = {'name': paciente_nome}
        # return requests.post(f"{self.url}/customers", json=payload, headers=self.headers)
        return {'id': 'cus_000001'}   # Mock para o desafio

    def gerar_cobranca(self, consulta):
        cliente_id = self.criar_cliente(consulta.paciente_nome)['id']

        payload = {
            'customer': cliente_id,
            'billingType': 'PIX',
            'value': 150.00,  # Valor fixo sugerido para o MVP
            'dueDate': consulta.data_hora.date().isoformat(),
            'description': f'Consulta com {consulta.profissional.nome_social}',
            'externalReference': str(consulta.id),
        }
        # return requests.post(f"{self.url}/payments", json=payload, headers=self.headers)
        return {
            'id': 'pay_999888777',
            'invoiceUrl': 'https://sandbox.asaas.com/i/999888777',
            'status': 'PENDING',
        }
