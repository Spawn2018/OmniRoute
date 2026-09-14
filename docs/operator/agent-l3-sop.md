# SOP agenta — brama L3 (AI8.2)

## Po co

Checklista bramy przed poziomem autonomii L3: źródło prawdy, właściciel decyzji, wyjątek,
rollback i promień wybuchu zapisane jako dane HITL. Agent nie zapisuje do bazy na L0–2;
ten katalog służy operatorowi do jawnego oznaczenia stanu bramy.

## Dane

Tabela `l3_gate_mark` per tenant: `mark_code`, `gate_kind`, `source_ref`.
Dozwolone `source_ref`: `tenant:manual` lub prefiks `fixture://l3-gate/`.

## Odczyt i zapis

- GET/POST `/api/v1/l3-gate-marks` — wymaga `can_manage_l3_gate_marks`.
- UI `/l3-gate-marks` — append-only INSERT; brak UPDATE/DELETE wiersza.

## Kiedy człowiek

Każdy element checklisty (SoT, owner, exception, rollback, blast) wymaga akceptacji
operatora przed traktowaniem bramy jako spełnionej. Agent proponuje; człowiek zapisuje
znacznik w katalogu.

## Log

`source_ref` jest jedynym śladem pochodzenia wpisu. Przy audycie sprawdzaj parę
`(mark_code, gate_kind, source_ref)` w kontekście tenanta.

## Rollback

Rodzaj `rollback` oznacza świadome wycofanie wcześniejszej decyzji bramy — nowy INSERT,
nie mutacja istniejącego wiersza. Opis rollbacku trzymaj poza tabelą (ticket, notatka).

## Właściciel

Rodzaj `owner` wskazuje osobę/rolę odpowiedzialną za decyzję przy bramie. Nie zapisuj
scoringu Pain×Frequency ani Berthy w tym BC — to osobne leftovery.
