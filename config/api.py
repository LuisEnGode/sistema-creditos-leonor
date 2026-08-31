from ninja import NinjaAPI

api = NinjaAPI(
    title="Sistema Créditos Leónor API",
    version="1.0.0",
)


@api.get("/health", tags=["Sistema"])
def health(request):
    return {"status": "ok"}
