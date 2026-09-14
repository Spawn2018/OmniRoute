# BC quality_descent_mark (AI8.2 leftover)

HITL katalog powodu zejścia jakości per tenant. mark_code +
descent_kind mae|crps|brier|manual|other + source_ref.
Nie silnik auto-zejścia. Nie L3 write.

## Dozwolone zależności
- `app.models.quality_descent_mark`
- `app.repositories.quality_descent_marks`
- `app.domain`

## Zakaz
- import innych BC services (l3_gate_marks, autonomy_levels, interval_scores, charges)
- zapis `l3_gate_mark` / `autonomy_level` / `interval_score` / `charge`
- silnik auto-zejścia · MAE/CRPS SQL · scoring osoby · L3 write
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
