from django.db import models


class Cliente(models.Model):
    TIPO_IDENTIFICACION_CHOICES = [
        ("cedula", "Cédula"),
        ("ruc", "RUC"),
        ("pasaporte", "Pasaporte"),
    ]

    tipo_identificacion = models.CharField(
        max_length=20,
        choices=TIPO_IDENTIFICACION_CHOICES,
        default="cedula",
    )
    identificacion = models.CharField(
        max_length=20,
        unique=True,
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    telefono = models.CharField(
        max_length=30,
        blank=True,
    )
    correo = models.EmailField(
        blank=True,
    )
    direccion = models.TextField(
        blank=True,
    )

    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.apellidos} {self.nombres} - {self.identificacion}"
