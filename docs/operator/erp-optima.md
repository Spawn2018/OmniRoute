# Konektor Optima

Na `/erp-connectors` dopisujesz **konektor Comarch Optima** tenanta: kod snake oraz kind `optima`. To nie live SOAP, nie WebAPI i nie agent on-prem.

1. Wejdź na Konektor Optima. Wpisz kod (`optima_biuro` — snake 2–32).
2. Kind zostaw `optima`. Inny brand (XL, nexo, GT) nie wejdzie — to osobne leftovery.
3. Podaj `source_ref` (`fixture://optima/…` albo `tenant:manual`).
4. „Zapisz konektor Optima”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: SOAP, WebAPI, agent, sekrety, URL, SQL `sa`, posting FS+FZ, `purchase_invoice`, KSeF, CAMT, XL, Symfonia, nexo, GT. Marża zostaje na `/charges`. Faktura sprzedaży zostaje na `/invoices`.

Nazwy w kodzie: `erp_connector` · `connector_code` · `system_kind` · `source_ref`.
