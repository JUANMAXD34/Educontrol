from django.contrib import admin
from .models import alumno,colegiatura,profesor,tutor,grupo,usuario

# Register your models here.
admin.site.register(colegiatura)
admin.site.register(profesor)
admin.site.register(grupo)
admin.site.register(tutor)
admin.site.register(alumno)
admin.site.register(usuario)