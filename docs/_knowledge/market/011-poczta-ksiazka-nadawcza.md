# Książka nadawcza Poczty Polskiej

**Kiedy:** Plan F11. Szczegóły: `docs/analysis/benchmark-tms-2026.md` §13p.

## API (oficjalne)

- EN SOAP: `e-nadawca.api.poczta-polska.pl/websrv/` — `addShipment`, `sendEnvelope`, `getOutboxBook`, `getEPOStatus`.
- Śledzenie REST: `checkmailex` / `checkmailcollectionex`. Zdarzenie `P_D` = doręczono; `P_UKEPO` = podpis dostępny.
- Imię odbiorcy: `osobaOdbierajaca` + `podmiotDoreczenia` w EPO, nie w REST.
- Umowa EPO + usługa na przesyłce. Papierowe ZPO = skan HITL.

## Omni

`sales_invoice.delivery_channel`: `electronic` | `paper_post` (domyślnie z `party`).
Papier = Poczta Polska, kolejka nadania, nie „wysłana” bez `postal_dispatch`.
Nie wyłącza KSeF. Klucz wiersza = `numer_nadania`.
Wejście numeru: (1) zwrotka EN, (2) skaner USB/HID albo kamera, (3) wklejenie z checksum.
API śledzi po numerze. Nie scrapować. Nie logować podpisu.
