from django.db import models

class Profissional(models.Model):
    PROFISSÕES_CHOICES = [
        ('MED', 'Médico(a)'),
        ('PSI', 'Psicólogo(a)'),
        ('ENF', 'Enfermeiro(a)'),
        # Podemos expandir depois
    ]

    # Identificação (Foco em Nome Social)
    nome_social = models.CharField("Nome Social", max_length=150)
    nome_registro = models.CharField("Nome de Registro", max_length=150, help_text="Para fins de documentos oficiais")
    
    # Atuação
    profissao = models.CharField("Profissão", max_length=3, choices=PROFISSÕES_CHOICES)
    registro_profissional = models.CharField("Registro (ex: CRM/CRP)", max_length=50)

    # Contato
    email = models.EmailField("E-mail de Contato", unique=True)
    telefone = models.CharField("Telefone/WhatsApp", max_length=20)

    # Endereço (Simplificado para o MVP)
    logradouro = models.CharField("Endereço", max_length=255)
    cidade = models.CharField("Cidade", max_length=100)
    estado = models.CharField("Estado", max_length=2)
    cep = models.CharField("CEP", max_length=9)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"

    def __str__(self):
        return f"{self.nome_social} ({self.get_profissao_display()})"