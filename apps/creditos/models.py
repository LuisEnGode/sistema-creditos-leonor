from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.solicitudes.models import SolicitudCredito


class Credito(models.Model):
    class Estado(models.TextChoices):
        VIGENTE = "vigente", "Vigente"
        CANCELADO = "cancelado", "Cancelado"

    solicitud = models.OneToOneField(
        SolicitudCredito,
        on_delete=models.PROTECT,
        related_name="credito",
    )

    monto_original = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    plazo_meses = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    tasa_interes_anual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )

    fecha_aprobacion = models.DateField(
        default=timezone.localdate,
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.VIGENTE,
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_aprobacion", "-id"]
        verbose_name = "crédito"
        verbose_name_plural = "créditos"

    @property
    def gasto_administrativo(self):
        """Calcula el 2 % del monto original como gasto administrativo."""
        return self.monto_original * Decimal("0.02")

    @property
    def ahorro(self):
        """Calcula el 5 % del monto original como ahorro del cliente."""
        return self.monto_original * Decimal("0.05")

    @property
    def descuentos_iniciales(self):
        """Suma el gasto administrativo y el ahorro descontados al desembolso."""
        return self.gasto_administrativo + self.ahorro

    @property
    def monto_desembolsado(self):
        """Calcula el monto entregado al cliente después de los descuentos iniciales."""
        return self.monto_original - self.descuentos_iniciales

    def clean(self):
        super().clean()

        if (
            self.solicitud_id
            and self.solicitud.estado != SolicitudCredito.Estado.APROBADA
        ):
            raise ValidationError(
                {
                    "solicitud": (
                        "Solamente una solicitud aprobada puede generar un crédito."
                    )
                }
            )

        if (
            self.solicitud_id
            and self.solicitud.tipo_credito == SolicitudCredito.TipoCredito.POR_DEFINIR
        ):
            raise ValidationError(
                {"solicitud": ("La solicitud debe tener definido el tipo de crédito.")}
            )

    def __str__(self):
        return f"Crédito #{self.pk} - {self.solicitud.cliente} - ${self.monto_original}"
