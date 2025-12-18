from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

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
    queryset = Consulta.objects.all().order_by('-data_hora')
    serializer_class = ConsultaSerializer
    filterset_fields = ['status'] # Filtros normais

    # Criando a rota customizada: /api/v1/consultas/por_profissional/
    @action(detail=False, methods=['get'], url_path='por-profissional/(?P<prof_id>[^/.]+)')
    def por_profissional(self, request, prof_id=None):
        """
        Retorna todas as consultas vinculadas a um ID de profissional específico.
        """
        consultas = self.queryset.filter(profissional_id=prof_id)
        
        # Paginação (opcional, mas boa prática)
        page = self.paginate_queryset(consultas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)