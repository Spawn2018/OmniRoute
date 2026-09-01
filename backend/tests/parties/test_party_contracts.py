from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_SERVICES = _ROOT / "backend" / "app" / "services"
_REPOS = _ROOT / "backend" / "app" / "repositories"


def test_importlinter_lists_parties_as_an_independent_bounded_context() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.parties" in independence


def test_importlinter_forbids_extraction_from_knowing_parties() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    extraction = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.parties" in extraction
    assert "app.repositories.parties" in extraction
    assert "app.models.party" in extraction


def test_parties_service_package_exists() -> None:
    assert (_SERVICES / "parties" / "party_service.py").is_file()
    assert (_SERVICES / "parties" / "AGENTS.md").is_file()
    assert (_REPOS / "parties" / "party_repository.py").is_file()


def test_pricing_modules_do_not_import_party_charge_override() -> None:
    assert (_SERVICES / "parties").is_dir()
    for bounded in ("quotations", "charges", "rate_lines"):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "party_charge_override" not in text
            assert "app.services.parties" not in text
        for path in (_REPOS / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "party_charge_override" not in text
            assert "app.repositories.parties" not in text


def test_extraction_service_does_not_import_parties() -> None:
    assert (_SERVICES / "parties").is_dir()
    source = (_SERVICES / "extraction" / "extraction_service.py").read_text(encoding="utf-8")
    assert "app.services.parties" not in source
    assert "app.models.party" not in source


def test_geography_stores_operator_party_id_without_importing_parties() -> None:
    from app.models.terminal import Terminal

    assert "operator_party_id" in Terminal.__table__.c
    for path in (_SERVICES / "geography").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "app.services.parties" not in text
        assert "app.repositories.parties" not in text


def test_lookup_lives_in_parties_service_with_timeout_and_without_gus_secrets() -> None:
    lookup = _SERVICES / "parties" / "lookup.py"
    assert lookup.is_file()
    source = lookup.read_text(encoding="utf-8")
    assert "timeout" in source
    lowered = source.lower()
    assert "gus_api_key =" not in lowered
    assert 'password = "' not in lowered
    assert "regon_key" not in lowered


def test_router_mounts_parties_api() -> None:
    source = (_ROOT / "backend" / "app" / "api" / "router.py").read_text(encoding="utf-8")
    assert "parties" in source
    assert "include_router(parties.router)" in source
