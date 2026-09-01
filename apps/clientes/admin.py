from django.contrib import admin

from apps.clientes.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "identificacion",
        "apellidos",
        "nombres",
        "telefono",
        "es_socio",
        "activo",
    )
    search_fields = (
        "identificacion",
        "nombres",
        "apellidos",
        "telefono",
        "correo",
    )
    list_filter = ("es_socio", "activo", "tipo_identificacion")
