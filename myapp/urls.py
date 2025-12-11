from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index, name='index'),
    path('login/',views.Login, name='login'),
    path('inicio/',views.inicio, name='inicio'),
    path('alumnos/',views.Lista_alumnos, name='Lista'),
    path('Grupos/',views.Grupos, name='grupos'),
    path('generar-pdf/',views.generar_pdf, name='pdf'),
    path('docente/',views.maestro, name='docente'),
    path('<str:rol>/logout/',views.signout, name='logout'),
    path('pdf-profe/',views.pdf_profe),
    path('admin-usuario/',views.crud_usuarios,name='crud-usuarios'),
    path('admin-grupo/',views.crud_grupo,name='crud-grupo'),
    path('admin-alumnos/', views.crud_alumno, name='admin-alumno'),
    path('<str:pag>/añadir-alumno/', views.crud_alumno_añadir, name='crud-alumno-añadir'),
    path('admin-docente/', views.crud_docente, name='admin-docente'),
    path('<str:pag>/añadir/', views.crud_docente_añadir, name='crud_docente_añadir'),
    path("pagos/", views.lista_pagos, name="lista_pagos"),
    path('pdf-factura/',views.pdf_factura),
    path('informacion/', views.informacion),
    path('p/',views.crendencial),
    path('inicio-admin/', views.inicio_admin, name='inicio-admin')
]
