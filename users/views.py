from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import logging

# Instanciando o logger para o app 'users'
logger = logging.getLogger(__name__)


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all().order_by('nome_social')
    serializer_class = ProfissionalSerializer

    # 🔒 Proteção: Apenas usuários autenticados
    permission_classes = [permissions.IsAuthenticated]

    # 🔍 Filtros: Busca textual, Filtro por campo e Ordenação
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Configuração da Tarefa 8: Campos pesquisáveis
    search_fields = ['nome_social', 'email', 'registro_profissional']

    # Campos para filtrar via query params (?estado=SP)
    filterset_fields = ['profissao', 'estado']

    # Campos que o frontend pode ordenar (?ordering=nome_social)
    ordering_fields = ['nome_social', 'profissao', 'estado']

    def perform_create(self, serializer):
        profissional = serializer.save()
        logger.info(
            f"[CREATE] Profissional '{profissional.nome_social}' cadastrado por usuário ID: {self.request.user.id}"
        )

    def perform_update(self, serializer):
        profissional = serializer.save()
        logger.info(
            f'[UPDATE] Profissional ID {profissional.id} atualizado por usuário ID: {self.request.user.id}'
        )


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all().order_by('-data_hora')
    serializer_class = ConsultaSerializer

    # 🔒 Proteção: Apenas usuários autenticados
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'profissional']
    ordering_fields = ['data_hora', 'status']

    def perform_create(self, serializer):
        consulta = serializer.save()
        logger.info(
            f"[SCHEDULE] Nova consulta ID {consulta.id} agendada para o paciente '{consulta.paciente_nome}' por usuário ID: {self.request.user.id}"
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='por-profissional/(?P<prof_id>[^/.]+)',
    )
    def por_profissional(self, request, prof_id=None):
        """
        Rota customizada protegida para buscar consultas de um profissional específico.
        """
        consultas = self.queryset.filter(profissional_id=prof_id)
        logger.debug(
            f'[FILTER] Usuário ID {request.user.id} consultou agenda do profissional ID {prof_id}'
        )

        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)
