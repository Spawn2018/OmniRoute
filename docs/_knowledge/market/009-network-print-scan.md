# Wydruki sieci drobnicowych + skan zwrotny

**Kiedy:** Plan D9 / D2. Szczegóły: `docs/analysis/benchmark-tms-2026.md` §13n.

## Druk

Szablon = dane (nie T-SQL SPEED). Na każdym arkuszu: `shipment_ref` + QR.
Wymóg sieci (`network_print_requirement`) blokuje wyjazd jak C8.
CMR groupage = osobny CMR na grupę dostaw (wzorzec Qargo).
Etykieta obcej sieci tylko z ich API (D8), nie generator-udawacz.

## Skan

Nasz QR odczytany → `shipment_document` od razu (`scan://`).
Zła trasa/status → odrzut.
Brak kodu → drabina SQL + HITL (jak §13m).
Diff CMR vs zlecenie = X6, nie cichy overwrite.
