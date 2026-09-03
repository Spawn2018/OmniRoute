# M-71 operator_decision — szyna Akceptuj/Odrzuć

**Plaster:** **74.0** (delta `docs/deltas/archived/74.0-operator-decision.md`)  
**Status:** ukończony (fundament) — pending + accept/reject. Nie M-57. Nie accept extractu.

## Zakres

- Tabela `operator_decision` per tenant: `subject_kind` (start: `inbound_message`), `subject_id` UUID bez FK, `status`, `decided_at`, `source_ref`
- Create = `pending`. POST decide: `accepted` albo `rejected`. Unikat pending na `(organization_id, subject_kind, subject_id)`
- OpenFGA `can_manage_operator_decisions` = member
- UI `/decisions`: lista + pending + Akceptuj / Odrzuć

## Poza zakresem

`changed` w zapisie · FK do `inbound_message` · draft maila (S13) · lock (S14) · send (S18) · accept HITL 1.3 · F9.1

## HC

- RLS FORCE + test izolacji
- Serwis nie importuje inbound / quotations / extraction
- LLM nie liczy. `charge` zostaje prawdą o marży
