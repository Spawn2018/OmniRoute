# Budżet wyceny ze stawek

Pomiar Q-E2. SQL z `QUOTE_FROM_CURRENT_SQL` (SELECT bieżącej `rate_line`, bez INSERT).
Baza: `omniroute_test` po `alembic upgrade head`. Nie żywa `omniroute`. Nie k6.

**Wiersze `rate_line`:** 0  
**Werdykt:** N/A — budżet AGENTS (p95 < 300 ms przy 50k wierszy) nie obowiązuje poniżej 50k. Anti-cel PLAN: nie wołać „szybkie” przy pustej tabeli.

## EXPLAIN (`enable_seqscan = off`)

```
Limit  (cost=8.18..8.20 rows=1 width=656)
  ->  Incremental Sort  (cost=8.18..8.22 rows=2 width=656)
        Sort Key: created_at DESC, id
        Presorted Key: created_at
        ->  Index Scan Backward using ix_rate_line_current_charge_code on rate_line rl  (cost=0.15..8.17 rows=1 width=656)
              Index Cond: ((organization_id = (NULLIF(current_setting('app.current_org'::text, true), ''::text))::uuid) AND ((charge_code)::text = 'THC'::text))
```

Indeks częściowy `ix_rate_line_current_charge_code` pochodzi z migracji `010_quotation_rls`, nie z modelu ORM.
