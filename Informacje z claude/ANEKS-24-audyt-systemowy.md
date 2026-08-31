# Aneks 24 — Mechanizmy przekrojowe i audyt systemowy

---

# CZĘŚĆ I — DWADZIEŚCIA REALNIE BRAKUJĄCYCH

Nie moduły domenowe, tylko mechanizmy przecinające cały system. Dlatego
ich brak jest niewidoczny na liście, a odczuwalny w każdym module.

## Grupa 1 — Sterowanie i kontrola

### M-179 · Silnik zatwierdzeń ⚠
**Brak przekrojowy.** Nie ma ani jednego mechanizmu akceptacji, a potrzebny
jest w kilkunastu miejscach.

```sql
approval_policy
  id, organization_id, entity_type
  condition jsonb,        -- np. wartość > 50000 albo marża < 5%
  approver_role_id, approver_user_id NULL
  levels smallint,        -- akceptacja wielostopniowa
  timeout_hours, on_timeout,   -- escalate | auto_approve | auto_reject
  is_active

approval_request
  id, policy_id, entity_type, entity_id
  requested_by, requested_at, level
  status, decided_by, decided_at, comment
  delegated_from_user_id
```

Gdzie jest potrzebny: oferta poniżej progu marży, rabat powyżej progu, zmiana
limitu kredytowego, odpis należności, korekta faktury, zatwierdzenie stawki
z ekstrakcji o niskiej pewności, zwolnienie trafienia sankcyjnego, zmiana
rachunku bankowego kontrahenta.

### M-180 · Silnik korekt i storn
Każda operacja finansowa musi mieć odwrotność. Dziś nie ma wzorca.

```sql
reversal
  id, entity_type, entity_id
  reason_code, reason_text
  reversed_by, reversed_at
  reversal_entity_id,     -- dokument korygujący
  restores_state jsonb
```

Storno faktury, cofnięcie rozliczenia płatności, unieważnienie zlecenia
po bookingu, wycofanie zatwierdzonej stawki, cofnięcie prowizji.

### M-181 · Rejestr wyjaśnień decyzji automatycznych
Wymóg z AI Act i RODO, ale też funkcja zaufania.

```sql
decision_log
  id, organization_id, decision_type
  entity_type, entity_id
  inputs jsonb, rules_applied jsonb, model_version NULL
  output jsonb, confidence
  was_overridden bool, override_by, override_reason
  decided_at
```

Każda automatyczna decyzja: dobór stawki, przypisanie kodu opłaty,
klasyfikacja maila, sugestia limitu, ocena ryzyka. Użytkownik klika
„dlaczego" i widzi ścieżkę.

### M-182 · Tryb próbny
Uruchomienie automatyzacji bez skutków, z podglądem, co by zrobiła.

```sql
dry_run
  id, automation_type, parameters jsonb
  would_affect jsonb, would_create jsonb, would_modify jsonb
  executed_at, executed_by, promoted_to_real bool
```

Krytyczne przy: masowej aktualizacji cennika, zmianie reguł marży, imporcie
danych, uruchomieniu windykacji, przeliczeniu prowizji.

### M-183 · Konfiguracja automatyzacji per tenant
Każda automatyzacja musi dać się wyłączyć bez wdrożenia.

```sql
automation_setting
  id, organization_id, automation_key
  is_enabled, mode,       -- off | suggest | auto
  parameters jsonb, disabled_reason, disabled_by
```

## Grupa 2 — Dane i spójność

### M-184 · Struktura grup kapitałowych ⚠
**Brak w modelu kontrahenta.** Klient należy do grupy, ma spółki zależne,
wspólny limit kredytowy i wspólne cenniki.

```sql
party_relationship
  id, organization_id
  parent_party_id, child_party_id
  kind,        -- subsidiary | branch | agent_of
               -- shared_credit | billing_for
  valid_from, valid_to
```

Bez tego: limit kredytowy liczony osobno dla trzech spółek tego samego
właściciela, faktury do niewłaściwego podmiotu, raport rentowności
rozproszony.

### M-185 · Mapowanie identyfikatorów zewnętrznych
Każda encja musi dać się powiązać z odpowiednikiem w systemie klienta,
armatora albo księgowości.

```sql
external_reference
  id, organization_id
  entity_type, entity_id
  system,      -- carrier | customer_erp | accounting | edi
  system_ref, external_id, external_url
  synced_at, sync_status
```

Bez tego integracja z systemem klienta wymaga dopasowywania po nazwie.

### M-186 · Datowanie efektywne danych referencyjnych
Stawka VAT zmienia się od pierwszego stycznia. Kurs obowiązuje na dzień.
Cennik ma okres. Kod opłaty przestaje obowiązywać.

```sql
-- wzorzec do zastosowania w słownikach
  effective_from, effective_to
  supersedes_id, superseded_by_id
```

Dziś tylko `rate_line` to ma. Powinny też: `charge_code`, `vat_rate`,
`markup_rule`, `payment_term_profile`, `port_charge_rule`.

### M-187 · Blokada optymistyczna
Dwóch użytkowników edytuje tę samą ofertę. Kto wygra?

```sql
-- kolumna na każdej edytowalnej encji
  version integer NOT NULL DEFAULT 1
-- UPDATE ... WHERE id = ? AND version = ?
```

Bez tego cicha utrata zmian. W systemie wieloosobowym to kwestia tygodni,
nie lat.

### M-188 · Miękkie usuwanie i kosz
Decyzja z Aneksu 18, nigdy niezamodelowana.

```sql
  deleted_at, deleted_by, delete_reason
  -- plus widok "kosz" z przywracaniem, czyszczenie po 30 dniach
```

### M-189 · Deduplikacja i scalanie encji
Ten sam kontrahent wprowadzony dwa razy. Dziś nie ma jak scalić.

```sql
merge_operation
  id, entity_type, surviving_id, merged_ids uuid[]
  field_resolution jsonb, merged_by, merged_at
  can_undo_until
```

Dotyczy: kontrahentów, kontaktów, portów własnych, kodów opłat,
członków sieci.

## Grupa 3 — Niezawodność integracji

### M-190 · Kolejka błędów integracji ⚠
Wywołanie API armatora nie powiodło się trzy razy. Co teraz?

```sql
dead_letter
  id, organization_id, source, operation
  payload jsonb, error, attempts, first_failed_at, last_attempt_at
  status,      -- pending | retrying | resolved | abandoned
  resolved_by, resolution
```

Bez tego nieudane operacje znikają. Z tym — operator widzi listę i decyduje.

### M-191 · Konfiguracja polityki ponowień
Per integracja: liczba prób, odstępy, limit czasu, przełącznik obwodu.

### M-192 · Rejestr wywołań zewnętrznych
Pełny zapis żądań i odpowiedzi do API armatorów, KSeF, wywiadowni.
Retencja krótsza niż dane biznesowe, ale konieczna przy sporze
i przy diagnozie.

## Grupa 4 — Twoja strona platformy ⚠

**To jest największy brak w tej grupie.** Zaprojektowaliśmy system dla klienta,
nigdy dla ciebie jako operatora platformy.

### M-193 · Konsola operatora platformy
```sql
platform_tenant
  organization_id, plan, status
  created_at, activated_at, suspended_at, suspension_reason
  trial_ends_at, contract_id
  health_score, last_activity_at

platform_metric
  organization_id, period
  active_users, quotations, shipments, sheets_parsed
  api_calls, storage_bytes, ai_cost
  errors_count, support_tickets
```

Widok wszystkich tenantów, ich kondycji i zużycia. Bez tego prowadzisz
firmę SaaS na wyczucie.

### M-194 · Impersonacja dla wsparcia
Klient zgłasza problem. Musisz zobaczyć jego ekran.

```sql
impersonation_session
  id, support_user_id, target_organization_id, target_user_id
  reason, ticket_ref
  started_at, ended_at, actions_performed jsonb
  customer_consent_ref
```

**Obowiązkowo z pełnym audytem i widoczne dla klienta.** Impersonacja bez
śladu to problem prawny i utrata zaufania.

### M-195 · Limity i kwoty per tenant
```sql
tenant_quota
  organization_id, resource,  -- users | sheets | api_calls | storage
  limit_value, current_usage, period
  overage_policy,   -- block | allow_charge | notify
  soft_limit_pct
```

Powiązane z rozliczaniem z M-67 i ze sprawiedliwością kolejki z M-01.

### M-196 · Zakończenie współpracy z tenantem
Klient odchodzi. Co się dzieje?

```sql
tenant_offboarding
  id, organization_id
  requested_at, data_export_id
  retention_until,     -- okres karencji przed usunięciem
  legal_holds uuid[],  -- z M-104
  anonymized_at, deleted_at
```

Eksport kompletu danych, karencja, usunięcie z uwzględnieniem obowiązków
przechowywania. To jest obietnica z części sprzedażowej — musi mieć
implementację.

### M-197 · Środowisko próbne tenanta
Kopia danych klienta na osobnej instancji do testowania zmian przed
wdrożeniem u niego. Argument sprzedażowy z M-76, brak mechanizmu.

### M-198 · Wersjonowanie konfiguracji tenanta
Klient zmienił reguły marży i coś przestało działać. Cofnięcie do
poprzedniej wersji konfiguracji bez odtwarzania bazy.

```sql
config_snapshot
  id, organization_id, taken_at, taken_by
  config jsonb, reason, restored_from_id
```

---

# PODSUMOWANIE CZĘŚCI I

| Grupa | Moduły | Nakład |
|---|---|---|
| Sterowanie i kontrola | M-179…M-183 | 14 dni |
| Dane i spójność | M-184…M-189 | 12 dni |
| Niezawodność integracji | M-190…M-192 | 6 dni |
| Strona platformy | M-193…M-198 | 16 dni |

**48 dni. Rejestr: 198 modułów.**

## Cztery, których brak zaboli najszybciej

**M-179 silnik zatwierdzeń** — potrzebny w kilkunastu miejscach, a nie ma go
nigdzie. Dodany później oznacza dopisywanie logiki akceptacji w każdym module
osobno, każdy inaczej.

**M-193 i M-194 konsola operatora z impersonacją** — bez tego przy trzecim
kliencie nie będziesz w stanie udzielić wsparcia inaczej niż prosząc o zrzuty
ekranu.

**M-184 grupy kapitałowe** — limit kredytowy liczony osobno dla trzech spółek
tego samego właściciela to realna strata pieniędzy przy pierwszym takim kliencie.

**M-190 kolejka błędów** — bez niej nieudane wywołania API armatorów znikają
bez śladu, a dowiadujesz się o tym od klienta.
---

# CZĘŚĆ II — AUDYT SYSTEMOWY

Przegląd wszystkich modułów wzdłuż sześciu wymiarów. Szukam nie nowych
modułów, tylko braków w istniejących.

---

# WYMIAR 1 — RĘCZNA KOREKTA AUTOMATU

Twój wymóg: system ma być automatem, ale musi pozwalać na ręczne dodanie
i usunięcie. **Sprawdziłem każdy moduł automatyczny. W dwunastu brakuje
drogi ręcznej.**

| Moduł | Czego brakuje |
|---|---|
| M-18 opłaty portowe | brak ręcznego dodania reguły z poziomu wyceny · brak wyłączenia reguły dla jednego zlecenia |
| M-19 stawki live | brak ręcznego wprowadzenia oferty armatora otrzymanej telefonicznie · brak edycji pobranej oferty |
| M-20 ekstrakcja | jest kolejka review, **brak możliwości ręcznego dopisania pozycji, której model nie znalazł** · brak oznaczenia cennika jako „nie parsuj, wprowadzę ręcznie" |
| M-21 wycena | brak ręcznego nadpisania wybranego wariantu · brak wymuszenia dostawcy wbrew rankingowi |
| M-24 ryzyko oferty | brak ręcznego ustawienia poziomu ryzyka z uzasadnieniem |
| M-28 zapytania klientów | brak ręcznego przypisania maila do istniejącego zapytania · brak rozdzielenia jednego maila na dwa zapytania |
| M-30 zapytania do agentów | brak ręcznego wprowadzenia odpowiedzi otrzymanej telefonicznie · brak zamknięcia zapytania bez odpowiedzi |
| M-36 tracking | **brak ręcznego dodania zdarzenia** — armator nie zawsze wysyła, operator wie z telefonu |
| M-41 rozliczenie faktur | brak ręcznego dopasowania pozycji, gdy automat nie trafił · brak oznaczenia rozbieżności jako zaakceptowanej |
| M-43 koszt kapitału | brak ręcznego nadpisania terminu płatności dla jednego zlecenia |
| M-53 sankcje | jest zwolnienie trafienia, **brak ręcznego dodania podmiotu do obserwacji** |
| M-90 rezerwy | brak ręcznego utworzenia i zamknięcia rezerwy |

## Wzorzec do wprowadzenia globalnie

```sql
-- na każdej encji tworzonej automatycznie
  created_source,      -- auto | manual | imported | corrected
  is_manually_overridden bool,
  override_reason text,
  overridden_by, overridden_at,
  original_value jsonb        -- co proponował automat
```

Plus reguła w interfejsie: **każda wartość wyliczona automatycznie ma
ikonę edycji.** Kliknięcie otwiera pole z prośbą o uzasadnienie. Automat
przestaje nadpisywać wartość ustawioną ręcznie, dopóki użytkownik nie cofnie.

Plus reguła odwrotna: **każda wartość ustawiona ręcznie ma przycisk
„przelicz automatycznie"** z podglądem, co się zmieni.

---

# WYMIAR 2 — BRAKUJĄCE ODNIESIENIA W BAZIE

Przeszedłem model danych szukając powiązań, które powinny istnieć i nie ma ich.

## Odniesienia krytyczne

| Encja | Brakujące powiązanie | Skutek braku |
|---|---|---|
| `quotation` | `rfq_id` jest, brak `customer_tariff_id` | nie wiadomo, czy oferta z cennika czy liczona |
| `quotation_line` | brak `port_charge_rule_id` | nie wiadomo, która reguła dała tę opłatę |
| `rate_line` | brak `rate_request_recipient_id` | nie wiadomo, z którego zapytania pochodzi stawka |
| `shipment_charge` | brak `cost_accrual_id` | rezerwa nie łączy się z kosztem rzeczywistym |
| `invoice_line` | brak wymuszonego `shipment_charge_id` | nie da się prześledzić faktury do pozycji zlecenia |
| `bill` | brak `carrier_order_id` i `booking_id` | faktura nie łączy się ze zleceniem do podwykonawcy |
| `party` | brak `parent_party_id` | patrz M-184 |
| `app_user` | brak `legal_entity_id` | nie wiadomo, w której spółce pracuje |
| `charge_code` | brak `account_code` | eksport księgowy wymaga ręcznego mapowania |
| `port` | brak `country_code` jako klucza obcego, brak `timezone` | liczenie cut-offów w złej strefie |
| `shipment` | brak `booking_id` po dodaniu M-89 | dwa źródła prawdy o rejsie |
| `document` | brak `language` | nie wiadomo, w jakim języku wygenerowano |
| `payment` | brak `legal_entity_id` | przy wielu podmiotach nie wiadomo, kto otrzymał |
| `contact_suggestion` | brak `inbound_message_id` jako klucza obcego | nie da się wrócić do źródła |
| `screening_hit` | brak `decision_log_id` | brak śladu, dlaczego zwolniono |

## Brakujące tabele referencyjne

```sql
currency                    -- nie ma jej wcale
  code, name, decimals, symbol, is_active
  -- JPY ma 0 miejsc, KWD ma 3 — bez tej tabeli zaokrąglasz źle

country
  code, name_pl, name_en, iso3, region
  is_eu, customs_zone, currency_code, timezone_default
  requires_ens, requires_ams

language
  code, name, is_rtl, date_format, number_format
```

## Brakujące indeksy — do sprawdzenia w migracjach

```
rate_line       (organization_id, pol, pod, mode, valid_to) WHERE superseded_by IS NULL
shipment_event  (shipment_id, event_datetime DESC)
inbound_message (organization_id, received_at DESC, classification)
audit_log       (organization_id, entity_type, entity_id, at DESC)
outbox          (published_at) WHERE published_at IS NULL
shipment_charge (shipment_id, charge_code)
approval_request(approver_role_id, status) WHERE status = 'pending'
```

Ostatni jest istotny: lista „do zatwierdzenia" musi być natychmiastowa,
bo użytkownik patrzy na nią kilkanaście razy dziennie.

---

# WYMIAR 3 — BRAKUJĄCE STANY I PRZEJŚCIA

Maszyna stanów jest zaprojektowana tylko dla zlecenia. Reszta encji ma
statusy bez zdefiniowanych przejść.

| Encja | Brakujące stany |
|---|---|
| `rfq` | brak `on_hold` (klient prosi o wstrzymanie), brak `superseded` (klient przysłał nowe) |
| `quotation` | brak `pending_approval`, brak `withdrawn` (my wycofujemy), brak `revised` |
| `rate_sheet` | brak `partially_active` (część pozycji zaakceptowana), brak `disputed` |
| `booking` | brak `pending_carrier_confirmation`, brak `waitlisted` |
| `invoice` | brak `pending_approval`, brak `disputed`, brak `partially_paid` |
| `claim` | brak `awaiting_documents`, brak `with_insurer`, brak `time_barred` |
| `credit_assessment` | brak `pending_review`, brak `expired` |
| `customs_declaration` | brak `amendment_requested` |

## Brakujące przejścia zbiorcze

Nie ma mechanizmu zmiany stanu wielu encji naraz z jedną walidacją:
zamknięcie miesiąca, masowe wygaszenie ofert, zbiorcze zatwierdzenie stawek,
przypisanie zleceń innemu operatorowi przy urlopie.

---

# WYMIAR 4 — BRAKUJĄCE AUTOMATYZACJE

Automatyzacje, które wynikają z modelu, ale nie zostały nazwane.

| Automatyzacja | Wyzwalacz | Czego dotyczy |
|---|---|---|
| Wygaszanie ofert | data ważności | M-21 |
| Zamykanie zleceń | dostarczone + wszystkie faktury | M-35 |
| Zwalnianie rezerw | faktura dopasowana | M-90 |
| Archiwizacja | po okresie retencji | M-104 |
| Odświeżanie stawek live | wygaśnięcie TTL | M-19 |
| Ponowne odpytanie agenta | brak odpowiedzi po terminie | M-30 |
| Eskalacja zadań | przekroczony termin | M-108 |
| Przeliczenie punktacji agentów | co tydzień | M-13 |
| Przeliczenie DSO i DPO | co miesiąc | M-43 |
| Aktualizacja kursów | codziennie 12:15 | M-07 |
| Sprawdzenie białej listy | przed każdą płatnością | M-10 |
| Weryfikacja certyfikatów rezydencji | co miesiąc | M-109 |
| Sprawdzenie terminów dokumentów pojazdów | codziennie | M-111 |
| Wykrycie przedawnień | codziennie | M-55, M-115 |
| Przeliczenie prowizji | po zapłacie faktury | M-101 |
| Odświeżenie widoków materializowanych | zmiana cennika | M-21 |
| Czyszczenie kosza | po 30 dniach | M-188 |
| Test odtworzenia kopii | co tydzień | M-96 |

**Każda z nich potrzebuje:** konfiguracji per tenant (M-183), trybu próbnego
(M-182), rejestru wykonań, możliwości ręcznego uruchomienia i wyłączenia.

---

# WYMIAR 5 — BRAKUJĄCE INFORMACJE

Pola, których brak odkryjesz dopiero przy pierwszym pytaniu klienta.

## Na zleceniu

```
□ numer referencyjny klienta (jego numer zamówienia)
□ numer referencyjny agenta
□ centrum kosztów klienta
□ osoba kontaktowa po stronie klienta dla tego zlecenia
□ priorytet i powód priorytetu
□ powiązanie ze zleceniem nadrzędnym (przesyłki dzielone)
□ powiązanie ze zleceniem powrotnym
□ wartość towaru i waluta (do ubezpieczenia i odprawy)
□ warunki płatności frachtu: prepaid / collect
□ czy dopuszczalny przeładunek
□ czy dopuszczalna wysyłka częściowa
```

## Na kontrahencie

```
□ preferowany sposób komunikacji i język
□ godziny pracy i strefa czasowa
□ dni wolne specyficzne dla klienta
□ wymagane dokumenty przy każdym zleceniu
□ zakazane relacje albo armatorzy
□ standardowe instrukcje dokumentacyjne
□ NIP-y powiązanych spółek (M-184)
□ status weryfikacji sankcyjnej i data
```

## Na stawce

```
□ warunki i zastrzeżenia w oryginalnym brzmieniu
□ minimalna i maksymalna ilość
□ czy podlega negocjacji
□ osoba kontaktowa u dostawcy dla tej stawki
□ czy wymaga wcześniejszego potwierdzenia
```

## Na ofercie

```
□ warunki płatności zaproponowane klientowi
□ okres ważności z uzasadnieniem
□ założenia przyjęte przy wycenie (do sporu)
□ co NIE jest zawarte w cenie — jawnie
□ osoba przygotowująca i zatwierdzająca
```

**Pozycja „co nie jest zawarte w cenie" jest najważniejsza z całej listy.**
Większość sporów z klientami dotyczy tego, czy coś było w ofercie. Jawna
lista wyłączeń na PDF eliminuje je niemal całkowicie.

---

# WYMIAR 6 — BRAKUJĄCE POWIĄZANIA MIĘDZY MODUŁAMI

Miejsca, gdzie moduły powinny się komunikować, a projekt tego nie przewiduje.

| Od | Do | Czego brakuje |
|---|---|---|
| M-53 sankcje | M-21 wycena | trafienie sankcyjne powinno blokować wystawienie oferty |
| M-14 ocena kredytowa | M-35 zlecenie | przekroczony limit blokuje booking |
| M-37 wyjątki | M-74 bliźniak kosztu | rollover automatycznie koryguje prognozę marży |
| M-61 dane rynkowe | M-92 cenniki klientów | GRI wywołuje przegląd cenników sprzedażowych |
| M-41 rozbieżności | M-13 karta wyników | rozbieżność obniża ocenę agenta |
| M-90 rezerwy | M-46 koszt obsługi | rezerwa wchodzi do rentowności klienta |
| M-99 odprawy | M-53 sankcje | kod TARIC sprawdzany wobec kontroli eksportu |
| M-102 ubezpieczenie | M-55 reklamacje | szkoda uruchamia zgłoszenie do ubezpieczyciela |
| M-111 kierowcy | M-48 alokacja | czas pracy ogranicza możliwe przydziały |
| M-87 windykacja | M-14 limit kredytowy | opóźnienie obniża limit automatycznie |
| M-25 wynik oferty | M-03 reguły marży | przegrane oferty korygują reguły |
| M-20 ekstrakcja | M-18 opłaty portowe | nowa opłata w cenniku tworzy regułę warunkową |

**Wzorzec:** wszystkie te powiązania powinny iść przez outbox i zdarzenia,
nie przez bezpośrednie wywołania. Inaczej moduły przestają być niezależne
i `import-linter` zacznie blokować.

```
sanctions.hit_detected → quotation.block
credit.limit_exceeded → booking.block
tracking.rollover_detected → margin_forecast.recalculate
market.gri_announced → customer_tariff.review_required
```
---

# CZĘŚĆ III — DRUGI AUDYT KRYTYCZNY

Przeszedłem projekt jeszcze raz, tym razem szukając nie braków, ale
**błędów i sprzeczności**. Znalazłem osiem.

## B-01 · Sprzeczność: niemutowalność stawek a korekta ręczna ⚠

Zasada 6 mówi: stawki są niemutowalne, zmiana to nowy rekord. Twój wymóg
mówi: musi być możliwość ręcznej edycji i usunięcia.

**To się wyklucza** i nie zauważyłem tego wcześniej.

**Rozstrzygnięcie:** niemutowalność dotyczy stawek **zweryfikowanych i użytych
w ofercie**. Stawka w kolejce review albo nieużyta jeszcze nigdzie jest
edytowalna normalnie. Po pierwszym użyciu w ofercie — tylko przez nowy rekord.

```sql
-- rate_line
  is_locked bool,        -- ustawiane przy pierwszym użyciu w quotation
  locked_at, locked_by_quotation_id
```

Usunięcie stawki użytej w ofercie: miękkie, z zachowaniem powiązania.

## B-02 · Silnik wyceny w SQL a konfigurowalność reguł

Zasada 11 każe liczyć w SQL. Zasada 2 każe trzymać reguły jako dane.
**Reguły marży jako dane, przetwarzane w SQL, to funkcja SQL generująca
zapytanie na podstawie danych** — czyli konstrukcja trudna do testowania
i debugowania.

**Rozstrzygnięcie:** rozdziel etapy. Dobór kandydatów w SQL (to jest
filtrowanie po dużym zbiorze). Kaskada narzutów w Pythonie (to jest kilkanaście
reguł na kilkunastu pozycjach — Python jest tu wystarczający i czytelniejszy).

Poprawka do zasady 11: *nie licz w Pythonie tego, co Postgres policzy z indeksem
**na dużym zbiorze***. Kaskada na dwudziestu pozycjach nie jest dużym zbiorem.

## B-03 · Provenance a RODO

Zasada 5 wymaga zachowania `source_ref` z plikiem źródłowym.
M-56 wymaga usuwania danych po okresie retencji.

Plik źródłowy cennika może zawierać dane osobowe (podpis, kontakt).
**Usunięcie pliku po retencji zrywa provenance stawek, które nadal
obowiązują.**

**Rozstrzygnięcie:** rozdziel plik od metadanych. Po retencji usuwasz plik,
zachowujesz `source_ref` z hashem, nazwą arkusza, wierszem i kolumną oraz
wyciągiem tekstowym pozycji. Provenance zostaje, dane osobowe znikają.

## B-04 · Automatyczna wysyłka a zatwierdzenia

M-03 przewiduje tryb `auto` wysyłający oferty bez człowieka.
M-179 wprowadza zatwierdzenia dla ofert poniżej progu marży.

**Co ma pierwszeństwo?** Nie zdefiniowaliśmy.

**Rozstrzygnięcie:** zatwierdzenie zawsze wygrywa. Oferta wymagająca akceptacji
nie idzie automatycznie, tylko trafia do kolejki — niezależnie od polityki
automatyzacji. Warunki `auto_quote_policy` muszą jawnie wykluczać przypadki
wymagające zatwierdzenia.

## B-05 · Karta wyników agenta a jego reprezentacja

M-13 ocenia agenta na podstawie odpowiedzi. M-184 wprowadza grupy kapitałowe.
**Agent działający przez trzy spółki dostaje trzy oceny.**

**Rozstrzygnięcie:** punktacja liczona na poziomie grupy, prezentowana
na poziomie podmiotu z adnotacją o grupie.

## B-06 · Ekspozycja walutowa a rezerwy

M-44 liczy ekspozycję z otwartych zleceń. M-90 wprowadza rezerwy na koszty
niezafakturowane. **Rezerwa w walucie obcej to ekspozycja, której M-44
nie widzi**, bo nie ma jeszcze zobowiązania.

**Rozstrzygnięcie:** `cost_accrual` wchodzi do wyliczenia ekspozycji netto
z oznaczeniem jako pozycja szacunkowa.

## B-07 · Widoczność kosztów a rozliczenie faktur

M-100 ukrywa koszty przed handlowcem. M-41 pokazuje rozbieżności między
wyceną a fakturą — **czyli koszty**.

**Rozstrzygnięcie:** raport rozbieżności widoczny wyłącznie dla ról
z `cost_visibility = full`. Handlowiec widzi jedynie flagę „to zlecenie
ma nierozliczoną rozbieżność" bez kwot.

## B-08 · Wielojęzyczność a słownik opłat

M-06 przewiduje `name_pl` i `name_en`. M-84 wymaga wydruków w języku klienta.
**Cztery języki w aliasach, dwa w nazwach.**

**Rozstrzygnięcie:** `charge_code` bez kolumn językowych, nazwy w tabeli
`translation` z M-79. Wtedy dodanie języka to dane, nie migracja.

---

# CZĘŚĆ IV — WZORCE DO WPROWADZENIA GLOBALNIE

Zamiast poprawiać moduł po module, wprowadź siedem wzorców obowiązujących
wszędzie. To jest tańsze i spójniejsze.

## W-01 · Wzorzec pochodzenia i korekty

```sql
  created_source,          -- auto | manual | imported | corrected
  is_manually_overridden bool,
  override_reason, overridden_by, overridden_at,
  original_value jsonb
```

Na każdej encji tworzonej albo wyliczanej automatycznie.

## W-02 · Wzorzec cyklu życia

```sql
  status, status_changed_at, status_changed_by
  deleted_at, deleted_by, delete_reason
  version integer          -- blokada optymistyczna
```

Plus zdefiniowana maszyna stanów dla każdej encji ze statusem, nie tylko
dla zlecenia.

## W-03 · Wzorzec datowania

```sql
  effective_from, effective_to
  supersedes_id, superseded_by_id
```

Na wszystkich danych referencyjnych i konfiguracyjnych.

## W-04 · Wzorzec powiązań zewnętrznych

```sql
  -- przez tabelę external_reference (M-185), nie kolumny na encji
```

## W-05 · Wzorzec wyjaśnialności

Każda wartość wyliczona automatycznie ma wpis w `decision_log` (M-181)
i przycisk „dlaczego" w interfejsie.

## W-06 · Wzorzec zdarzeniowy między modułami

Komunikacja wyłącznie przez outbox. Nazewnictwo: `modul.zdarzenie_w_czasie_przeszłym`.
Konsument deklaruje subskrypcję, producent nie wie o konsumentach.

## W-07 · Wzorzec zatwierdzenia

Każda operacja o skutku finansowym powyżej progu przechodzi przez
`approval_request` (M-179). Progi konfigurowalne per tenant.

---

# PODSUMOWANIE AUDYTU

| Wymiar | Znalezione braki |
|---|---|
| Ręczna korekta automatu | **12 modułów bez drogi ręcznej** |
| Odniesienia w bazie | 15 brakujących powiązań, 3 brakujące tabele referencyjne, 7 indeksów |
| Stany i przejścia | 8 encji bez pełnego zestawu stanów, brak operacji zbiorczych |
| Automatyzacje | 18 nienazwanych |
| Informacje | ~35 brakujących pól w czterech obszarach |
| Powiązania międzymodułowe | 12 brakujących przepływów zdarzeń |
| **Sprzeczności** | **8 błędów projektowych** |

## Nakład na usunięcie braków

| Zakres | Dni |
|---|---|
| 20 mechanizmów przekrojowych (M-179…M-198) | 48 |
| 7 wzorców globalnych wprowadzonych w fazie 0 | 8 |
| Uzupełnienie ręcznej korekty w 12 modułach | 12 |
| Brakujące odniesienia i indeksy | 4 |
| Uzupełnienie stanów i przejść | 6 |
| Nazwanie i konfiguracja 18 automatyzacji | 9 |
| Brakujące pola informacyjne | 5 |
| Zdarzenia międzymodułowe | 7 |
| Poprawa 8 sprzeczności | 6 |
| **Razem** | **105 dni** |

## Trzy rzeczy do zrobienia natychmiast

**① Siedem wzorców globalnych w fazie 0.** Osiem dni. Wprowadzone później
oznaczają migrację stu trzydziestu tabel.

**② Rozstrzygnięcie ośmiu sprzeczności jako ADR.** Sześć dni, ale najpierw
decyzja — każda z nich będzie wracać przy implementacji, jeśli jej nie
zapiszesz.

**③ Wzorzec ręcznej korekty jako element definicji ukończenia.** Dopisz do
`AGENTS.md`: *żaden plaster z automatyzacją nie jest ukończony bez drogi
ręcznej i przycisku „przelicz automatycznie".*

To ostatnie jest najważniejsze, bo zapobiega powstawaniu tego samego braku
w kolejnych modułach. Reszta to nadrabianie, ta jedna zasada to profilaktyka.
