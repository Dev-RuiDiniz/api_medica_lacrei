from django.contrib import admin
from .models import Profissional, Consulta


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome_social', 'profissao', 'cidade', 'estado')
    search_fields = ('nome_social', 'email', 'registro_profissional')
    list_filter = ('profissao', 'estado')


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente_nome', 'profissional', 'data_hora', 'status')
    list_filter = ('status', 'data_hora')
    search_fields = ('paciente_nome', 'profissional__nome_social')
