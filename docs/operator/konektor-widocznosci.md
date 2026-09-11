# Konektor widoczności

Na `/visibility-connectors` dopisujesz **konektor widoczności** tenanta: kod snake oraz kind
`p44`, `fourkites` albo `shippeo`. To nie live HTTP do vendora, nie mapa i nie tablica ETA.

1. Wejdź na Konektor widoczności. Wpisz kod (`p44_desk_pl` — snake 2–32).
2. Wybierz vendor: `p44`, `fourkites` albo `shippeo`. Token marki ≠ live track.
3. Podaj `source_ref` (`fixture://visibility/…` albo `tenant:manual`).
4. „Zapisz konektor widoczności”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: live p44 / FourKites / Shippeo, scrape ocean, AIS, sekrety, URL, mapa, live ETA.
Marża zostaje na `/charges`. Tracking zlecenia zostaje na `/tracking`.

Nazwy w kodzie: `visibility_connector` · `connector_code` · `system_kind` · `source_ref`.
