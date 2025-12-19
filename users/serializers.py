import bleach
from rest_framework import serializers
from django.utils import timezone
from .models import Profissional, Consulta

class ProfissionalSerializer(serializers.ModelSerializer):
    profissao_display = serializers.CharField(source='get_profissao_display', read_only=True)

    class Meta:
        model = Profissional
        fields = [
            'id', 'nome_social', 'nome_registro', 'profissao', 
            'profissao_display', 'registro_profissional', 'email', 
            'telefone', 'cep', 'logradouro', 'cidade', 'estado'
        ]

    def validate(self, data):
        for field, value in data.items():
            if isinstance(value, str):
                data[field] = bleach.clean(value, tags=[], strip=True).strip()
        return data

class ConsultaSerializer(serializers.ModelSerializer):
    profissional_detalhes = ProfissionalSerializer(source='profissional', read_only=True)

    class Meta:
        model = Consulta
        fields = [
            'id', 'profissional', 'profissional_detalhes', 
            'data_hora', 'paciente_nome', 'status', 'observacoes'
        ]
        
    def validate_data_hora(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("A data da consulta não pode ser no passado.")
        return value

    def validate(self, data):
        # 1. Recupera os dados atuais da instância se for um UPDATE (PATCH/PUT)
        # Se o campo não estiver no 'data' (payload do PATCH), pegamos do objeto existente
        data_hora = data.get('data_hora', getattr(self.instance, 'data_hora', None))
        profissional = data.get('profissional', getattr(self.instance, 'profissional', None))
        
        instance_id = self.instance.id if self.instance else None

        # 2. Validação de data (Só compara se data_hora existir)
        if data_hora and data_hora < timezone.now():
            raise serializers.ValidationError({"data_hora": "A data da consulta não pode ser no passado."})

        # 3. Validação de conflito de horário
        # Só valida se tivermos as duas informações necessárias
        if profissional and data_hora:
            conflito = Consulta.objects.filter(
                profissional=profissional,
                data_hora=data_hora
            ).exclude(id=instance_id)

            if conflito.exists():
                raise serializers.ValidationError(
                    {"detail": "Este profissional já possui um agendamento neste horário."}
                )
        
        # 4. Sanitização contra XSS
        for field, value in data.items():
            if isinstance(value, str):
                data[field] = bleach.clean(value, tags=[], strip=True).strip()
                
        return data