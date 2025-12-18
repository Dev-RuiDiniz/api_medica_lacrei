from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer

class ProfissionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e excluir profissionais.
    """
    queryset = Profissional.objects.all().order_by('nome_social')
    serializer_class = ProfissionalSerializer
    
    # Habilita busca por nome social e filtro por profissão
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['profissao', 'estado']
    search_fields = ['nome_social', 'email']

class ConsultaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar o agendamento de consultas.
    """
    queryset = Consulta.objects.all().order_by('-data_hora')
    serializer_class = ConsultaSerializer
    
    # Habilita filtros por status e data
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'profissional']

    def perform_create(self, serializer):
        # Exemplo de lógica customizada: você pode adicionar logs ou 
        # enviar notificações aqui ao salvar uma nova consulta.
        serializer.save()