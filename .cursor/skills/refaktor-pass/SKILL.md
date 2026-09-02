---
name: refaktor-pass
description: Cotygodniowy slot refaktoryzacji z metrykami
---

# Refaktor pass

1. Uruchom: `just complexity`, `just dup`, `just dead`, `python scripts/quality/refactor_ratio.py`
2. Cel: stosunek przeniesionego/dodanego ≥ 10% w oknie tygodnia; nota 4,4 na Grupie A ([PLAN-REALIZACJA.md](../../docs/PLAN-REALIZACJA.md) § Cel jakości)
3. Trzecie powtórzenie → wyodrębnij helper. Drugie nie. Tablice-odczyty nie idą na 5,0.
4. Max 3 zmiany na sesję. Po każdej: `just test`.
5. NIE zmieniaj zachowania. Testy bez modyfikacji.
