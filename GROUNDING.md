# GROUNDING.md — twarde ograniczenia domenowe (HC)

**Hard Constraints (HC)** wygrywają z promptem użytkownika, skillami i regułami stylu.
**Constraint Points (CP)** ostrzegają; HC odmawiają.

## HC-01 Multi-tenancy

- Każda tabela biznesowa ma `organization_id`.
- RLS włączony i wymuszony (`FORCE ROW LEVEL SECURITY`).
- Zero zapytań cross-tenant. Test izolacji obowiązkowy przy każdej nowej tabeli.

## HC-02 Pieniądze

- Kwoty: `Decimal` + waluta jako para. Nigdy `float`.
- LLM **nie liczy** sum, marż, VAT, kursów. Kod deterministyczny.
- `charge` / `shipment_charge` = jedyne miejsce prawdy o marży.

## HC-03 Stawki i provenance

- Bez `source_ref` stawka nie wchodzi do bazy.
- Stawki niemutowalne; zmiana = nowy rekord + `superseded_by`.
- Ekstrakcja wymaga `unparsed_regions` w odpowiedzi.

## HC-04 Zapis AI tylko w granicach autonomii

- Poziomy **0–2** (domyślnie 1): AI generuje propozycję (JSON/intent). **Nie zapisuje** do bazy produkcyjnej. Zapis tylko przez `service` po walidacji Pydantic + regułach biznesowych. Ekstrakcja wymaga akceptacji człowieka przed zapisem.
- Poziomy **3–5**: AI może zapisać **wyłącznie** w granicach zapisanych jako dana (per tenant, per klient) + wiersz w dzienniku audytu. Poza granicą = odmowa.
- Automatyczne zejście poziomu przy spadku jakości (CRPS / Brier / MAE / fidelity) **zanim** jakikolwiek tenant dostanie poziom 3.
- L3–5 nie zdejmuje `source_ref`, Decimal ani `charge` = marża. LLM **nadal nie liczy**.

## HC-05 Bezpieczeństwo i sekrety

- Poświadczenia armatorów/API należą do tenanta, szyfrowane jego kluczem.
- Sekrety nigdy w kodzie, commitach, logach LLM.
- Endpoint bez jawnej deklaracji uprawnień = odmowa.

## HC-06 Integracje

- Wywołania zewnętrzne: idempotencja + timeout + retry z backoffem.
- Zdarzenia między modułami: outbox, nie bezpośrednie wywołanie serwisu.
- Brak pełnego event sourcingu — audit_log + outbox wystarczą.

## HC-07 Wydajność gorących ścieżek

- Silnik wyceny / dobór stawek: **SQL**, nie Python/ORM na 50k wierszy.
- p95 wyceny < 300 ms — warunek merge, nie „później”.

## HC-08 RAG — gdzie wolno, gdzie nie

- **Wolno:** SOP, regulacje ADR, historia maili, dokumentacja API zewnętrznych.
- **Zakaz:** logika wyceny, schemat DB, reguły VAT/podatków — tylko typowany kod/SQL.

## CP-01 Refaktoring

- Trzecie powtórzenie uzasadnia wyodrębnienie. Drugie nie.
- Metryka: kod przeniesiony / dodany ≥ 10% w oknie 4 tygodni.

## CP-02 UI enterprise

- Data-dense, compact mode. Bez „AI slop” (gradienty landing page, gigantyczne paddingi).
- Tabele > 500 wierszy: wirtualizacja obowiązkowa.

## CP-03 Architektura

- Modularny monolit. import-linter egzekwuje granice.
- Mikroserwisy odrzucone (ADR w `docs/adr/`).
