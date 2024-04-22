from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import time
from django.contrib.messages import constants
from django.contrib.messages import add_message
from django.contrib import auth


def cadastro(request):
    if request.method == 'GET':
      return render(request, 'cadastro.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmarsenha = request.POST.get('confirmarsenha')
        

        print(username, email, senha, confirmarsenha)

        if senha != confirmarsenha:
            add_message(request, constants.ERROR, 'As senhas não batem seu viado')
            time.sleep(1)
            return redirect('/usuarios/cadastro/')
        
        users = User.objects.filter(username=username)

        if users.exists():
            add_message(request, constants.ERROR, 'Ja tem um viado que se chama assim')
            return redirect('/usuarios/cadastro/')


          
       
        user = User.objects.create_user(username= username, email = email,  password=senha)


        return HttpResponse('cadastro realizado com sucesso')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
         username = request.POST.get('username')
         senha = request.POST.get('senha')
       
         user = auth.authenticate(request, username=username, password=senha)
    
    if user:
        auth.login(request, user)
        return redirect ('/pacientes/home')
    else:
        add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return redirect('/usuarios/login')
    



def sair(request):
    auth.logout(request)
    return redirect('login')
