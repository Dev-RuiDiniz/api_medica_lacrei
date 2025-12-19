from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Profissional(models.Model):
    PROFISSÕES_CHOICES = [
        ('MED', 'Médico(a)'),
        ('PSI', 'Psicólogo(a)'),
        ('ENF', 'Enfermeiro(a)'),
        # Podemos expandir depois
    ]

    # Identificação (Foco em Nome Social)
    nome_social = models.CharField('Nome Social', max_length=150)
    nome_registro = models.CharField(
        'Nome de Registro',
        max_length=150,
        help_text='Para fins de documentos oficiais',
    )

    # Atuação
    profissao = models.CharField(
        'Profissão', max_length=3, choices=PROFISSÕES_CHOICES
    )
    registro_profissional = models.CharField(
        'Registro (ex: CRM/CRP)', max_length=50
    )

    # Contato
    email = models.EmailField('E-mail de Contato', unique=True)
    telefone = models.CharField('Telefone/WhatsApp', max_length=20)

    # Endereço (Simplificado para o MVP)
    logradouro = models.CharField('Endereço', max_length=255)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=9)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'

    def __str__(self):
        return f'{self.nome_social} ({self.get_profissao_display()})'


class Consulta(models.Model):
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    # Relacionamento: Se o profissional for deletado, as consultas dele também serão (CASCADE)
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name='consultas',
        verbose_name='Profissional',
    )

    # Dados da Consulta
    data_hora = models.DateTimeField('Data e Hora da Consulta')
    paciente_nome = models.CharField('Nome do Paciente', max_length=150)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='AGENDADO'
    )
    observacoes = models.TextField(
        'Observações Clínicas', blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.paciente_nome} com {self.profissional.nome_social} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        """
        Validações de regra de negócio antes de salvar.
        """
        # 1. Impedir datas no passado
        if self.data_hora < timezone.now():
            raise ValidationError(
                'Não é possível agendar uma consulta para uma data passada.'
            )

        # 2. Impedir horários conflitantes para o mesmo profissional
        # Verifica se já existe uma consulta para o mesmo profissional no mesmo horário
        conflito = Consulta.objects.filter(
            profissional=self.profissional, data_hora=self.data_hora
        ).exclude(
            id=self.id
        )   # Exclui a própria consulta em caso de edição

        if conflito.exists():
            raise ValidationError(
                f'O profissional {self.profissional.nome_social} já possui uma consulta agendada para este horário.'
            )

    def save(self, *args, **kwargs):
        """
        Sobrescreve o save para garantir que o clean() seja chamado,
        pois o Django não chama clean() automaticamente no save().
        """
        self.full_clean()
        super().save(*args, **kwargs)
