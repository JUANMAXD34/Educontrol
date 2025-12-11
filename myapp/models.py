from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import calendar

# Create your models here.
#

from django.db import models

class profesor(models.Model):
    nombre_profesor = models.CharField(max_length=200)
    apellidos_profesor = models.CharField(max_length=200)
    curp = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    comprobante_domicilio = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    cedula_profesional = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    identificacion = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    telefono = models.CharField(max_length=15)
    edad = models.PositiveIntegerField()
    correo_electronico = models.EmailField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to='fotos/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])],default='fotos/default.jpg')

    def clean(self):
        existe = profesor.objects.filter(
            nombre_profesor = self.nombre_profesor,
            telefono = self.telefono,
            correo_electronico = self.correo_electronico
        ).exclude(pk=self.pk).exists()

        if existe:
            raise ValidationError("El profesor ya se encuentra registrado")

    def __str__(self):
        return f'{self.nombre_profesor} {self.apellidos_profesor}'


class grupo(models.Model):
    nombre_grupo = models.CharField(max_length=2)
    grado = models.PositiveSmallIntegerField(choices=[(1, '1°'), (2, '2°'), (3, '3°')])
    turno = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')])
    profesor = models.ForeignKey(profesor, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_grupo} - {self.get_grado_display()} - {self.turno}"

class alumno(models.Model):
    nombre_alumno = models.CharField(max_length=100)
    apellidos_alumno = models.CharField(max_length=100)
    curp = models.CharField(max_length=18, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to="alumnos/fotos/", blank=True, null=True)
    acta_nacimiento = models.FileField(upload_to="alumnos/actas/", blank=True, null=True)
    comprobante_domicilio = models.FileField(upload_to="alumnos/comprobantes/", blank=True, null=True)
    tutores = models.ManyToManyField("Tutor", related_name="alumnos")
    grupo = models.ForeignKey(grupo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre_alumno} {self.apellidos_alumno}"

class tutor(models.Model):
    RELACION_CHOICES = [
        ('PADRE', 'Padre'),
        ('MADRE', 'Madre'),
        ('ABUELO', 'Abuelo/Abuela'),
        ('TUTOR', 'Tutor Legal'),
        ('OTRO', 'Otro'),
    ]

    nombre_tutor = models.CharField(max_length=100)
    apellidos_tutor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    relacion = models.CharField(max_length=10, choices=RELACION_CHOICES)
    foto = models.ImageField(upload_to="tutores/fotos/", blank=True, null=True)
    ine = models.FileField(upload_to="tutores/ine/", blank=True, null=True)
    comprobante_domicilio = models.FileField(upload_to="tutores/comprobantes/", blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre_tutor', 'apellidos_tutor', 'telefono', 'email'],
                name='unique_tutor'
            )
        ]

    def __str__(self):
        return f"{self.nombre_tutor} ({self.relacion})"


class colegiatura(models.Model):
    METODO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
    ]

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('VENCIDO', 'Vencido'),
    ]

    alumno = models.ForeignKey(alumno, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    fecha_pago = models.DateField()
    mes = models.CharField(max_length=20)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default='EFECTIVO')
    referencia = models.CharField(max_length=50, default='Pago de colegiatura mensual')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mes} - {self.alumno} ({self.estado})"

@receiver(post_save, sender=colegiatura)
def generar_siguiente_mes(sender, instance, created, **kwargs):
    if instance.estado == "PAGADO" or instance.estado == "VENCIDO":
        fecha_actual = instance.fecha_pago
        siguiente_mes = fecha_actual.month + 1
        siguiente_anio = fecha_actual.year

        if siguiente_mes > 12:
            siguiente_mes = 1
            siguiente_anio += 1

        MESES_ES = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
        }

        mes_str = f"{MESES_ES[siguiente_mes]} {siguiente_anio}"

        pagos_en_anio = colegiatura.objects.filter(
            alumno=instance.alumno,
            fecha_pago__year=siguiente_anio
        ).count()

        if pagos_en_anio >= 12:
            return  

        existe = colegiatura.objects.filter(
            alumno=instance.alumno,
            mes=mes_str
        ).exists()

        if not existe:
            colegiatura.objects.create(
                alumno=instance.alumno,
                monto=instance.monto,
                fecha_pago=fecha_actual + timedelta(days=30),
                mes=mes_str,
                metodo="EFECTIVO",
                referencia="Pago de Colegiatura",
                estado="PENDIENTE"
            )


class usuario(AbstractUser):
    foto = models.ImageField(upload_to='fotos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    telefono = models.CharField(max_length=15, default=123456789012345)
    
