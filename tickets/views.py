from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import EmpresaCadastroForm, TicketForm, ComentarioForm
from django.db.models import Count, Q

def cadastrar_empresa(request):
    if request.method == 'POST':
        form = EmpresaCadastroForm(request.POST)
        if form.is_valid():
            empresa = form.save()
            #Efetua o login automático
            login(request, empresa.usuario)
            return redirect('lista_tickets')
    else:
        form = EmpresaCadastroForm()
    return render(request, 'tickets/cadastrar_empresa.html', {'form': form})

@login_required
def lista_tickets(request):
    #Apenas tickets do usuário logado e pertencentes a empresa
    if hasattr(request.user, 'empresa'):
        base_tickets = Ticket.objects.filter(empresa=request.user.empresa)
    elif request.user.is_staff:
        base_tickets = Ticket.objects.all()
    else:
        base_tickets = Ticket.objects.none()

    #Ordenação final da tabela
    tickets = base_tickets.order_by('-data_criacao')
    #Métricas para cards
    metricas = base_tickets.aggregate(
        total=Count('id'),
        abertos=Count('id', filter=Q(status='ABERTO')),
        em_andamento=Count('id', filter=Q(status='EM_ANDAMENTO')),
        aguardando=Count('id', filter=Q(status='AGUARDANDO')),
        resolvidos=Count('id', filter=Q(status='RESOLVIDO')),
    )

    return render(request, 'tickets/lista_tickets.html', {
        'tickets': tickets,
        'metricas': metricas
    })

@login_required
def criar_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.empresa = request.user.empresa
            ticket.save()
            return redirect('lista_tickets')
    else:
        form = TicketForm()
    return render(request, 'tickets/criar_ticket.html', {'form': form})

@login_required
def detalhe_ticket(request, pk):
    #Garante que a empresa visualize apenas os tickets dela
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        ticket = get_object_or_404(Ticket, pk=pk, empresa=request.user.empresa)

    comentarios = ticket.comentarios.all().order_by('data_envio')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.ticket = ticket
            comentario.autor = request.user
            comentario.save()
            return redirect('detalhe_ticket', pk=ticket.pk)
    else:
        form = ComentarioForm()

    return render(request, 'tickets/detalhe_ticket.html', {
        'ticket': ticket,
        'comentarios': comentarios,
        'form': form
    })