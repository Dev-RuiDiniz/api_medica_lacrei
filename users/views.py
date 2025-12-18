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
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['profissao', 'estado']
    search_fields = ['nome_social', 'email']

    def perform_create(self, serializer):
        # Registra a criação no log
        profissional = serializer.save()
        logger.info(f"[CREATE] Profissional '{profissional.nome_social}' cadastrado por usuário ID: {self.request.user.id}")

    def perform_update(self, serializer):
        # Registra a atualização no log
        profissional = serializer.save()
        logger.info(f"[UPDATE] Profissional ID {profissional.id} atualizado por usuário ID: {self.request.user.id}")

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all().order_by('-data_hora')
    serializer_class = ConsultaSerializer
    
    # 🔒 Proteção: Apenas usuários autenticados
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'profissional']

    def perform_create(self, serializer):
        # Registra o agendamento no log
        consulta = serializer.save()
        logger.info(f"[SCHEDULE] Nova consulta ID {consulta.id} agendada para o paciente '{consulta.paciente_nome}' por usuário ID: {self.request.user.id}")

    @action(detail=False, methods=['get'], url_path='por-profissional/(?P<prof_id>[^/.]+)')
    def por_profissional(self, request, prof_id=None):
        """
        Rota customizada protegida para buscar consultas de um profissional específico.
        """
        consultas = self.queryset.filter(profissional_id=prof_id)
        
        # Log de acesso à busca filtrada
        logger.debug(f"[FILTER] Usuário ID {request.user.id} consultou agenda do profissional ID {prof_id}")
        
        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)