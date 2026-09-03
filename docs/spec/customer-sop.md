# M-16 customer_sop — procedury operacyjne klienta

**Moduł żywy:** M-16 (archiwum M-16; nie koliduje z M-03 `organization_setting` / M-35 zlecenie)  
**Plaster:** **11.0** (katalog) · **73.0** (`blocks_auto`)  
**Status:** katalog SOP + flaga „nie wolno auto”. Nie send. Nie generator zadań.

Delta: [docs/deltas/archived/73.0-sop-blocks-auto.md](../deltas/archived/73.0-sop-blocks-auto.md). Fundament: [11.0](../deltas/archived/11.0-customer-sop.md).

## 73.0 blokada auto

### Zakres

- `customer_sop.blocks_auto` BOOLEAN NOT NULL default true
- `GET /customer-sops/auto-block?party_id=` — true gdy jest zatwierdzona SOP z flagą
- Draft nie blokuje. UI checkbox na `/customer-sops`

### Poza 73.0

Send / Graph (S18) · szyna Akceptuj/Zmień (S11) · parser `body` · generator zadań

### HC

- RLS bez nowej tabeli. Serwis SOP nie importuje inbound / quotations.
- LLM nie liczy i nie pisze SOP.

## 11.0 katalog SOP

### Zakres

- Tabela `customer_sop` per tenant: kod, tytuł, treść, `draft`/`approved`
- Create = draft; `approve`; `resolve(party_id, code)`
- UI `/customer-sops` + panel na `/parties`

### HC

- RLS FORCE + test izolacji
- ExtractionService nie importuje `parties`
