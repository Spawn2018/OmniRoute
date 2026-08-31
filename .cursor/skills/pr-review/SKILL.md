---
name: pr-review
description: Review 4-pass przed merge — artefakty, nie dyskusja agent↔agent
---

# PR Review (software factory)

Agenci nie „rozmawiają”. Wymieniają **artefakty**. Wykonaj 4 passa sekwencyjnie:

## Pass 1 — Correctness
- Kryteria z delta-spec: każde → PRZESZŁO / NIE
- `just test`, `just check`

## Pass 2 — Security
- RLS, uprawnienia endpointów, sekrety, cross-tenant
- `GROUNDING.md` HC-01..HC-06

## Pass 3 — Domain
- Decimal, charge=marża, source_ref, human approval ekstrakcji
- Brak float, brak LLM liczącego

## Pass 4 — Duplication
- `just dup`, lowca-duplikatow
- Type-4 semantic clones — czy logika już istnieje?

## Output
Tabela + lista blokujących vs informacyjnych. Nie naprawiaj w tym kroku.
