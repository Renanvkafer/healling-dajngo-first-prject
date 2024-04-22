from django.shortcuts import render, redirect
from medico.models import DadosMedico, Especialidades, medico_datas, is_medico
from datetime import datetime
from .models import consulta
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.


def home(request):
    if request.method =='GET':
       medico_filtrar = request.GET.get('medico')
       especialidades_filtrar = request.GET.get('especialidades')
       medicos = DadosMedico.objects.all()
       if medico_filtrar:
           medicos = medicos.filter(nome__icontains=medico_filtrar)

       if especialidades_filtrar:
           medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

       especialidades = Especialidades.objects.all()
       return render (request, 'home.html', {'medicos': medicos,'especialidades':especialidades, 'is_medico': is_medico(request.user)})
    

def escolher_horario(request, id_dados_medicos):
    if request.method == 'GET':
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datasabertas = medico_datas.objects.filter(user=medico.user).filter(agendado=False).filter(data__gt=datetime.now())
        return render(request, 'escolher_horario.html', {'medico': medico, 'datasabertas': datasabertas, 'is_medico': is_medico(request.user)})
    

def agendar_horario(request, id_data_aberta):
    if request.method == 'GET':
        data_aberta = medico_datas.objects.get(id=id_data_aberta)

        horario_agendado = consulta(
            paciente = request.user,
            data_aberta = data_aberta
        )

        horario_agendado.save()

        medico_datas.agendado = True
        medico_datas.save()
        
        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso!')
        return redirect('/pacientes/minhas_consultas/')
    

def minhas_consultas(request):
    if request.method == 'GET':
        minhas_consultas = consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request,'minhas_consultas.html', {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})
    

def Consulta(request, id_consulta):
    if request.method == 'GET':
        Consulta = consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=Consulta.data_aberta.user)
        return render(request, 'consulta.html', {'Consulta': Consulta, 'dado_medico': dado_medico, 'is_medico': is_medico(request.user)})