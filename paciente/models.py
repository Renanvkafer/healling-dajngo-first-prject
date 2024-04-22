from django.db import models
from django.contrib.auth.models import  User
from medico.models import medico_datas
# Create your models here.


class consulta(models.Model):
    status_choices =(
            ( 'A', 'Aguendada'),
            ( 'F', 'Finalizada'),
            ( 'C', 'Cancelada'),
            ( 'I', 'Iniciada'),
            ('AV', 'Avaliada'),
    )
    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(medico_datas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.paciente.username