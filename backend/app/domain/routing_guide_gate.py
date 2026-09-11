from collections.abc import Collection

from app.domain.errors import RoutingGuideOffGuide


def assert_asn_on_routing_guide(
    *,
    guide_code: str | None,
    enforcement_kinds: Collection[str],
    known_guide_codes: Collection[str],
) -> None:
    """Gdy tenant ma block_409 — ASN wymaga znanego guide_code. record_only nie blokuje."""
    if "block_409" not in enforcement_kinds:
        return
    if guide_code is None:
        raise RoutingGuideOffGuide(
            "brak guide_code — egzekucja przewodnika block_409"
        )
    if guide_code not in known_guide_codes:
        raise RoutingGuideOffGuide(
            "guide_code poza katalogiem przewodnika routingu"
        )
