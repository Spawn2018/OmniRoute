# prediction_ledger (B0b / V1)

Ledger predykcji per tenant. Append-only INSERT. Przedział N7 + CRPS/MAE jako dane. Nie silnik. Nie scoring osoby.

- RLS FORCE. OpenFGA `can_manage_prediction_ledgers` = member
- `prediction_kind`: `eta` / `transit` / `disrupt`
- `horizon_code`: `h1h` / `h6h` / `h24h` / `h7d`
- `interval_low` / `interval_high` / `crps` / `mae`: `Numeric(14,4)`, nie float
- Brak CRPS → 400. Unique `(organization_id, source_ref)`
- Job: `/prediction-ledgers`

Delta: [193.0](../deltas/archived/193.0-prediction-ledger.md).
