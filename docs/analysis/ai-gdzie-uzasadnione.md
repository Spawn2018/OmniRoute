# AI — gdzie uzasadnione (kanon)

Źródła (tylko): `AGENTS.md` (zasady 4, 8; sqlglot), `GROUNDING.md` HC-02/04 (+ HC-03, HC-08), `docs/spec/extraction.md`, ADR-0003 §9–10 HITL, `PLAN-REALIZACJA.md` M-20 + U-art50, `benchmark-tms-2026.md` §10 i §13m–13p.

**Już w kontrakcie:** M-20 draft→HITL→accept; model wyciąga, kod przetwarza, **model nie liczy**; zapis tylko przez `service` po człowieku; `amount_text` nie float; `source_ref` + `unparsed_regions`; Art. 50 = label UI (`U-art50`), nie opinia prawna.

**13g–13l** poza tym wycinkiem lektury. **13m–13p** chce AI tam, gdzie ten sam pipeline M-20 zdejmuje przepisywanie; nie chce AI tam, gdzie jest XSD, SQL, kod kreskowy albo oficjalne API.

---

## 1. AI TAK (HITL obowiązkowy)

Wymierna korzyść operatora: mniej ręcznego przepisywania z PDF/maila. Korzyść budowniczego: **jeden** `extraction_draft` + split, nie pięć parserów.

| # | Job / pola | Skąd | Korzyść | Warunek HITL |
|---|---|---|---|---|
| 1 | Cennik / oferta → kandydaci stawek (`amount_text`, `charge_code` z katalogu, `unparsed_regions`) | M-20, 1.3 | Zero transkrypcji cennika | Accept → `rate_line` w tej samej transakcji HTTP; `ExtractionService` nie zapisuje stawek |
| 2 | Treść / załącznik `inbound_message` → ten sam `extract_to_draft` | spec M-20 66.0, PLAN S3 | Jeden kanał poczta→kolejka, nie drugi extractor | HITL zostaje; serwis nie pisze `rate_line` |
| 3 | Mail → szkic RFQ / pól zlecenia (klasyfikacja + ekstrakcja, nie silnik wyceny) | §10 ULEPSZ | Mniej kopiowania z wątku | Draft; matching kontrahenta nie jest auto-zapisem `party` |
| 4 | FV kosztowa z maila / skanu → `extraction_draft` kind=`purchase_invoice` | §13m | Jedna kolejka zamiast ręcznego FZ | Bez accept **brak** `purchase_invoice` na zleceniu i **brak** sync FK |
| 5 | Skan CMR/POD/obcy dokument **bez** kodu Omni → kind + pola | §13n tor 2 | Operator nie zgaduje zlecenia z rozmazanego CMR | Drabina SQL + accept; model nie wybiera `shipment` |
| 6 | Ten sam split HITL dla: RFQ klienta, FV kosztowa, cennik, CMR/POD | §13o, ADR-0003 | Jeden UI; `draft.kind` różni job, nie nowy ekran | Confidence per pole, span/bbox, reject z powodem, Art. 50; optimistic accept zakazany |
| 7 | Pola z `bbox` + pewność 0–1 + `span_text`; edycja `amount_text` przed accept | §13o, leftover `U-pdf-spans` | Mniej poprawek; niskie pasmo nie wchodzi w accept zbiorczy | Decimal przy accept w kodzie; `operator_override` nie „poprawia” pewności modelu |
| 8 | Klasyfikacja `document_kind` gdy brak QR | §13n | Porządek skrzynki skanów | Zapis `shipment_document` dopiero po accept (tor bez kodu) |
| 9 | Diff pól dokumentu vs zlecenie (waga, sztuki, data) | §13n X6 | Widać rozjazd, nie cichy overwrite | Konflikty do recenzji |
| 10 | Szkic `mail_draft` „podaj `shipment_ref` / kontener” przy FV bez sygnałów | §13m | Mniej ręcznych maili o numer | Świadomy mailto; nigdy auto-send |
| 11 | Label „propozycja AI” na szkicu | PLAN `U-art50`, Fala 4 copilot/mail | Spełnienie Art. 50 w UI | Draft bez labelu = gate pada; D0 nie zdejmuje HITL |
| 12 | Guard przed modelem (regex dziś; llm-guard + Presidio = cel HC) | spec M-20, AGENTS | Wejście niezaufane nie idzie nagie do LLM | Guard ≠ zapis; CI = `mock` |

OpenCV kadr/enhance i ML Kit / VisionKit przy spuście to **geometria**, nie ten wiersz — idą **przed** instructorem (§13o).

---

## 2. AI NIE (sprzeczne z HC / 13m–13p)

| # | Job | Blokada | Dlaczego |
|---|---|---|---|
| 1 | Sumy, marża, VAT, kurs NBP, przeliczenia | HC-02, zasada 4 | Model nigdy nie liczy; `charge.margin` i SQL |
| 2 | Auto-zapis extractu / `rate_line` / `charge` / zlecenia z modelu | HC-04, zasada 8 | AI = JSON/intent; zapis = `service` po Pydantic + człowiek |
| 3 | Sell / marża z LLM; druga tabela marży | PLAN 1.3, M-08, HC-02 | Accept HITL ≠ `charge`; LLM nie wstawia sprzedaży |
| 4 | Auto-podpięcie FV kosztowej pod `shipment` | §13m | Progi M-03 sortują recenzję; nigdy auto-podpięcie |
| 5 | Score dopasowania FV / suma linii zbiorczej w modelu | §13m | Drabina i suma = SQL; Decimal z akceptowanego draftu |
| 6 | Parser KSeF FA(3) przez LLM | §13m | XML + XSD, nie instructor |
| 7 | Auto-zapis skanu gdy **jest** kod Omni — albo LLM zamiast skanera | §13n tor 1 | SQL + `source_ref=scan://`; LLM tu jest zbędny i groźny |
| 8 | Auto-scoring `natural_person` / JDG; scoring osoby na karcie / fraud | PLAN AI Act, M-14, §10 sąsiad M-13/M-54 | Minimal risk tylko przy HITL i **braku** scoringu osoby |
| 9 | Real-ESRGAN / GFPGAN / inpainting „dopisz róg / cyfrę” na FV | §13o | Nowa treść; kwota nie może powstać z wymyślonego glifu |
| 10 | Accept bo „pewność wysoka”, optimistic UI na kwocie/`accept` | ADR-0003 §9–10, HC-04 | Pewność sortuje kolejkę, nie zastępuje kliknięcia |
| 11 | RAG / pgvector na wycenie, schemacie DB, VAT | HC-08 | RAG tylko SOP / ADR / maile / dokumentacja API |
| 12 | Numer nadania / imię EPO z OCR koperty; koszt znaczka z LLM; śledzenie PP ze scrapa | §13p | REST/EN + skaner HID; imię = `getEPOStatus` albo HITL ze skanu; `charge` z `source_ref` |

---

## 3. SZARE (Prediction Ledger + Art. 50 + HITL; nie P0 nocy)

| # | Job | Plan | Warunek | Nie P0 |
|---|---|---|---|---|
| 1 | ETA / slot / „kiedy dojedzie” | §10 milczy; predykcja w kanonie = zmierzona, nie magia | Wpis do Prediction Ledger; HITL zanim status klienta | Silnik SQL/telemetria najpierw; LLM nie liczy ETA |
| 2 | AI summaries wątków mailowych | §10 KOPIUJ, fala HZ | Label Art. 50; nie zapis encji | Nie kolejka M-20 |
| 3 | Chat → reguła walidacji (tekst → dane → test na próbie → aktywacja) | §10 ULEPSZ, HZ | Zasada 2: konfiguracja = dane; człowiek włącza | Nie parser stawek |
| 4 | Czat o rekordach / copilot wieży (M-57) | §10 CZĘŚĆ, HZ | Art. 50; szkice, nie nowy czat-zapis | PLAN S56/S58: nigdy auto-send |
| 5 | Agent zakupowy (RFQ→odpowiedzi→ranking) | §10 CZĘŚĆ M-30/31, HZ | Ranking = propozycja; award po człowieku | Nie live HTTP z modelu |
| 6 | Narracja CFO / raport po SQL (M-15, S57) | §10 JEST | Zdania z pól SQL; LLM nie liczy | Rozszerzenia predykcyjne = F/V, nie nocny plaster |
| 7 | Anomalia / fraud jako „dowód” | sąsiad §10, M-54 | Flaga do recenzji ≠ werdykt | Nie scoring osoby |
| 8 | Ryzyko kontrahenta / early warning zarządu | poza §10 jobem M-20 | Podmiot, nigdy osoba; Decision Ledger | Wieża V/HZ |
| 9 | Contract intelligence (FV vs umowa) | nie w 13m jako P0 | Diff + HITL; kwoty z Decimal po accept | Po żywym `purchase_invoice` |
| 10 | Negocjacje w limitach ceny/marży | nie 13m–13p | Limity z danych + HITL; marża zostaje w `charge` | HZ ostrożnie |
| 11 | SQL z modelu (zapytania) | AGENTS bezpieczeństwo | Tylko przez `sqlglot`; nie logika wyceny | Nie silnik M-21 |
| 12 | Digital twin / Omni Market forecasts | nie 13m–13p | B0 = zdarzenia + Prediction Ledger zanim „AI przewiduje” | Park / HZ; zakaz obietnicy magii |

P0 tej osi (jeśli w ogóle AI): ten sam M-20 na FV/skanach (§13m–13o) + `U-art50` / spany. Reszta szarości czeka na ledger i HITL, nie na nocny parser.
