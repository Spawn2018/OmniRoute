# Dokument kontrahenta

Na `/party-documents` zapisujesz **rodzaj dokumentu** przy istniejącym kontrahencie (np. `ocp`, `ocs`). To nie blokada 409 na zleceniu i nie skan z extractu.

1. Wejdź na Dokument kontrahenta. Wklej `party_id` kontrahenta tenanta.
2. Wpisz kind snake (2–32 znaki).
3. „Zapisz dokument kontrahenta” z `source_ref` (`fixture://party-document/…` albo `tenant:manual`).

Czego tu nie ma: 409 na `POST shipment`, `relation_document_requirement`, daty ważności, składka, bajty, HITL extract, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Kontrahent zostaje na `/parties`. Licencja KREPTD zostaje na `/kreptd-licences`.

Nazwy w kodzie: `party_document` · `party_id` · `document_kind` · `source_ref`.
