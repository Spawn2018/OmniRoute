from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.database import probe_database
from app.core.request_id import RequestIdMiddleware
from app.domain.errors import (
    DomainError,
    PermissionDenied,
    ResourceNotFound,
    TenantContextMissing,
    Unauthenticated,
)

app = FastAPI(
    title="OmniRoute",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.add_middleware(RequestIdMiddleware)
app.include_router(api_router)


@app.exception_handler(Unauthenticated)
async def unauthenticated_handler(_request: Request, exc: Unauthenticated) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc) or "Brak tokenu sesji"},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(PermissionDenied)
async def permission_denied_handler(_request: Request, exc: PermissionDenied) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": str(exc) or "Brak uprawnień"})


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(_request: Request, exc: ResourceNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(TenantContextMissing)
async def tenant_missing_handler(_request: Request, exc: TenantContextMissing) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> JSONResponse:
    if await probe_database():
        return JSONResponse({"status": "ok"})
    return JSONResponse({"status": "not_ready"}, status_code=503)
