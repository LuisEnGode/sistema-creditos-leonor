from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.clientes.models import Cliente


class SolicitudCredito(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PENDIENTE = "pendiente", "Pendiente"
        APROBADA = "aprobada", "Aprobada"
        RECHAZADA = "rechazada", "Rechazada"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="solicitudes_credito",
    )
    monto_solicitado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    plazo_meses = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    fecha_solicitud = models.DateField(
        default=timezone.localdate,
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
    )
    observaciones = models.TextField(
        blank=True,
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_solicitud", "-id"]
        verbose_name = "solicitud de crédito"
        verbose_name_plural = "solicitudes de crédito"

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.cliente} - ${self.monto_solicitado}"
