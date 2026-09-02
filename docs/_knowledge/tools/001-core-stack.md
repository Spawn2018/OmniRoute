# Tools — wzorce integracji

## Postgres — schemat
**Kiedy:** plaster z tabelą albo `resolve`  
**Skąd:** `backend/alembic/versions/` (ta tabela) + modele **tego BC**. Nie MCP (niepodłączony). Nie wszystkie modele.

## Temporal
**Kiedy:** RFQ, ekstrakcja wielokrokowa, OCR pipeline  
**Repo:** temporalio/temporal  
**Alternatywa:** Celery — odrzucona jako fundament (REWIZJA-STOSU)

## OpenFGA
**Kiedy:** authz relacyjny per tenant  
**Repo:** openfga/openfga  
**Alternatywa:** DIY RBAC — odrzucona
