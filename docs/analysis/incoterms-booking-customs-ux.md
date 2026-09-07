# Incoterms, booking, odprawa, skrzynka buy — audyt i kontrakt Omni

**Data:** 2026-09-08. **Nie kanon kolejki** — kanon = PLAN (wpięte IDs niżej). Zero kodu w tej karcie.  
**Źródła:** ICC Incoterms 2020 (publiczne tabele alokacji; **nie** cytujemy oficjalnego tekstu ICC), CargoWise / Descartes / Magaya (docs vendorów 2025–2026), overlay skrzynek (Keelway×Magaya, CargoInbox, FreightMynd, Varolio), matryca Omni §13q (slot ≠ gwarancja).

## Werdykt (jedno spojrzenie)

| Temat | Jak robią najwięksi | Co robimy w Omni | Czego nie robimy |
|---|---|---|---|
| Kto bookuje / kto odprawia | CargoWise: job + **party roles** + szablon dokumentów; Descartes: TMS + osobny customs; Magaya: freight+customs w jednym, **mail poza TMS** | Katalog `incoterm_responsibility` (dane) + `shipment_stakeholder` + szkice maila jak Fala O. Człowiek zatwierdza cel | LLM wybiera Incoterms albo „zgaduje” agenta |
| Dokumenty do agenta / armatora / agencji | SoR trzyma plik przy zleceniu; wysyłka = e-mail / eAdaptor / broker module | `document_dispatch_rule` → N× `mail_draft` + załączniki `shipment_document`. HITL send | Auto-send; Selenium na portal celny |
| Booking „sam wie gdzie” | Nikt nie ma magii. Overlay AI **proponuje**, operator klika. Zavin/FreightMynd: 50% maila z approval | `booking_instruction` z macierzy + pusty stakeholder = „wskaż party”. Zakres: precarriage / ocean / oncarriage / contact_exchange | Live HTTP armatora bez S21/umowy |
| Slot we wszystkich portach | **Nikt.** PCS/TOS per terminal (Navis, lokalne API). CargoWise = adapter per kraj | Katalog `terminal_slot_connector`: `api` \| `email_hitl` \| `portal_task` \| `unsupported` na **każdym** terminalu | Gwarancja slotu; bot na portal |
| Skrzynka per agent | CargoWise/Magaya = SoR; praca w Outlooku. Keelway: ranking **per shipment**, ocean osobno od FTL | Widok buy-desk: group-by **edytowalny** (`table_view`): party / kraj / wątek / status | Nowy czat; auto-zapis stawki z maila |
| Kraj na liście agentów | Słownik kontrahenta (ISO) | `party.country_code` **już jest** — pokazać i filtrować (O7) | Druga kolumna „kraj” poza ISO |

---

## 1. Incoterms → obowiązki (dane, nie model)

Publiczna alokacja ICC 2020 (eksport / główny fracht / import). DDP jedyny, gdzie sprzedawca robi import.

| Incoterm | Odprawa eksport | Główny fracht (kto contraktuje) | Odprawa import |
|---|---|---|---|
| EXW | kupujący | kupujący | kupujący |
| FCA, FAS, FOB | sprzedawca | kupujący | kupujący |
| CFR, CIF, CPT, CIP | sprzedawca | sprzedawca | kupujący |
| DAP, DPU | sprzedawca | sprzedawca | kupujący |
| DDP | sprzedawca | sprzedawca | sprzedawca |

Omni nie jest stroną kontraktu sprzedaży. Jest **spedytorem klienta**. Macierz operacyjna ma oś `trade_side`:

- `import` = klient Omni = **kupujący** (typowy import PL).
- `export` = klient Omni = **sprzedawca**.

Z tego SQL składa **domyślnego adresata** (rola, nie osoba):

| trade_side | Incoterm | Przykład jobu | Domyślny booking_scope | Domyślny recipient dokumentów import |
|---|---|---|---|---|
| import | DAP / DPU | Agent w CN prosi o kontakt załadowcy; daje kontakt swojego agenta w PL | `contact_exchange` + dest haulage; **nie** ocean (sprzedawca już bookuje) | `omni_customs` albo `client_customs` (flaga na zleceniu) |
| import | FOB / FCA | My bookujemy ocean + dest | `ocean` + `oncarriage` | j.w. |
| import | EXW | My organizujemy całość z origin | `precarriage` + `ocean` + `oncarriage` + export docs do origin_agent | j.w. |
| import | CIF / CFR | Ocean po stronie sprzedawcy | `oncarriage` + import docs | j.w. |
| export | FOB | My do statku + eksport | `precarriage` + `ocean` (do FOB) | docs eksport → `omni_customs` / `origin_agent` |
| export | DAP | My do miejsca + eksport | pełny łańcuch poza importem | import docs → agent dest / klient dest |

Puste pole stakeholder = UI „wskaż kontrahenta tej roli”, nie zgadywanie z LLM.

**DAP Chiny → PL (Twój przykład):** instrukcja `contact_exchange`: szkic do origin_agent (namiary załadowcy z `shipper`) + szkic do klienta (kontakt dest_agent). To **nie** jest booking u armatora.

---

## 2. Jak to mają Soft / TMS (fakty, nie marketing)

**CargoWise:** jeden job; role (shipper, consignee, agent, carrier, customs broker); dokumenty przypięte do jobu; wysyłka do overseas agent przez e-mail / eAdaptor. Customs = Value Pack per jurysdykcja, nie „jeden silnik świata”. Booking u armatora = konektor per linia, nie uniwersalny.

**Descartes Forwarder TMS:** operacje + osobno CustomsInfo / filing. Slot/brama = inny produkt (PCS). Nie grupuje wątków RFQ jak Gmail.

**Magaya:** freight+warehouse+customs w stacku. **Luka potwierdzona przez Keelway (2026):** odpowiedzi agentów/armatorów lądują w Gmail i **nie** są w Magaya. Overlay: match do shipment, ocean osobno od FTL, ranking stawek — **propozycja**, zapis do Magaya po potwierdzeniu.

**Overlay (CargoInbox, FreightMynd, Varolio, Zavin):** 80% roboty spedytora jest w mailu. Wspólny wzorzec UX: (1) wątek przypięty do **jednego** zlecenia/oferty, (2) grupa per nadawca/carrier, (3) extract → HITL, (4) SLA „brak odpowiedzi”. Żaden nie zastępuje macierzy Incoterms.

**Wniosek UX:** nie budujemy drugiego Outlooka. Budujemy **buy-desk / ops-desk na ofercie i zleceniu**: lewa kolumna = grupy (edytowalny group-by + saved view), prawa = wątek (`in_reply_to` / `rfc822_message_id` — pola już w pola-wizja na `inbound_message`). Jedno spojrzenie: status grupy (czekamy / jest stawka / najtańsza / najszybszy TT z O1).

---

## 3. Slot „we wszystkich portach”

PDF Omni już odrzucił **gwarancję** slotu (s.290). CargoWise też nie rezerwuje „wszędzie”.

Kontrakt Omni:

- Każdy `terminal` (M-05 4.2) ma wiersz `terminal_slot_connector.mode`.
- `api` tylko przy **oficjalnym** API (P0: Baltic Hub OAuth gdy umowa — TO_VERIFY).
- Brak API = `email_hitl` (szkic do terminalu) albo `portal_task` (zadanie człowiekowi). Nigdy Selenium.
- Tabela `terminal_appointment`: okno, status `requested`/`confirmed`/`rejected`, `source_ref`.
- UI: semafor na terminalu (zielony = API, żółty = mail, szary = brak). Operator widzi prawdę, nie „zarezerwowaliśmy wszędzie”.

---

## 4. Telematyka — dwa reżimy (Twoja decyzja 2026-09-08)

| `observation_kind` | Kiedy wolno pollować flotę | Stop | Ponowne włączenie |
|---|---|---|---|
| `omni_telematic` | Pakiet Omni (Teltonika/Queclink) **u tego przewoźnika**, umowa powierzenia | Nie gasimy po 3 dniach — flota w umowie | n/d |
| `external_api` | GBOX/IKOL/… BYO | **3 dni robocze** bez `trip` na tej płycie (nie kalendarzowe) | nowy `trip` na tej rejestracji → `active` |

RODO art. 5: minimalizacja zostaje przy **zewnętrznym** GPS. Flota 24/7 tylko gdy Omni jest operatorem urządzenia i jest umowa z przewoźnikiem (on = administrator danych kierowców albo współadmin — klauzula w umowie tenanta; TO_VERIFY prawnik).

---

## 5. Scoring — cofnięcie „na stałe”, nie auto-decyzja

Twoja decyzja: zostaje, **umowy RODO**, AI = **sugestia**, zawsze człowiek.

Zgodne z kartą [005-jdg-wywiadownie-prawo.md](../_knowledge/market/005-jdg-wywiadownie-prawo.md): art. 22 = zakaz **wyłącznie** zautomatyzowanej decyzji. AI Act wysokie ryzyko = zakaz **auto-scoru bez człowieka**.

| Job | Co wolno | Co nie |
|---|---|---|
| Kredyt | Fakty SQL + raport wywiadowni + **szkic sugestii**; `credit_review` + S11 | LLM liczy limit; zapis limitu bez accept |
| Score kierowcy | KPI tripa/pojazdu w SQL; opcjonalna sugestia przy DPA | auto-HR, zwolnienie z modelu |
| Kamera | BYO incydent → flaga + HITL | własny Video AI; ocena osoby bez umowy |

---

## 6. Pola (szkic; Plan tnie)

Nowe tabele: `incoterm_responsibility`, `shipment_stakeholder`, `document_dispatch_rule`, `document_dispatch`, `booking_instruction`, `terminal_slot_connector`, `terminal_appointment`.  
Rozszerzenia: `resource_telematics_link.observation_kind`; `credit_review.suggested_*` (tekst + Decimal wpisuje człowiek albo SQL, nie model); `table_view.group_by`; pokaz `party.country_code` na liście O.

Szczegóły: [karty-pol-fala-i.md](karty-pol-fala-i.md).

---

## 7. Audyt nauki i case'ów (logika + UX)

Źródła **publiczne**; statusy CONFIRMED / TO_VERIFY. Nie zmyślamy API.

### Prawo i decyzja (scoring, GPS)

| Źródło | Co mówi | Skutek w Omni |
|---|---|---|
| RODO art. 22 | Zakaz decyzji **wyłącznie** zautomatyzowanej wobec osoby | Szkic AI wolno; zapis limitu / score = S11 |
| RODO art. 5(1)(c) | Minimalizacja | External GPS: 3 dni robocze bez trip. Flota tylko gdy Omni jest operatorem pakietu + umowa |
| AI Act zał. III 5(b) + motyw 58 | Creditworthiness / scoring osoby = wysokie ryzyko przy autonomii | LLM **nie liczy** limitu (HC). M14b = tekst sugestii |
| EDPB Guidelines 05/2020 (consent) + DPA | Kamera / score kierowcy = powierzenie + podstawa | Umowy tenanta zanim ingest BYO |

### Incoterms i forwarding (logika, nie marketing)

| Źródło | Co mówi | Skutek w Omni |
|---|---|---|
| ICC Incoterms 2020 — **publiczne** tabele alokacji (eksport / main carriage / import) | DDP jedyny z importem po stronie sprzedawcy | Katalog `incoterm_responsibility` jako **dane**; nie wklejamy tekstu ICC |
| FIATA Model Rules / praktyka agent overseas | Agent origin/dest to **role na jobie**, nie „ktoś z maila” | `shipment_stakeholder.role` + pusty = „wskaż party” |
| CargoWise One (docs: job + organization/party roles + document templates + eAdaptor) | Jeden job; wysyłka docs = szablon × rola; customs = Value Pack per kraj | I2 + I3; nie jeden silnik celny świata |
| Descartes Forwarder TMS vs CustomsInfo | Operacje ≠ filing celny | I3 = mail/HITL; C-fala = filing gdy API |
| Magaya + overlay Keelway (komunikat 2026: odpowiedzi agentów zostają w Gmail) | SoR nie grupuje RFQ; overlay matchuje do shipment, zapis po approve | Fala O + O8; ExtractionService nie zapisuje stawek |

### Skrzynka i UX (nauka HCI + overlay)

| Źródło | Co mówi | Skutek w Omni |
|---|---|---|
| Whittaker & Sidner 1996, *Email overload* | Ludzie gubią się w płaskiej skrzynce; ratunek = wątki i foldery zadaniowe | Group-by **edytowalny** (party / kraj / wątek / status), nie drugi Inbox |
| Bellotti et al. CHI 2005, *Taking email to task* | Mail jest listą zadań; UI musi pokazać **stan jobu**, nie treść listu | Karta grupy: czekamy / jest stawka / najtańsza / najszybszy TT (SQL O1) |
| CargoInbox, FreightMynd, Varolio, Zavin (case'y vendor 2024–2026) | 1 shipment = 1 wątek; extract → approval 50%+; ocean osobno od FTL | Ten sam wzorzec co O4/O6; zero auto-send |
| Nielsen: recognition over recall + pojedynczy punkt orientacji | Jedno spojrzenie = semafor grupy, nie 40 otwartych maili | Saved view (`table_view`); default group = `party` |

### Slot portowy (dlaczego nie ma „wszystkich portów”)

| Źródło | Co mówi | Skutek w Omni |
|---|---|---|
| IPCSA / Port Community System — literatura (PCS per port, nie global API) | Każdy TOS/PCS (Navis N4, lokalne) ma inny kontrakt | `terminal_slot_connector.mode` na **każdym** terminalu |
| CargoWise terminal connectors | Adapter per kraj / per terminal, nie „zarezerwujemy wszędzie” | T8; gwarancja slotu = odrzut (PDF s.290) |
| PDF Omni s.296, 309 | Selenium na portal = zakaz | `portal_task` = zadanie człowiekowi |

**Wniosek idealnego rozwiązania:** CargoWise wygrywa **modelem danych** (job + role + szablon). Overlay wygrywa **UX skrzynki** (grupa + HITL). Nikt nie wygrywa slotów ani magicznego bookingu. Omni składa: macierz Incoterms jako dane + role + ten sam mail/HITL co Fala O + capability matrix slotów + dwa reżimy GPS.
