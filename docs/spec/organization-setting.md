# M-03 organization_setting — konfiguracja jako dane

**Plaster:** 3.0  
**Status:** fundament (katalog ustawień tenanta). Nie env. Nie sekrety.

## Zakres

- Tabela `organization_setting`: `organization_id`, `setting_key`, `setting_value`, timestamps
- Unikalność `(organization_id, setting_key)`
- Klucze z allowlisty: `default_currency` (ISO 4217), `quotation_number_prefix` (1–16 A–Z 0–9 . _ -), `quotation_print_template` (`plain` | `letter`); nieznany klucz = odrzut
- Sekrety (`*secret*`, `*password*`, `*token*`, `*api_key*`) nie wchodzą
- OpenFGA `can_manage_organization_settings` = member
- UI `/organization-settings`: DataTableShell + zapis waluty, prefiksu i tokenu szablonu

## Poza zakresem

outbox, Infisical, Auth0, sekrety tenanta, `table_view`, zmiana HITL, ExtractionService, licznik / `quotation.document_number`, PDF.

## HC

- RLS FORCE + test izolacji
- Konfiguracja jest danymi, nie kodem
- Kwoty nadal Decimal; tu tylko waluta ISO, nie liczenie
