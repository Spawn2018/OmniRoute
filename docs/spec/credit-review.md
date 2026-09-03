# M-14 credit_review — ocena kredytowa (recenzja ręczna)

**Moduł żywy:** M-14 (archiwum M-14; nie koliduje z żywym M-10 `party.credit_limit` / M-13 `party_scorecard` / M-08 `charge`)  
**Plaster:** **14.0** (katalog) · **88.0** (wskazanie raportu)  
**Status:** katalog recenzji kredytowej per `party` + nullable `bureau_attachment_ref`. Nie auto-scoring. Nie scoring `natural_person` / JDG. Nie zmiana `credit_limit`. Nie HTTP do biura.

Delta: [docs/deltas/archived/14.0-credit-review.md](../deltas/archived/14.0-credit-review.md) · [docs/deltas/archived/88.0-credit-review-bureau.md](../deltas/archived/88.0-credit-review-bureau.md).

## 14.0 katalog recenzji kredytowej

### Zakres

- Tabela `credit_review` per tenant: `organization_id`, `party_id`, `review_date`, `decision` (`ok` | `hold` | `refuse`), `note`, `source_ref`, timestamps
- Unikat `(organization_id, party_id, review_date)`. FK złożone do `party`
- `resolve(party_id, on_date)` — najnowszy `review_date <= on_date`
- OpenFGA `can_manage_parties` = member (jak karta wyników; nie nowa relacja)
- UI `/credit-reviews` + panel na `/parties`
- `party.credit_limit` z 5.0 zostaje ręcznym limitem — **nie** kolumna scoringu, **nie** nadpisuj w 14.0

### Poza 14.0

Auto-scoring · biuro BIK/KRD/HTTP · `legal_form` / PESEL · scoring `natural_person` / JDG · zmiana `credit_limit` · SQL z `quotation`/`charge` · M-15 VDF · ExtractionService · LLM liczący limit

### HC

- RLS FORCE + test izolacji
- Brak pola score / rating liczbowego — zakaz auto-scoringu osoby (AI Act) w tym plasterze = brak silnika, nie teatr
- `credit_limit` zostaje parą Decimal na `party`; LLM nie liczy
- Marża zostaje w `charge.margin()`
- ExtractionService nie importuje `parties`

## 88.0 wskazanie raportu wywiadowni

### Zakres

- Kolumna `credit_review.bureau_attachment_ref` TEXT NULL. RLS z 025.
- `PATCH /credit-reviews/{id}/attach-bureau` — URI, który operator już ma. `can_manage_parties`.
- UI `/credit-reviews`: „Dołącz raport”. `source_ref` nietknięty.

### Poza 88.0

Auto-limit · BIK/KRD HTTP · blob · score · `legal_form` · F9.1
