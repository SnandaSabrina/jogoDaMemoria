"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.shortcuts import redirect
# from django.conf import settings
# from django.conf.urls.static import static
from jogoMemoria.views import jogador_login, jogador_cadastro, jogador_logout, jogo_index, jogo_ranking, salvar_jogo 

urlpatterns = [
    path('login/', jogador_login, name='login'),
    path('cadastro/', jogador_cadastro, name='cadastro'),
    path('', jogo_index, name='index'),
    path('ranking/', jogo_ranking, name='ranking'),
    path('salvar-jogo/', salvar_jogo, name='salvar-jogo'),
    path('logout/', jogador_logout, name='logout'),  # URL de logout
    re_path(r'.*', lambda request: redirect('/')),
    # path('admin/', admin.site.urls),
]