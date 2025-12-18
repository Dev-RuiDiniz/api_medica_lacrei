import bleach
from rest_framework import serializers
from django.utils import timezone
from .models import Profissional, Consulta

class ProfissionalSerializer(serializers.ModelSerializer):
    # Campo calculado para mostrar o rótulo amigável da profissão (ex: Médico(a))
    profissao_display = serializers.CharField(source='get_profissao_display', read_only=True)

    class Meta:
        model = Profissional
        fields = [
            'id', 'nome_social', 'nome_registro', 'profissao', 
            'profissao_display', 'registro_profissional', 'email', 
            'telefone', 'cep', 'logradouro', 'cidade', 'estado'
        ]

    def validate(self, data):
        """
        Sanitização global para campos de texto do Profissional.
        """
        for field, value in data.items():
            if isinstance(value, str):
                # Remove tags HTML e limpa espaços extras
                data[field] = bleach.clean(value, tags=[], strip=True).strip()
        return data

class ConsultaSerializer(serializers.ModelSerializer):
    # Detalhes ricos do profissional para o GET, mantendo a FK para o POST
    profissional_detalhes = ProfissionalSerializer(source='profissional', read_only=True)

    class Meta:
        model = Consulta
        fields = [
            'id', 'profissional', 'profissional_detalhes', 
            'data_hora', 'paciente_nome', 'status', 'observacoes'
        ]
        
    def validate_data_hora(self, value):
        """
        Impede agendamentos no passado.
        """
        if value < timezone.now():
            raise serializers.ValidationError("A data da consulta não pode ser no passado.")
        return value

    def validate(self, data):
        """
        Sanitização global para campos de texto da Consulta (Paciente e Observações).
        """
        for field, value in data.items():
            if isinstance(value, str):
                data[field] = bleach.clean(value, tags=[], strip=True).strip()
        return data