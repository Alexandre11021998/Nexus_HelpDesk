from django.contrib import admin
from .models import Empresa, Ticket, Comentario

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj', 'usuario', 'data_cadastro')
    search_fields = ('nome_fantasia', 'cnpj')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'empresa', 'status', 'prioridade', 'data_criacao')
    list_filter = ('status', 'prioridade', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'empresa__nome_fantasia')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'autor', 'data_envio')
    search_fields = ('texto',)