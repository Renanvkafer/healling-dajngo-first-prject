from django.contrib import admin
from .models import Especialidades, DadosMedico, medico_datas

# Register your models here.

admin.site.register(Especialidades)
admin.site.register(DadosMedico)
admin.site.register(medico_datas)

