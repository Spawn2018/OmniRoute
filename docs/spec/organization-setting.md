# M-03 organization_setting — konfiguracja jako dane

**Plaster:** 3.0  
**Status:** fundament (katalog ustawień tenanta). Nie env. Nie sekrety.

## Zakres

- Tabela `organization_setting`: `organization_id`, `setting_key`, `setting_value`, timestamps
- Unikalność `(organization_id, setting_key)`
- Klucze z allowlisty (dziś: `default_currency` = ISO 4217 CHAR(3)); nieznany klucz = odrzut
- Sekrety (`*secret*`, `*password*`, `*token*`, `*api_key*`) nie wchodzą
- OpenFGA `can_manage_organization_settings` = member
- UI `/organization-settings`: DataTableShell + zapis waluty domyślnej

## Poza zakresem

outbox, Infisical, Auth0, sekrety tenanta, `table_view`, zmiana HITL, ExtractionService.

## HC

- RLS FORCE + test izolacji
- Konfiguracja jest danymi, nie kodem
- Kwoty nadal Decimal; tu tylko waluta ISO, nie liczenie
