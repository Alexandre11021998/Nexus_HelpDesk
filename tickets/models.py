from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    # Associa a Empresa a uma conta de usuário para login
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa')
    nome_fantasia = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_fantasia


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('AGUARDANDO_CLIENTE', 'Aguardando Cliente'),
        ('RESOLVIDO', 'Resolvido'),
        ('FECHADO', 'Fechado'),
    ]

    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tickets')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(verbose_name="Descrição do Problema")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='MEDIA')
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.titulo} ({self.empresa.nome_fantasia})"


class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.username} no Ticket #{self.ticket.id}"