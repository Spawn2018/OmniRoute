# Konektor SAP/Oracle (CT6)

Ekran `/sap-connectors` zapisuje konektor jako dane: kod snake, system `sap` albo `oracle`, oraz `source_ref`.

To katalog HITL jak Optima (F9). Nie woła SOAP/RFC. Nie trzyma sekretów ani URL. Nie liczy kwot.

Źródło: `tenant:manual` albo `fixture://sap-connector/…`. Zły kod albo system → błąd walidacji po polsku.

Czego tu nie ma: live SAP, SQL do MSSQL/Oracle klienta, Optima (to `/erp-connectors`), mapa. Marża zostaje na `/charges`.
