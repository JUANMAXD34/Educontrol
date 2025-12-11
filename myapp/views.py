from django.http import HttpResponse
from django.contrib import messages
from .models import alumno, profesor, tutor, colegiatura, grupo, usuario
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import UsuarioForm, grupoForm, profesorForm, UserForm, AlumnoForm, TutorForm, ProfesorFormulario, PagoForm, PagoActualizar
from .utils import enviar_factura_por_correo

#Index
def Index(request):
    title = 'Hola'
    return render(request, 'index.html', {
        'title':title,
        'form':CreateNewTask()
    })

#Login y Logout
def Login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('inicio-admin')
        else:
            return redirect('inicio') 

    if request.method == 'POST':
        formulario = UserForm(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password']
            usuario = authenticate(username=username, password=password)
            if usuario:
                login(request, usuario)
                if usuario.is_superuser:
                    return redirect('inicio-admin')
                else:
                    return redirect('inicio')
        return render(request, 'login.html', {
            'form': formulario
        })
    else:
        form = UserForm()
        return render(request, 'login.html', {
            'form': form
        })

def signout(request, rol=None):
    logout(request)
    return redirect('index')

#Parte de usuario si no me pierdo xd, con rutas protegidas obvio
@login_required
def inicio(request):
    return render(request,'inicio.html')

@login_required
def Lista_alumnos(request):
    grupos = grupo.objects.all()
    tutores = tutor.objects.all()
    alumnos = alumno.objects.prefetch_related("tutores").all()
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'añadir-tutor':
            form = TutorForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                mensaje = 'El tutor fue agregado correctamente.'
                return render(request, 'alumnos.html', {
                    'alumno':alumnos,
                    'formulario':AlumnoForm(),
                    'form':TutorForm(),
                    'mensaje':mensaje,
                    "tutores": tutores,
                    "grupos": grupos
                })
            else:
                data_id = 1
                return render(request, 'alumnos.html', {
                    'alumno':alumnos,
                    'formulario':AlumnoForm(),
                    'form':form,
                    'error_id':data_id,
                    "tutores": tutores,
                    "grupos": grupos
                })
        elif form_type == 'añadir-alumno':
            form = AlumnoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                mensaje = 'El alumno fue agregado exitosamente.'
                alumnos = alumno.objects.all()
                return render(request, 'alumnos.html', {
                    'alumno':alumnos,
                    'formulario':AlumnoForm(),
                    'form':TutorForm(),
                    'mensaje':mensaje,
                    "tutores": tutores,
                    "grupos": grupos
                })
            else:
                data_id = 1
                return render(request, 'alumnos.html', {
                    'alumno':alumnos,
                    'formulario':form,
                    'form':TutorForm(),
                    'error_id2':data_id,
                    "tutores": tutores,
                    "grupos": grupos
                })
                
    else:
        return render(request, 'alumnos.html', {
            'alumno':alumnos,
            'formulario':AlumnoForm(),
            'form':TutorForm(),
            "tutores": tutores,
            "grupos": grupos
        })

@login_required
def informacion(request):
    id = request.GET.get('id')
    alumno_obj = get_object_or_404(alumno, id=id)
    grupo_obj = alumno_obj.grupo
    tutores_obj = alumno_obj.tutores.all()
    datos = {
        "alumno": alumno_obj,
        "grupo": grupo_obj,
        "tutores": tutores_obj,
    }
    return render(request, "informacion.html", datos)

@login_required
def Grupos(request):
    grupos = alumno.objects.all().order_by('apellidos_alumno')
    lista = grupo.objects.all().order_by('nombre_grupo')
    alumnos = alumno.objects.all()
    return render(request,'grupo.html', {
        'grupo':grupos,
        'lista':lista,
        'alumno':alumnos
    })

@login_required
def generar_pdf(request):
    grupo = request.GET.get('grupo')
    turno = request.GET.get('turno')
    alumnos = alumno.objects.select_related('grupo')
    if grupo:
        alumnos = alumnos.filter(grupo__nombre_grupo=grupo)
    if turno:
        alumnos = alumnos.filter(grupo__turno=turno)

    return render(request, 'descarga_pdf.html', {
        'alumno': alumnos,
        'now':timezone.now()
    })

@login_required
def maestro(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'buscar':
            id = request.POST.get('nombre_profesor')
            if id:
                profe = profesor.objects.get(pk=id)
                print('ola')
                return render(request, 'profesor.html', {
                    'profesor': profesor.objects.all(),
                    'datos': profe,
                    'form': profesorForm(),
                    'formulario':ProfesorFormulario()
                })
            else:
                print('error')
                print(id)
                return render(request,'profesor.html',{
                    'profesor':profesor.objects.all(),
                    'form': profesorForm(),
                    'formulario':ProfesorFormulario()
                })
        elif form_type == 'agregar':
            formulario = ProfesorFormulario(request.POST, request.FILES)
            if formulario.is_valid():
                formulario.save()
                mensaje = '¡Docente registrado exitosamente!'
                return render(request,'profesor.html',{
                    'profesor':profesor.objects.all(),
                    'form': profesorForm(),
                    'formulario':ProfesorFormulario(),
                    'mensaje':mensaje
                })
            else:
                instancia_id = 1
                return render(request,'profesor.html',{
                    'profesor':profesor.objects.all(),
                    'form':profesorForm(),
                    'formulario':formulario,
                    'error_id':instancia_id
                })
    else:    
        return render(request,'profesor.html',{
            'profesor':profesor.objects.all(),
            'form': profesorForm(),
            'formulario':ProfesorFormulario()
        })

@login_required
def pdf_profe(request):
    id = request.GET.get('id')
    profe = profesor.objects.all().get(pk=id)
    return render(request, 'pdf-profesores.html',{
        'profesor':profe
    })

@login_required
def lista_pagos(request):
    pagos = colegiatura.objects.select_related("alumno").order_by('id')
    alumnos = alumno.objects.all().order_by('id')
    pago_seleccionado = None
    form = None
    formulario = PagoForm()

    if request.GET.get("pago_id"):
        pago_id = request.GET.get("pago_id")
        pago_seleccionado = get_object_or_404(colegiatura, id=pago_id)
        form = PagoActualizar(instance=pago_seleccionado)

    if request.method == "POST":
        pago_id = request.POST.get("pago_id")
        if pago_id: 
            pago_seleccionado = get_object_or_404(colegiatura, id=pago_id)
            form = PagoActualizar(request.POST, instance=pago_seleccionado)
            if form.is_valid():
                pago = form.save(commit=False) 
                pago.save()
                enviar_factura_por_correo(pago)
                mensaje = 'Pago realizado con exito, se enviara la factura atravez de correo electronico.'
                return render(request, "colegiatura.html", {
                    "pagos": pagos,
                    "alumnos": alumnos,
                    "pago_seleccionado": pago_seleccionado,
                    "form": PagoActualizar(),
                    "formulario": formulario,
                    'mensaje':mensaje
                })
            else:
                return render(request, "colegiatura.html", {
                    "pagos": pagos,
                    "alumnos": alumnos,
                    "pago_seleccionado": pago_seleccionado,
                    "form": form,
                    "formulario": formulario
                })
        else:
            formulario = PagoForm(request.POST)
            if formulario.is_valid():
                pago = formulario.save()
                enviar_factura_por_correo(pago)
                mensaje = 'Pago realizado con exito, se enviara la factura atravez de correo electronico.'
                return render(request, "colegiatura.html", {
                    "pagos": pagos,
                    "alumnos": alumnos,
                    "pago_seleccionado": pago_seleccionado,
                    "form": form,
                    "formulario": PagoForm(),
                    'mensaje':mensaje
                })
            else:
                return render(request, "colegiatura.html", {
                    "pagos": pagos,
                    "alumnos": alumnos,
                    "pago_seleccionado": pago_seleccionado,
                    "form": form,
                    "formulario": formulario
                })
    else:
        return render(request, "colegiatura.html", {
            "pagos": pagos,
            "alumnos": alumnos,
            "pago_seleccionado": pago_seleccionado,
            "form": form,
            "formulario": formulario
        })

@login_required
def pdf_factura(request):
    colegiatura_id = request.GET.get("colegiatura_id")
    pago = colegiatura.objects.select_related("alumno__grupo").prefetch_related("alumno__tutores").get(id=colegiatura_id)

    alumno = pago.alumno
    tutores = alumno.tutores.all()
    return render(request,"factura.html",{
        "alumno": alumno,
        "tutores": tutores,
        "colegiatura": pago,
    })

def crendencial(request):
    return render(request,'credencial.html')
#Fin de la parte de usuario xd


#Inicio de la parte de admin, debo quitar el crud se ve feo xd
@login_required
def inicio_admin(request):
    if not request.user.is_superuser:
        return redirect('login')
    else:
        return render(request,'crud-paginas/inicio_admin.html')

@login_required
def crud_usuarios(request):
    if not request.user.is_superuser:
        return redirect('login')
    else:
        user = usuario.objects.all()
        formularios = [(u, UsuarioForm(instance=u)) for u in user]

        if request.method == 'POST':
            form_type = request.POST.get('form_type')

            if form_type == 'agregar':
                formulario = UsuarioForm(request.POST, request.FILES)
                if formulario.is_valid(): 
                    nuevo_usuario = formulario.save(commit=False)
                    password = formulario.cleaned_data.get('password')
                    if password:
                        nuevo_usuario.set_password(password)
                    nuevo_usuario.is_superuser = formulario.cleaned_data.get('is_staff')
                    nuevo_usuario.save()
                    mensaje = 'Usuario creado exitosamente.'
                    return render(request, 'crud-paginas/crud.html', {
                        'user': usuario.objects.all(),
                        'form': UsuarioForm(),
                        'formulario': formularios,
                        'mensaje':mensaje
                    })
                else:
                    return render(request, 'crud-paginas/crud.html', {
                        'form': formulario,
                        'user': user,
                        'formulario': formularios
                    })
            elif form_type == 'actualizar':
                id = request.POST.get('id')
                instancia = usuario.objects.get(id=id)
                formulario = UsuarioForm(request.POST, request.FILES, instance=instancia)
                if formulario.is_valid():
                    usuario_actualizado = formulario.save(commit=False)
                    usuario_actualizado.is_staff = formulario.cleaned_data.get('is_staff')
                    usuario_actualizado.is_superuser = usuario_actualizado.is_staff 
                    usuario_actualizado.save()
                    return redirect('crud-usuarios')
                else:
                    formularios = [(u, formulario if u.id == instancia.id else UsuarioForm(instance=u)) for u in user]
                    return render(request, 'crud-paginas/crud.html', {
                        'user': user,
                        'formulario': formularios,
                        'error_id': instancia.id,
                        'form': UsuarioForm(),
                        'error_id': instancia.id 
                    })
            elif form_type == 'borrar':
                id = request.POST.get('id')
                deleted_count, _ = usuario.objects.filter(id=id).delete()
                actualizado = usuario.objects.all().order_by('id')
                mensaje = (
                    f"No se encontró ningún usuario con ID {id}."
                    if deleted_count == 0
                    else f"Usuario con ID {id} eliminado correctamente."
                )
                form = [(g, UsuarioForm(instance=g)) for g in actualizado]
                return render(request, 'crud-paginas/crud.html', {
                    'user': actualizado,
                    'formulario': form,
                    'form': UsuarioForm(),
                    'delete': mensaje
                })
        else:
            formulario = UsuarioForm()
            return render(request, 'crud-paginas/crud.html', {
                'user': usuario.objects.all(),
                'form': formulario,
                'formulario': formularios
            })

@login_required
def crud_grupo(request):
    if not request.user.is_superuser:
        return redirect('login')
    else:
        profe = profesor.objects.all()
        grupos = grupo.objects.all().order_by('grado')
        form = [(g, grupoForm(instance=g)) for g in grupos]
        if request.method == 'POST':
            form_type = request.POST.get('form_type')
            if form_type == 'agregar':
                formulario = grupoForm(request.POST)
                if formulario.is_valid():
                    formulario.save()
                    print(request.POST)
                    return redirect('crud-grupo')
                else:
                    return render(request, 'crud-paginas/crud-grupo.html', {
                        'profesor': profe,
                        'formulario': formulario,
                        'grupo': grupos,
                        'form': form
                    })
            elif form_type == 'actualizar':
                grupo_id = request.POST.get('id')
                instancia = grupo.objects.get(id=grupo_id)
                formulario = grupoForm(request.POST, instance=instancia)
                if formulario.is_valid():
                    formulario.save()
                    return redirect('crud-grupo')
                else:
                    form = [(g, formulario if g.id == instancia.id else grupoForm(instance=g)) for g in grupos]
                    return render(request, 'crud-paginas/crud-grupo.html', {
                        'profesor': profe,
                        'formulario': grupoForm(),
                        'grupo': grupos,
                        'form': form,
                        'error_id': instancia.id 
                    })
            elif form_type == 'borrar':
                id = request.POST.get('id')
                deleted_count, _ = grupo.objects.filter(id=id).delete()
                actualizado = grupo.objects.all().order_by('grado')
                form = [(g, grupoForm(instance=g)) for g in actualizado]
                mensaje = (
                    f"No se encontró ningún grupo con ID {id}."
                    if deleted_count == 0
                    else f"Grupo con ID {id} eliminado correctamente."
                )
                return render(request, 'crud-paginas/crud-grupo.html', {
                    'profesor': profe,
                    'formulario': grupoForm(),
                    'grupo': actualizado,
                    'form': form,
                    'mensaje': mensaje
                })
        else:
            formulario = grupoForm()
            return render(request, 'crud-paginas/crud-grupo.html', {
                'profesor': profe,
                'formulario': formulario,
                'grupo': grupos,
                'form': form
            })

def crud_alumno(request):
    return render(request,'crud-paginas/crud-alumnos.html')

def crud_alumno_añadir(request, pag):
    return render(request,'crud-paginas/crud-alumnos-añadir.html')

@login_required
def crud_docente(request):
    if not request.user.is_superuser:
        return redirect('login')
    else:
        docentes = profesor.objects.all().order_by('id')
        forms = [(doc, ProfesorFormulario(instance=doc)) for doc in docentes]

        if request.method == 'POST':
            form_type = request.POST.get('form_type')

            if form_type == 'actualizar':
                id = request.POST.get('id')
                instancia = profesor.objects.get(id=id)
                formulario = ProfesorFormulario(request.POST, instance=instancia)
                if formulario.is_valid():
                    formulario.save()
                    return redirect('admin-docente')
                else:
                    formularios = [
                        (u, formulario if u.id == instancia.id else ProfesorFormulario(instance=u))
                        for u in docentes
                    ]
                    return render(request, 'crud-paginas/crud-docente.html', {
                        'docentes': docentes,
                        'forms': formularios
                    })

            elif form_type == 'borrar':
                id = request.POST.get('id-docente')
                deleted_count, _ = profesor.objects.filter(id=id).delete()
                actualizado = profesor.objects.all().order_by('id')
                forms = [(g, ProfesorFormulario(instance=g)) for g in actualizado]
                mensaje = (
                    f"No se encontró ningún docente con ID {id}."
                    if deleted_count == 0
                    else f"Docente con ID {id} eliminado correctamente."
                )
                return render(request, 'crud-paginas/crud-docente.html', {
                    'docentes': actualizado,
                    'forms': forms,
                    'mensaje': mensaje
                })

    return render(request, 'crud-paginas/crud-docente.html', {
        'docentes': docentes,
        'forms': forms
    })

@login_required
def crud_docente_añadir(request, pag):
    if not request.user.is_superuser:
        return redirect('login')
    else:
        if request.method == 'POST':
            formulario = ProfesorFormulario(request.POST,request.FILES)
            if formulario.is_valid():
                formulario.save()
                mensaje = 'El docente ha sido agregado exitosamente.'
                return render(request,'crud-paginas/crud-docente-añadir.html', {
                    'pag': pag,
                    'form': ProfesorFormulario,
                    'mensaje':mensaje
                })
            else:
                return render(request,'crud-paginas/crud-docente-añadir.html', {
                    'pag': pag,
                    'form': formulario
                })
        return render(request,'crud-paginas/crud-docente-añadir.html', {
            'pag': pag,
            'form': ProfesorFormulario
            })