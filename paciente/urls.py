from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('escolher_horario/<int:id_dados_medicos>/', views.escolher_horario, name='escolher_horario'),
    path('agendar_horario/<int:id_medico_datas>/', views.agendar_horario, name="agendar_horario"),
    path('minhas_consultas/', views.minhas_consultas, name="minhas_consultas"),
    path('consulta/<int:id_consulta>/', views.Consulta, name="consulta"),
]
