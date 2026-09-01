from datetime import date
from decimal import Decimal

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from apps.solicitudes.models import SolicitudCredito

router = Router(tags=["Solicitudes"])


class SolicitudCreditoOut(Schema):
    id: int
    cliente_id: int
    monto_solicitado: Decimal
    plazo_meses: int
    fecha_solicitud: date
    estado: str
    observaciones: str


@router.get("/", response=list[SolicitudCreditoOut])
def listar_solicitudes(request):
    return SolicitudCredito.objects.select_related("cliente").all()


@router.get("/{solicitud_id}", response=SolicitudCreditoOut)
def obtener_solicitud(request, solicitud_id: int):
    return get_object_or_404(
        SolicitudCredito.objects.select_related("cliente"),
        id=solicitud_id,
    )
