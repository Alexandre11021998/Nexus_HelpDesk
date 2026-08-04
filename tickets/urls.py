from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'),
    path('novo/', views.criar_ticket, name='criar_ticket'),
    path('<int:pk>/', views.detalhe_ticket, name='detalhe_ticket'),
]