from ninja import NinjaAPI

from apps.clientes.api import router as clientes_router

api = NinjaAPI(
    title="Sistema Créditos Leónor API",
    version="1.0.0",
)

api.add_router("/clientes/", clientes_router)


@api.get("/health", tags=["Sistema"])
def health(request):
    return {"status": "ok"}
