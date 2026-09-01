# M-16 customer_sop — procedury operacyjne klienta

**Moduł żywy:** M-16 (archiwum M-16; nie koliduje z M-03 `organization_setting` / M-35 zlecenie)  
**Plaster:** **11.0** (plan)  
**Status:** plan — katalog SOP + zatwierdzenie. Nie generator zadań. Nie walidacja zlecenia.

Delta: [docs/deltas/open/11.0-customer-sop.md](../deltas/open/11.0-customer-sop.md).

## 11.0 katalog SOP

### Zakres

- Tabela `customer_sop` per tenant: `organization_id`, `party_id`, `code` (snake), `title`, `body`, `status` (`draft`|`approved`), `approved_at`, `source_ref`, timestamps
- Unikat `(organization_id, party_id, code)`. FK złożone do `party`
- Create = draft; `approve` z draft; `resolve(party_id, code)`
- OpenFGA `can_manage_parties` = member
- UI `/customer-sops` + panel na `/parties`

### Poza 11.0

Generator zadań · walidacja przy zleceniu (M-35) · `superseded_by` · M-18 · M-19 · ExtractionService · LLM piszący SOP · `organization_setting` jako treść SOP

### HC

- RLS FORCE + test izolacji
- Konfiguracja operacyjna klienta jest danymi, nie kodem — ale nie w allowliście M-03
- LLM nie liczy i nie pisze SOP
- ExtractionService nie importuje `parties`
