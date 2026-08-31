# Tools — wzorce integracji

## Postgres MCP
**Kiedy:** podgląd schematu, EXPLAIN  
**Repo:** mcp-server-postgres  
**Alternatywa:** czytanie wszystkich modeli SQLAlchemy — odrzucona (context bloat)

## Temporal
**Kiedy:** RFQ, ekstrakcja wielokrokowa, OCR pipeline  
**Repo:** temporalio/temporal  
**Alternatywa:** Celery — odrzucona jako fundament (REWIZJA-STOSU)

## OpenFGA
**Kiedy:** authz relacyjny per tenant  
**Repo:** openfga/openfga  
**Alternatywa:** DIY RBAC — odrzucona
