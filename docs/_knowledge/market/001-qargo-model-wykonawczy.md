# Qargo — model wykonawczy (zweryfikowany 2026-09)

**Kiedy:** Plan modułów Fali T (stop/trip/resource/task/planning board).

## Model danych (api-docs.qargo.com, sekcja Concepts)

- `Company` = jeden byt, może być jednocześnie customer i subcontractor.
- `Order` (jednostka przychodowa) → `Consignment` → `Stop` / `Stop group`.
- `Trip` = jednostka wykonawczo-kosztowa; „contains stops from various orders";
  read-only przez API; koszty na `/v1/trips/trip/{id}/costs`.
- `Resource` = pojazd / kierowca / naczepa. `Task` = workflow z warunków.
- Expected vs actual: koszt liczony w statusie Planned zapisany jako snapshot
  przy przejściu do In Transit; późniejsze zmiany tylko w Actual; wariancja w P&L tripa.

## Planning board

- Widoki: Timeline / Blocks / Table / Legs + osobny pre-planning.
- Mapa (PTV): selekcja prostokątem i poligonem, do 1000 orderów To Plan;
  markery: trójkąt=collection, kwadrat=delivery, koło=other; kolor=status;
  warstwy: Satellite / LEZ / Live Traffic / Truck Restrictions.
- Select & Drop zastąpił „drag and scroll" (drag&drop działa w obrębie ekranu).
- Gęstość A+ / A−; saved views: All users / Private / Specific users.

## Task engine

Warunki szablonu: Route, Goods, Service level, Transport service,
Vehicle category, Customer, Department — ewaluowane asynchronicznie.

## Dla OmniRoute

Stop/trip/resource = luka (S50 parkował z braku jobu). Werdykty i fale:
`docs/analysis/benchmark-tms-2026.md` § 2. Nie kopiować stacku (ADR-0004).
