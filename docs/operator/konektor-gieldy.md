# Konektor giełdy

Na `/exchange-connectors` dopisujesz **konektor giełdy** tenanta: kod snake oraz nazwana tablica P0 (`trans_eu`, `timocom`, `teleroute`, `transporeon`, `other`). To nie live HTTP, nie wystawienie frachtu i nie portal klienta.

1. Wejdź na Konektor giełdy. Wpisz kod (`trans_eu_desk` — snake 2–32).
2. Wybierz tablicę z listy allowlisty HITL.
3. Podaj `source_ref` (`fixture://portal/…` albo `tenant:manual`).
4. „Zapisz konektor giełdy”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: live Trans.eu / TIMOCOM / Transporeon, auto-post, scrape, sekrety, URL, OAuth2, portal klienta/przewoźnika, apka, konsument outboxa. Marża zostaje na `/charges`. Sesja zostaje na `/session`.

Nazwy w kodzie: `exchange_connector` · `connector_code` · `system_kind` · `source_ref`.
