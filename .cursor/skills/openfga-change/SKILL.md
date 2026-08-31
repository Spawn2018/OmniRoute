# Skill: zmiana modelu OpenFGA

## Kiedy
Nowe uprawnienie, nowa relacja, nowy typ obiektu AuthZ.

## Kroki
1. Edytuj `authz/model.fga` (źródło prawdy).
2. Zaktualizuj `app/integrations/openfga/model.py` (WriteAuthorizationModelRequest).
3. Dodaj test: odmowa bez tuple + pozwolenie z tuple.
4. Endpoint: jawna deklaracja `require_permission(...)` — brak = odmowa (GROUNDING HC-05).

## Zakaz
- DIY RBAC obok OpenFGA
- Sprawdzanie uprawnień w serwisie domenowym (AuthZ na granicy API)
