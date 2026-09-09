# Schemat monitoringu

Na `/monitoring-schemes` zapisujesz **kod schematu monitoringu** tenanta (np. `sent`, `ekaer`). To nie zgłoszenie do PUESC i nie wymyślony SENT w kraju bez urzędu.

1. Wejdź na Schemat monitoringu. Wpisz kod snake (2–32 znaki).
2. „Zapisz schemat monitoringu” z `source_ref` (`fixture://monitoring-scheme/…` albo `tenant:manual`).

Czego tu nie ma: XML SENT, SENT-GEO, live HTTP, `shipment_monitoring_filing`, mapa „SENT-Europa”, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Zgłoszenie zostaje leftover C1.

Nazwy w kodzie: `monitoring_scheme` · `scheme_code` · `source_ref`.
