from rest_framework import viewsets, filters, permissions # Adicionado permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all().order_by('nome_social')
    serializer_class = ProfissionalSerializer
    
    # 🔒 Proteção: Apenas usuários autenticados podem acessar
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['profissao', 'estado']
    search_fields = ['nome_social', 'email']

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all().order_by('-data_hora')
    serializer_class = ConsultaSerializer
    
    # 🔒 Proteção: Apenas usuários autenticados podem acessar
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'profissional']

    @action(detail=False, methods=['get'], url_path='por-profissional/(?P<prof_id>[^/.]+)')
    def por_profissional(self, request, prof_id=None):
        # A permissão definida acima também protege esta action customizada
        consultas = self.queryset.filter(profissional_id=prof_id)
        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)