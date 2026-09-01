# M-12 network — katalog sieci i stowarzyszeń

**Plaster:** **9.0** (delta `docs/deltas/open/9.0-network.md`)  
**Status:** plan — katalog per tenant. Nie katalog agentów. Nie scraping.

## Zakres

- Tabela `network`: `organization_id`, `code` (token snake), `name`, `aliases[]`, `website`, `region_scope`, `is_global`, `source_ref`, timestamps
- Unikalność `(organization_id, code)`
- `resolve(token)` — kod albo alias; nieznany = `UnknownNetwork`
- OpenFGA `can_manage_networks` = member
- UI `/networks`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

`network_membership` · `network_member` · kontakty · `network_member_link` · import Excel/PDF · RapidFuzz / dedupe · ranking M-13 · zapytanie do agenta (M-30) · scraping portali WCA/Globalia · wspólny katalog SaaS · FK do `party` · ExtractionService

## HC

- RLS FORCE + test izolacji; `organization_id` na każdym wierszu (kopia per tenant — legalność sui generis)
- Kwoty nie mieszkają na katalogu
- LLM nie liczy i nie zgaduje członkostwa
- ExtractionService nie importuje `networks`
