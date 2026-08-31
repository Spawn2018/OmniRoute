from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.domain.errors import DomainError, PermissionDenied, TenantContextMissing

app = FastAPI(title="OmniRoute", version="0.1.0")
app.include_router(api_router)


@app.exception_handler(PermissionDenied)
async def permission_denied_handler(_request: Request, exc: PermissionDenied) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": str(exc) or "Brak uprawnień"})


@app.exception_handler(TenantContextMissing)
async def tenant_missing_handler(_request: Request, exc: TenantContextMissing) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
