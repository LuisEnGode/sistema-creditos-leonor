from django.contrib import admin

from apps.solicitudes.models import SolicitudCredito


@admin.register(SolicitudCredito)
class SolicitudCreditoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "monto_solicitado",
        "plazo_meses",
        "fecha_solicitud",
        "estado",
    )
    search_fields = (
        "cliente__identificacion",
        "cliente__nombres",
        "cliente__apellidos",
    )
    list_filter = (
        "estado",
        "fecha_solicitud",
    )
    autocomplete_fields = ("cliente",)
    date_hierarchy = "fecha_solicitud"
    ordering = ("-fecha_solicitud", "-id")
