from django import forms
import re
from .models import usuario, grupo, profesor, alumno, tutor, colegiatura
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime

class CreateNewTask(forms.Form):
    Title = forms.CharField(label='Titulo de la Tarea', max_length=200)
    Description = forms.CharField(widget=forms.Textarea, label='Descripcion de la tarea',required=False)

class CreateNewClassmate(forms.Form):
    nombre = forms.CharField(max_length=200, label='Nombre(s)', required=True)
    apellidos = forms.CharField(max_length=200, label='Apellidos')
    grupo = forms.ChoiceField(label='Grupo')

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = usuario
        fields = ['username', 'email', 'telefono', 'foto', 'is_staff','password']
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise forms.ValidationError("El usuario debe tener al menos 4 caracteres.")
        if usuario.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("Este usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and usuario.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if len(telefono) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")
        return telefono

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        archivo = self.files.get('foto') 
        if archivo:
            if archivo.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                raise forms.ValidationError("Solo se permiten imágenes PNG, JPG o JPEG.")
            if archivo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("La imagen no debe superar los 2MB.")
        return foto
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            return self.instance.password
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos un número.')
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('La contraseña debe tener al menos una letra.')
        if not any(char in "!@#$^&*()-_=+[]{}|;:,.<>?/" for char in password):
            raise forms.ValidationError('La contraseña debe tener al menos un carácter especial.')
        return password
    
class grupoForm(ModelForm):
    class Meta:
        model = grupo
        fields = ['nombre_grupo','grado','turno','profesor']
        
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre_grupo')
        turno = cleaned_data.get('turno')
        grado = cleaned_data.get('grado')
        profesor = cleaned_data.get('profesor')

        if nombre and turno:
            existe = grupo.objects.filter(nombre_grupo=nombre, turno=turno, grado = grado).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError('Ya existe este grupo.')
        
        if nombre and grado:
            grado_string = str(grado)
            grado_numero = ''.join(filter(str.isdigit, grado_string))
            nombre_grado = nombre.strip()[0]

            if grado_numero and nombre_grado != grado_numero:
                raise forms.ValidationError(
                    f"El nombre del grupo {nombre} no coincide con el grado seleccionado."
                )

        if profesor and turno:
            existente = grupo.objects.filter(profesor=profesor, turno=turno).exclude(pk=self.instance.pk).exists()
            if existente:
                raise forms.ValidationError("Este profesor ya tiene un grupo asignado en ese turno.")
            
        

    def __init__(self, *args, **kwargs):
        super(grupoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

class profesorForm(forms.ModelForm):
    nombre_profesor = forms.ModelChoiceField(
        queryset=profesor.objects.all(),
        label="Profesor",
        widget=forms.Select(attrs={'class': 'list'}),
    )
    class Meta:
        model = profesor
        fields = ['nombre_profesor']

class UserForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Debe ingresar un usuario válido.')
        if len(username) < 4:
            raise forms.ValidationError('El Usuario debe ser mayor a 4 caracteres.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Debe ingresar una contraseña.')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Usuario o contraseña incorrectos.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

class AlumnoForm(forms.ModelForm):
    nombre_alumno = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$', 'El nombre solo puede contener letras y espacios.')],
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan'})
    )
    apellidos_alumno = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$', 'Los apellidos solo pueden contener letras y espacios.')],
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Pérez Gómez'})
    )
    curp = forms.CharField(
        max_length=18,
        min_length=18,
        validators=[RegexValidator(r'^[A-Z0-9]{18}$', 'La CURP debe contener exactamente 18 caracteres alfanuméricos en mayúsculas.')],
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: ABCD123456HDFRRR09'})
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'invalid': 'Ingrese una fecha válida en formato AAAA-MM-DD.'}
    )
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Ejemplo: Calle Falsa 123, Colonia Centro'}),
        max_length=300
    )
    acta_nacimiento = forms.FileField(widget=forms.FileInput(attrs={'accept': '.pdf'}))
    comprobante_domicilio = forms.FileField(widget=forms.FileInput(attrs={'accept': '.pdf'}))

    class Meta:
        model = alumno
        fields = '__all__'

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha and fecha > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre_alumno")
        apellidos = cleaned_data.get("apellidos_alumno")
        curp = cleaned_data.get("curp")

        if nombre and apellidos and curp:
            if alumno.objects.filter(
                nombre_alumno=nombre,
                apellidos_alumno=apellidos,
                curp=curp
            ).exists():
                raise forms.ValidationError(
                    "Ya existe un alumno registrado con el mismo nombre, apellidos y CURP."
                )
        return cleaned_data



class TutorForm(forms.ModelForm):
    nombre_tutor = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$', 'El nombre solo puede contener letras y espacios.')],
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan'})
    )
    apellidos_tutor = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$', 'Los apellidos solo pueden contener letras y espacios.')],
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Pérez Gómez'})
    )
    telefono = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^[0-9]+$', 'El teléfono solo puede contener números.')],
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 5512345678'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Ejemplo: correo@dominio.com'})
    )

    class Meta:
        model = tutor
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre_tutor")
        apellidos = cleaned_data.get("apellidos_tutor")
        telefono = cleaned_data.get("telefono")
        email = cleaned_data.get("email")

        if nombre and apellidos and telefono and email:
            if tutor.objects.filter(
                nombre_tutor=nombre,
                apellidos_tutor=apellidos,
                telefono=telefono,
                email=email
            ).exists():
                raise forms.ValidationError(
                    "Ya existe un tutor registrado con el mismo nombre, apellidos, teléfono y correo."
                )
        return cleaned_data





class ProfesorFormulario(forms.ModelForm):
    nombre_profesor = forms.CharField(max_length=200, validators=[RegexValidator(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$', 'El nombre solo puede contener letras y espacios.')],widget=forms.TextInput(attrs={'placeholder':'Ejemplo: Juan Carlos'}))
    apellidos_profesor = forms.CharField(max_length=200,validators=[RegexValidator(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$', 'Los apellidos solo pueden contener letras y espacios.')],widget=forms.TextInput(attrs={'placeholder':'Ejemplo: Pérez Gómez'}))
    telefono = forms.CharField(max_length=15, validators=[RegexValidator(r'^\d{10,15}$', 'El teléfono debe contener entre 10 y 15 dígitos.')], widget=forms.TextInput(attrs={'placeholder':'Ejemplo: 5512345678'}))
    correo_electronico = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ejemplo: juan.perez@gmail.com'}))
    curp = forms.FileField(widget=forms.FileInput(attrs={'accept':'.pdf'}))
    comprobante_domicilio = forms.FileField(widget=forms.FileInput(attrs={'accept':'.pdf'}))
    cedula_profesional = forms.FileField(widget=forms.FileInput(attrs={'accept':'.pdf'}))
    identificacion = forms.FileField(widget=forms.FileInput(attrs={'accept':'.pdf'}))
    edad = forms.IntegerField(min_value=18, max_value=100,widget=forms.NumberInput(attrs={'placeholder': 'Ejemplo: 19'}))

    class Meta:
        model = profesor
        fields = '__all__'

    def clean_curp(self):
        archivo = self.cleaned_data.get('curp')
        if archivo and not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("El archivo de CURP debe estar en formato PDF.")
        return archivo

    def clean_comprobante_domicilio(self):
        archivo = self.cleaned_data.get('comprobante_domicilio')
        if archivo and not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("El comprobante de domicilio debe estar en formato PDF.")
        return archivo

    def clean_cedula_profesional(self):
        archivo = self.cleaned_data.get('cedula_profesional')
        if archivo and not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("La cédula profesional debe estar en formato PDF.")
        return archivo

    def clean_identificacion(self):
        archivo = self.cleaned_data.get('identificacion')
        if archivo and not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("La identificación debe estar en formato PDF.")
        return archivo

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto and not foto.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError("La foto debe estar en formato JPG, JPEG o PNG.")
        return foto

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if correo and not re.match(patron, correo):
            raise forms.ValidationError("Ingresa un correo válido en formato estándar.")
        qs = profesor.objects.filter(correo_electronico=correo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre_profesor")
        apellidos = cleaned_data.get("apellidos_profesor")
        edad = cleaned_data.get("edad")
        telefono = cleaned_data.get("telefono")
        correo = cleaned_data.get("correo_electronico")
        if nombre and apellidos and edad and telefono and correo:
            qs = profesor.objects.filter(
                nombre_profesor=nombre,
                apellidos_profesor=apellidos,
                edad=edad,
                telefono=telefono,
                correo_electronico=correo
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe este registro.")
        return cleaned_data

class PagoForm(forms.ModelForm):
    monto = forms.IntegerField(
        min_value=2000,
        max_value=2000,
        widget=forms.NumberInput(attrs={'class': 'input campos', 'placeholder': 'Monto'})
    )

    class Meta:
        model = colegiatura
        fields = ['alumno', 'monto', 'fecha_pago', 'metodo', 'referencia', 'estado']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'input campos'}),
            'fecha_pago': forms.DateInput(attrs={'class': 'input campos', 'type': 'date'}),
            'metodo': forms.Select(attrs={'class': 'input campos'}),
            'referencia': forms.TextInput(attrs={'class': 'input campos', 'placeholder': 'Referencia'}),
            'estado': forms.Select(attrs={'class': 'input campos'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get("alumno")
        fecha_pago = cleaned_data.get("fecha_pago")

        if alumno and fecha_pago:
            MESES_ES = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
            }
            mes_str = f"{MESES_ES[fecha_pago.month]} {fecha_pago.year}"

            existe = colegiatura.objects.filter(alumno=alumno, mes=mes_str).exists()
            if existe:
                raise forms.ValidationError(f"Ya existe un pago registrado para {mes_str} de este alumno.")
            pagos_en_anio = colegiatura.objects.filter(
                alumno=alumno,
                fecha_pago__year=fecha_pago.year
            ).count()
            if pagos_en_anio >= 12:
                raise forms.ValidationError(
                    f"El alumno ya tiene registrados los 12 pagos de colegiatura para {fecha_pago.year}."
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        MESES_ES = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
        }
        instance.mes = f"{MESES_ES[instance.fecha_pago.month]} {instance.fecha_pago.year}"
        if commit:
            instance.save()
        return instance


class PagoActualizar(forms.ModelForm):
    class Meta:
        model = colegiatura
        fields = ['alumno', 'monto', 'fecha_pago', 'metodo', 'referencia', 'estado']
        
    def __init__(self, *args, **kwargs):
        super(PagoActualizar, self).__init__(*args, **kwargs)
        self.fields['alumno'].disabled = True
        self.fields['monto'].disabled = True
        self.fields['fecha_pago'].disabled = True

    def clean_referencia(self):
        ref = self.cleaned_data.get('referencia')
        if not ref or not ref.strip():
            raise forms.ValidationError('La referencia no puede estar vacía.')
        if len(ref) < 5:
            raise forms.ValidationError('La referencia debe tener al menos 5 caracteres.')
        return ref

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if self.instance.estado == "PAGADO" and estado == "PENDIENTE":
            raise forms.ValidationError("No se puede revertir un pago ya marcado como PAGADO.")
        return estado
