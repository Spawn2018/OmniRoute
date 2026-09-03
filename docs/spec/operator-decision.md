# M-71 operator_decision — szyna Akceptuj/Odrzuć

**Plaster:** **74.0** fundament · **77.0** `lock_version` · **121.0** (zamknięty)  
**Status:** pending + accept/reject/changed + lock. Nie M-57. Nie accept extractu.

Delta: [74.0](../deltas/archived/74.0-operator-decision.md) · [77.0](../deltas/archived/77.0-decision-lock.md) · [121.0](../deltas/archived/121.0-decision-changed.md).

## Zakres

- Tabela `operator_decision` per tenant: `subject_kind` (`inbound_message` albo `mail_draft`), `subject_id` UUID bez FK, `status`, `decided_at`, `lock_version`, `source_ref`
- Create = `pending`, `lock_version` 0. POST decide: `accepted` | `changed` | `rejected` + `lock_version`. Unikat pending na `(organization_id, subject_kind, subject_id)`
- Decide = jeden `UPDATE … WHERE pending AND lock_version`. Drugi Akceptuj = konflikt.
- OpenFGA `can_manage_operator_decisions` = member
- UI `/decisions`: lista + pending + Akceptuj / Zmień / Odrzuć z wersją

## Poza zakresem

FK do `inbound_message` · send (S18) · accept HITL 1.3 · F9.1

## 121.0 werdykt `changed`

### Zakres

- POST decide: `accepted` | `changed` | `rejected` + `lock_version`
- Przycisk Zmień na `/decisions`

### Poza 121.0

Nadpisanie po zapisie · LLM · send

## HC

- RLS FORCE + test izolacji
- Serwis nie importuje inbound / quotations / extraction
- LLM nie liczy. `charge` zostaje prawdą o marży
