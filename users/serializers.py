from rest_framework import serializers
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

class ConsultaSerializer(serializers.ModelSerializer):
    # Mostra os detalhes do profissional dentro da consulta (opcional)
    profissional_detalhes = ProfissionalSerializer(source='profissional', read_only=True)

    class Meta:
        model = Consulta
        fields = [
            'id', 'profissional', 'profissional_detalhes', 
            'data_hora', 'paciente_nome', 'status', 'observacoes'
        ]
        
    def validate_data_hora(self, value):
        """
        Exemplo de validação: Impede agendamentos no passado.
        """
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("A data da consulta não pode ser no passado.")
        return value