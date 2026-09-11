from collections.abc import Collection, Mapping

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


def assert_asn_labels_on_routing_guide(
    *,
    guide_code: str | None,
    enforcement_kinds: Collection[str],
    match_kinds: Collection[str],
    plant_label: str | None,
    carrier_label: str | None,
    guide_lane_by_code: Mapping[str, str | None],
    guide_mode_by_code: Mapping[str, str | None],
) -> None:
    """Po guide_code: opcjonalne porównanie etykiet wg katalogu match (289.0)."""
    if "block_409" not in enforcement_kinds:
        return
    if guide_code is None:
        return
    if "lane_label" in match_kinds:
        expected = guide_lane_by_code.get(guide_code)
        if expected is None or not str(expected).strip():
            raise RoutingGuideOffGuide(
                "przewodnik bez lane_label — matching lane_label"
            )
        if plant_label is None or _fold(plant_label) != _fold(str(expected)):
            raise RoutingGuideOffGuide(
                "plant_label poza lane_label przewodnika"
            )
    if "mode_label" in match_kinds:
        expected = guide_mode_by_code.get(guide_code)
        if expected is None or not str(expected).strip():
            raise RoutingGuideOffGuide(
                "przewodnik bez mode_label — matching mode_label"
            )
        if carrier_label is None or _fold(carrier_label) != _fold(str(expected)):
            raise RoutingGuideOffGuide(
                "carrier_label poza mode_label przewodnika"
            )


def _fold(raw: str) -> str:
    return raw.strip().casefold()
