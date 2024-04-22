from django.shortcuts import render, redirect
from medico.models import Especialidades, DadosMedico, is_medico, medico_datas
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from paciente.models import consulta


def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Voce já possui um cadastro')
        return redirect('/medicos/abrir_horario/')


    
    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades, 'is_medico': is_medico(request.user)})
    elif request.method == 'POST':
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        daddos_medico = DadosMedico(
            crm = crm,
            nome = nome,
            cep = cep,
            rua = rua,
            bairro = bairro,
            numero = numero,
            rg = rg,
            cedula_identidade_medica = cim,
            foto = foto,
            especialidade_id = especialidade,
            descricao = descricao,
            valor_consulta = valor_consulta,
            user =  request.user
        )

        daddos_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso')
        return redirect('/medico/abrir_horario')


def abrir_horario(request):

    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Voce não possui um cadastro')
        return redirect('/usuarios/sair')
    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user = request.user)
        Medico_datas = medico_datas.objects.filter(user = request.user)
        formatted_dates = [date.data.strftime('%Y-%m-%dT%H:%M') for date in Medico_datas]
        return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos,  'Medico_datas': formatted_dates, 'is_medico': is_medico(request.user)})
    elif request.method == "POST":
        data = request.POST.get('data')
        print(type(data))
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        if data_formatada <= datetime.now():
          messages.add_message(request, constants.WARNING, 'Data inválida')
          return redirect('/medicos/abrir_horario/')
        horario_abrir = medico_datas(
            data = data,
            user = request.user,

        )
        horario_abrir.save()
        messages.add_message(request, constants.SUCCESS, 'Horário aberto com sucesso')
        return redirect('/medicos/abrir_horario/')
    

def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Voce não possui um cadastro medico')
        return redirect('/usuarios/sair')
    hoje = datetime.now().date()
    consultas_hoje = consulta

    consultas_hoje = consulta.objects.filter(data_aberta__user = request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = consulta.objects.exclude(id__in=consultas_hoje.values('id'))
    if request.method == 'GET':
       especialidades_filtrar = request.GET.get('especialidades')
       datas_filtrar = request.GET.get('datas')
       medicos = DadosMedico.objects.all()
       if especialidades_filtrar:
           especialidades = medicos.filter(especialidade_id__in=especialidades_filtrar)

       if datas_filtrar:
           medicos = medicos.filter(medico_datas__data__in=datas_filtrar)

       especialidades = Especialidades.objects.all()
           
    return render(request, 'consultas_medico.html', {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes, 'medicos': medicos, 'especialidades': especialidades, 'is_medico': is_medico(request.user)})


def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
       messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
       return redirect('/usuarios/sair')

    if request.method == "GET":
       Consulta = consulta.objects.get(id=id_consulta)
       return render(request, 'consulta_area_medico.html', {'Consulta': Consulta,'is_medico': is_medico(request.user)}) 
 
        