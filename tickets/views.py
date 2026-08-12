from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import EmpresaCadastroForm, TicketForm, ComentarioForm, TicketStatusForm    
from django.db.models import Count, Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login

@staff_member_required
def painel_suporte(request):
    status_filtro = request.GET.get('status', 'TODOS')

    #Alteração rápida de status
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form_status = TicketStatusForm(request.POST, instance=ticket)
        if form_status.is_valid():
            form_status.save()
            return redirect(f"{request.path}?status={status_filtro}")

    tickets = Ticket.objects.all().select_related('empresa').order_by('-data_criacao')

    if status_filtro != 'TODOS':
        tickets = tickets.filter(status=status_filtro)

    #Contador de tickets por status
    contadores ={
        'todos': Ticket.objects.count(),
        'aberto': Ticket.objects.filter(status='ABERTO').count(),
        'em_andamento': Ticket.objects.filter(status='EM_ANDAMENTO').count(),
        'aguardando': Ticket.objects.filter(status='AGUARDANDO').count(),
        'resolvido': Ticket.objects.filter(status='RESOLVIDO').count(),
    }

    return render(request, 'tickets/painel_suporte.html', {
        'tickets': tickets,
        'status_filtro': status_filtro,
        'contadores': contadores,
        'status_choices': Ticket.STATUS_CHOICES
    })

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