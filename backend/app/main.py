from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.database import probe_database
from app.core.request_id import RequestIdMiddleware
from app.domain.errors import (
    BulkAcceptConfidenceBelow,
    ChannelQuoteConflict,
    CloneCarryMarkConflict,
    ConsignmentFtlLimit,
    ContainerReeferRequired,
    DomainError,
    DraftNotPending,
    ExtractionCandidatesNotEditable,
    MarginFloorBreach,
    PalletLedgerConflict,
    PalletSynchroMarkConflict,
    PartyConflict,
    PermissionDenied,
    ProductTicketOwnerRequired,
    QuotationNamedPlaceRequired,
    ResourceNotFound,
    RoutingGuideOffGuide,
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


@app.exception_handler(DraftNotPending)
async def draft_not_pending_handler(_request: Request, exc: DraftNotPending) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(BulkAcceptConfidenceBelow)
async def bulk_accept_confidence_below_handler(
    _request: Request,
    exc: BulkAcceptConfidenceBelow,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(ExtractionCandidatesNotEditable)
async def extraction_candidates_not_editable_handler(
    _request: Request,
    exc: ExtractionCandidatesNotEditable,
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(ChannelQuoteConflict)
async def channel_quote_conflict_handler(
    _request: Request,
    exc: ChannelQuoteConflict,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(MarginFloorBreach)
async def margin_floor_breach_handler(
    _request: Request,
    exc: MarginFloorBreach,
) -> JSONResponse:
    body: dict[str, object] = {"detail": str(exc)}
    if exc.decision_id is not None:
        body["decision_id"] = str(exc.decision_id)
    return JSONResponse(status_code=409, content=body)


@app.exception_handler(ProductTicketOwnerRequired)
async def product_ticket_owner_required_handler(
    _request: Request,
    exc: ProductTicketOwnerRequired,
) -> JSONResponse:
    body: dict[str, object] = {"detail": str(exc)}
    if exc.decision_id is not None:
        body["decision_id"] = str(exc.decision_id)
    return JSONResponse(status_code=409, content=body)


@app.exception_handler(ConsignmentFtlLimit)
async def consignment_ftl_limit_handler(
    _request: Request,
    exc: ConsignmentFtlLimit,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(ContainerReeferRequired)
async def container_reefer_required_handler(
    _request: Request,
    exc: ContainerReeferRequired,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(RoutingGuideOffGuide)
async def routing_guide_off_guide_handler(
    _request: Request,
    exc: RoutingGuideOffGuide,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(QuotationNamedPlaceRequired)
async def quotation_named_place_handler(
    _request: Request,
    exc: QuotationNamedPlaceRequired,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(PartyConflict)
async def party_conflict_handler(_request: Request, exc: PartyConflict) -> JSONResponse:
    existing = exc.existing_party_id
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
            "existing_party_id": str(existing),
            "href": f"/parties/{existing}",
        },
    )


@app.exception_handler(PalletLedgerConflict)
async def pallet_ledger_conflict_handler(
    _request: Request,
    exc: PalletLedgerConflict,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(PalletSynchroMarkConflict)
async def pallet_synchro_mark_conflict_handler(
    _request: Request,
    exc: PalletSynchroMarkConflict,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(CloneCarryMarkConflict)
async def clone_carry_mark_conflict_handler(
    _request: Request,
    exc: CloneCarryMarkConflict,
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


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
