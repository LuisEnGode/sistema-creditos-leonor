from ninja import Router, Schema

from apps.clientes.models import Cliente

router = Router(tags=["Clientes"])


class ClienteOut(Schema):
    id: int
    tipo_identificacion: str
    identificacion: str
    nombres: str
    apellidos: str
    telefono: str
    correo: str
    es_socio: bool
    activo: bool


@router.get("/", response=list[ClienteOut])
def listar_clientes(request):
    return Cliente.objects.all()


@router.get("/{cliente_id}", response=ClienteOut)
def obtener_cliente(request, cliente_id: int):
    return Cliente.objects.get(id=cliente_id)
