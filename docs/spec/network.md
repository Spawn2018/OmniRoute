# M-12 network — katalog sieci i stowarzyszeń

**Plaster:** **9.0** · **82.0** (`docs/deltas/archived/82.0-network-member.md`)  
**Status:** ukończony (fundament) — katalog sieci + ręczni członkowie per tenant. Nie portal WCA.

## Zakres

- Tabela `network`: `organization_id`, `code` (token snake), `name`, `aliases[]`, `website`, `region_scope`, `is_global`, `source_ref`, timestamps
- Unikalność `(organization_id, code)`
- `resolve(token)` — kod albo alias; nieznany = `UnknownNetwork`
- OpenFGA `can_manage_networks` = member
- UI `/networks`: lista DataTableShell + dodanie + rozwiązanie tokenu

## 82.0 `network_member`

- Tabela per tenant: `network_id` FK, `member_code`, `legal_name`, `source_ref`
- RLS FORCE. `GET/POST /networks/{id}/members`. Ten sam `/networks`
- Zero portalu / RapidFuzz / FK `party`

## Poza zakresem

`network_membership` · kontakty · `network_member_link` · import Excel/PDF · RapidFuzz / dedupe · ranking M-13 · zapytanie do agenta (M-30) · portal WCA/Globalia · wspólny katalog SaaS · FK do `party` · ExtractionService

## HC

- RLS FORCE + test izolacji; `organization_id` na każdym wierszu (kopia per tenant — legalność sui generis)
- Kwoty nie mieszkają na katalogu
- LLM nie liczy i nie zgaduje członkostwa
- ExtractionService nie importuje `networks`
