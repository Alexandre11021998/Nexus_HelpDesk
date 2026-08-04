from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),

    # Autenticação e cadastro
    path('cadastrar/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('login/', auth_views.LoginView.as_view(template_name='tickets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]