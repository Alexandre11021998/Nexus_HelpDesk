from django import forms
from django.contrib.auth.models import User
from .models import Empresa, Ticket, Comentario


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descricao', 'prioridade']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resumo do problema'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva detalhadamente o seu problema'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adicione um comentário ou resposta'}),
        }


# --- FORMULÁRIO DE ATUALIZAÇÃO DE STATUS DE TICKET ---
class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }


# --- FORMULÁRIO DE CADASTRO DE EMPRESA ---
class EmpresaCadastroForm(forms.ModelForm):
    username = forms.CharField(
        label='Nome de usuário (Login)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario_empresa'})
    )
    email = forms.EmailField(
        label='Email de contato',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@empresa.com'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha de acesso'})
    )

    class Meta:
        model = Empresa
        fields = ['nome_fantasia', 'cnpj', 'telefone']
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão social ou Nome Fantasia da empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0001-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
        }

    def save(self, commit=True):
        # 1. Cria o usuário
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        ) 
        # 2. Cria perfil da empresa
        empresa = super().save(commit=False)
        empresa.usuario = user
        if commit:
            empresa.save()
        return empresa