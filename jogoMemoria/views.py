from django.shortcuts import render, redirect # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout

from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from jogoMemoria.models import Jogo, Jogador
from django.http import JsonResponse

def jogador_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try: 
                jogador = user.jogador  
            except Jogador.DoesNotExist:
                return render(request, 'login.html', {'error': 'Usuário não encontrado.'})
            
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})

    return render(request, 'login.html', )

def jogador_cadastro(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()

            if Jogador.objects.filter(user=user).exists():
                messages.error(request, 'Este usuário já está cadastrado como jogador.')
            else:
                nickname = request.POST.get('nickname')
                Jogador.objects.create(user=user, nickname=nickname)
                messages.success(request, 'Cadastro realizado com sucesso!')

            return redirect('login')  # Redireciona para a página de login
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os dados.')
    else:
        user_form = UserCreationForm()  # Formulário de cadastro do User

    return render(request, 'cadastro.html', {'user_form': user_form})

def jogador_logout(request):
    logout(request)
    return redirect('login')
def format_time(seconds):
    try:
        seconds = int(seconds)
    except ValueError:
        return "0m 00s"

    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds:02d}s"


def jogo_ranking(request):
    data_jogos = Jogo.objects.all().order_by('tentativas', 'tempo', '-data_hora')
    lista_jogos = []
    posicao = 1
    for jogo in data_jogos:
        local_time = jogo.data_hora
        jogo.tempo = format_time(jogo.tempo)
        lista_jogos.append({
            "Posição": f"{posicao}°",
            "Nome": jogo.nome,
            "Tentativas": jogo.tentativas,
            "Tempo": jogo.tempo,
            "Data": local_time.strftime("%d/%m/%Y"),
            "Hora": local_time.strftime("%H:%M:%S"),
        })
        posicao += 1
    return render(request, 'ranking.html', {'jogo_listar': lista_jogos})

@login_required
def jogo_index(request):
    return render(request, 'index.html')

@login_required
def salvar_jogo(request):
    if request.method == "POST":
        try:
            tentativas = request.POST.get('tentativas')
            tempo = request.POST.get('tempo')

            jogador = Jogador.objects.get(user=request.user)

            jogo = Jogo.objects.create(
                nome=jogador.nickname,  
                tentativas=tentativas,
                tempo=tempo,
                jogador=jogador 
            )
            
            return JsonResponse({"status": "success", "message": "Jogo salvo com sucesso!"})
        
        except Jogador.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Jogador não encontrado."}, status=404)
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")
            return JsonResponse({"status": "error", "message": "Erro ao salvar o jogo."}, status=500)
