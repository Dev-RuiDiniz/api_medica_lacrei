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
        Validação de nível de objeto para capturar conflitos antes do save.
        """
        # Acesso aos dados enviados
        profissional = data.get('profissional')
        data_hora = data.get('data_hora')
        
        # O ID é necessário para excluir a própria consulta em updates
        instance_id = self.instance.id if self.instance else None

        # Reutilizamos a lógica de conflito
        if data_hora < timezone.now():
            raise serializers.ValidationError({"data_hora": "A data da consulta não pode ser no passado."})

        conflito = Consulta.objects.filter(
            profissional=profissional,
            data_hora=data_hora
        ).exclude(id=instance_id)

        if conflito.exists():
            raise serializers.ValidationError(
                {"detail": "Este profissional já possui um agendamento neste horário."}
            )
        
        # Chama a sanitização que fizemos na tarefa anterior
        for field, value in data.items():
            if isinstance(value, str):
                import bleach
                data[field] = bleach.clean(value, tags=[], strip=True).strip()
                
        return data