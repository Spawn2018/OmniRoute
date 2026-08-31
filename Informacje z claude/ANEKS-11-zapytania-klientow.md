# Aneks 11 — Zapytania od klientów: pełna automatyzacja

---

## 1. Dlaczego to trudniejsze niż przy agentach

| | Agenci | Klienci |
|---|---|---|
| Kto zaczyna wątek | ty | klient |
| Jak znaleźć wiadomość | znasz `conversationId` | musisz jej szukać |
| Dostęp do skrzynki | tylko własne wątki | szerszy |
| Co może zawierać | prawie zawsze stawki | cokolwiek |
| Koszt pomyłki | niski | **wysoki — zaśmiecony system** |

Ostatni wiersz jest najważniejszy. Odpowiedź agenta na twoje zapytanie to niemal na pewno cennik. Mail od klienta to może być zapytanie, reklamacja, pytanie o fakturę, dokument do zlecenia, zmiana bookingu albo życzenia świąteczne. **Jeśli system zrobi zapytanie ofertowe z każdego maila, użytkownicy wyłączą funkcję w tydzień.**

## 2. Cztery ścieżki wejścia

### A. Dedykowany adres — najczystsza, najmniej używana

`oferty@spedytor.pl`, publikowany na stronie i w stopkach. Pełny dostęp bez żadnych wątpliwości prywatnościowych.

Problem: klienci piszą do swojego handlowca, nie na adres ogólny. Zadziała dla nowych zapytań ze strony, nie dla stałych relacji.

### B. Filtr po domenach znanych klientów — **rekomendowana**

System odpytuje skrzynkę wyłącznie o wiadomości od nadawców, których domeny są w `party_email_domain` z rolą klienta. Nie widzi niczego innego — ani rozmów z bankiem, ani prywatnych, ani wewnętrznych.

To jest chirurgiczne i sprzedaje się tak samo dobrze jak model z Aneksu 10: **„widzimy wyłącznie korespondencję od waszych klientów, których sami wprowadziliście do systemu"**.

Ograniczenie: nowy klient, którego domeny jeszcze nie znasz, przepada. Rozwiązanie w sekcji 6.

### C. Folder z regułą — dla klientów wrażliwych na dostęp

Reguła w Outlooku kopiuje do folderu `Spedycja/Zapytania` wiadomości spełniające warunek (nadawca z listy, słowa kluczowe, załącznik). System czyta tylko ten folder. Regułę da się utworzyć programowo przy podłączaniu konta.

### D. Dodatek do Outlooka — uzupełnienie, nie podstawa

Przycisk „Zarejestruj jako zapytanie" dla przypadków, które przeszły przez sito.

**Rekomendacja: B jako domyślna, A równolegle, C dla klientów z restrykcyjnym IT, D później.**

## 3. Klasyfikacja musi być wieloklasowa

To jest sedno działającej automatyzacji. Nie pytasz „czy to zapytanie ofertowe", tylko „czym to jest".

| Klasa | Akcja | Wartość |
|---|---|---|
| **Nowe zapytanie** | utwórz `rfq` | podstawowa |
| **Akceptacja oferty** | zmień status, przygotuj booking | **najwyższa** |
| **Negocjacja oferty** | dopnij do `quotation`, oznacz do reakcji | wysoka |
| **Dopytanie o zlecenie** | dopnij do `shipment`, powiadom operatora | wysoka |
| **Dokumenty do zlecenia** | wyciągnij załączniki do `shipment_document` | wysoka |
| **Sprawa finansowa** | dopnij do faktury | średnia |
| **Reklamacja** | utwórz zgłoszenie | średnia |
| **Inne** | zignoruj, ale zapamiętaj do nauki | — |

**Wykrywanie akceptacji oferty jest najcenniejszą klasą i nikt o niej nie myśli.** Klient odpisuje „ok, proszę bookować" — dziś to zależy od tego, czy handlowiec zauważy maila w piątek po południu. Zautomatyzowane wykrycie plus alert skraca czas do bookingu i eliminuje najdroższą pomyłkę operacyjną, jaka istnieje: przegapioną akceptację.

Klasyfikacja odbywa się w dwóch krokach — najpierw kod (czy wiadomość jest odpowiedzią w wątku znanej oferty? czy zawiera numer zlecenia?), potem model dla reszty. Kontekst wątku rozstrzyga większość przypadków bez sięgania po model.

## 4. Ekstrakcja zapytania

Ten sam pipeline co przy cennikach, inny schemat wyjściowy.

```json
{
  "enquiry_type": "new_quote",
  "lanes": [{
    "origin_raw": "Gdynia",
    "destination_raw": "Callao",
    "mode_raw": "FCL",
    "equipment_raw": "2x40HC",
    "commodity_raw": "meble drewniane",
    "hs_code": null,
    "incoterm_raw": "FOB",
    "ready_date_raw": "połowa września",
    "weight_kg": null,
    "volume_cbm": null,
    "special_requirements": []
  }],
  "customer_deadline": null,
  "attachments_relevant": ["packing_list.xlsx"],
  "missing_critical": ["gross_weight", "hs_code"],
  "unparsed_regions": [],
  "language": "pl"
}
```

**Cztery rzeczy, które muszą działać:**

**Wiele relacji w jednym mailu.** Klient pyta o pięć kierunków naraz — to jedno `rfq` z pięcioma pozycjami, nie pięć osobnych zapytań i nie jedno z pierwszą relacją.

**Załączniki jako źródło danych.** Packing list i faktura handlowa zawierają wagę, objętość, opis towaru i kod HS — czyli dokładnie to, czego brakuje w treści maila. Przepuść je przez ten sam ekstraktor.

**Wiele języków.** Klienci piszą po polsku, angielsku i niemiecku, często mieszając.

**Daty nieprecyzyjne.** „Połowa września", „za dwa tygodnie", „ASAP" — normalizuj do zakresu dat, nie do jednej daty, i oznacz jako przybliżone.

## 5. Progi pewności — funkcja stoi albo upada na tym

```
pewność ≥ 0,90   → automatyczne utworzenie rfq, powiadomienie handlowca
0,60 – 0,90      → skrzynka propozycji, jedno kliknięcie do zatwierdzenia
< 0,60           → nic się nie dzieje, wiadomość oznaczona do nauki
```

**Skrzynka propozycji jest ważniejsza od automatu.** Wygląda tak:

```
PROPOZYCJE (4)

📧 od: anna.nowak@meblexport.pl                            87%
   „potrzebuję stawki na dwa kontenery do Peru na wrzesień"
   → Nowe zapytanie · Gdynia → Callao · 2×40HC
   [ Utwórz zapytanie ]  [ To nie jest zapytanie ]  [ Edytuj ]

📧 od: k.wisniewski@aludrew.com                            72%
   „czy możemy dostać lepszą cenę na tej ofercie?"
   → Negocjacja oferty OF/2026/00913
   [ Dopnij do oferty ]  [ To co innego ]
```

Każde „to nie jest zapytanie" trafia do zbioru uczącego. Po dwustu decyzjach próg 0,90 przepuszcza znacznie więcej, bo klasyfikator zna specyfikę tego klienta.

## 6. Nieznany nadawca to nie szum, to lead

Mail z nieznanej domeny z zapytaniem o transport to **potencjalny nowy klient**. Nie ignoruj.

```sql
lead
  id, organization_id
  from_email, from_domain, company_name_extracted
  rfq_id NULL, source,          -- email | website | referral
  status,                        -- new | qualified | converted | rejected
  krs_lookup jsonb,             -- automatyczne dociągnięcie z KRS po nazwie
  created_at
```

Automatycznie: wyszukanie firmy w KRS po nazwie ze stopki, podstawowa weryfikacja, karta leada w skrzynce propozycji. Handlowiec decyduje, czy założyć kontrahenta.

Wymaga to jednak dostępu szerszego niż filtr po znanych domenach z punktu 2B — czyli dedykowanego adresu z punktu 2A. To jest właśnie powód, dla którego warto mieć oba kanały.

## 7. Duplikaty

Klient wysyła to samo do dwóch handlowców albo ponawia po trzech dniach. Wykrywanie: ten sam nadawca lub domena, ta sama relacja, okno 7 dni, podobieństwo treści.

Efekt: jedno `rfq` z dwoma źródłami, a nie dwie równoległe wyceny wysyłane temu samemu klientowi z różnymi cenami. Ta pomyłka zdarza się realnie i kosztuje wiarygodność.

## 8. Trzy poziomy automatyzacji

Tu jest odpowiedź na „pełen automat" — z zastrzeżeniem, że dochodzi się do niego stopniowo.

### Poziom 1 — zapytanie tworzy się samo *(od początku)*
Mail wpada, `rfq` jest gotowe, handlowiec widzi je w kolejce z podświetlonymi brakami. Wycenia ręcznie.

### Poziom 2 — oferta przygotowuje się sama *(po pipeline stawek)*
System dociąga stawki z bazy, sprawdza spot, wykrywa braki, nakłada regułę marży i przygotowuje **projekt oferty**. Handlowiec sprawdza, poprawia, wysyła. Czas do oferty spada z godzin do minut.

### Poziom 3 — oferta wychodzi sama *(z regułami)*
Tu jest funkcja, której nie ma nikt na rynku — i tu potrzebne są twarde bezpieczniki.

```sql
auto_quote_policy
  id, organization_id
  customer_party_id NULL,        -- NULL = reguła ogólna
  is_enabled
  max_quote_value,               -- sufit kwotowy
  allowed_lanes jsonb,
  require_rate_max_age_days,     -- np. tylko stawki świeższe niż 14 dni
  require_verified_rate,         -- tylko zweryfikowane przez człowieka
  min_margin_pct,                -- nie schodzi poniżej
  exclude_dangerous_goods,
  exclude_new_customers,
  require_complete_enquiry,      -- brak pól krytycznych
  daily_cap,                     -- ile ofert dziennie automatycznie
  cc_salesperson                 -- zawsze kopia do handlowca
```

Reguła brzmi: **automat działa tylko wtedy, gdy wszystko jest znane i bezpieczne.** Znany klient, relacja z listy, świeża zweryfikowana stawka, komplet danych w zapytaniu, marża powyżej progu, wartość poniżej sufitu, brak ładunku niebezpiecznego. Cokolwiek odbiega — trafia do człowieka.

Efekt w praktyce: klient pisze o 22:15, oferta wychodzi o 22:16. Konkurencja odpowiada nazajutrz po południu. **Na powtarzalnych relacjach ze stałymi klientami to jest przewaga, której nie da się dogonić organizacyjnie.**

Włączaj per klient, zaczynając od jednego lojalnego, na jednej relacji, z niskim sufitem. Rozszerzaj, gdy statystyki potwierdzą, że działa.

## 9. Model danych

```sql
inbound_message
  id, organization_id
  source_channel,               -- shared_mailbox | user_mailbox | web_form
  message_id, conversation_id
  from_email, from_name, to_email, subject
  received_at, raw_path
  matched_party_id NULL
  classification,               -- klasy z sekcji 3
  classification_confidence
  linked_entity_type, linked_entity_id
  status,                       -- auto_processed | proposed
                                -- confirmed | dismissed
  reviewed_by, reviewed_at

classification_feedback         -- pętla uczenia
  id, inbound_message_id
  predicted_class, actual_class, corrected_by, corrected_at
```

## 10. Metryki, które trzeba mierzyć od pierwszego dnia

- **Trafność klasyfikacji** per klasa — bez tego nie wiesz, czy podnosić próg
- **Odsetek automatyczny** — ile zapytań powstało bez człowieka
- **Fałszywe pozytywy** — ile utworzonych zapytań odrzucono. To jest metryka zaufania i najważniejsza z całej listy
- **Czas od wpłynięcia do utworzenia** — powinien być liczony w sekundach
- **`time_to_quote`** — łącznie, przed i po

Jeśli fałszywe pozytywy przekroczą kilka procent, podnieś próg i pogódź się z mniejszą automatyzacją. Zaufanie do funkcji odbudowuje się miesiącami.

## 11. Kolejność

| Etap | Zakres | Dni |
|---|---|---|
| 1 | Dedykowany adres + web formularz → `rfq` | 3 |
| 2 | Filtr po domenach znanych klientów | 3 |
| 3 | Klasyfikator wieloklasowy + skrzynka propozycji | 5 |
| 4 | Ekstrakcja: wiele relacji, załączniki, języki, daty | 4 |
| 5 | Wykrywanie akceptacji oferty i negocjacji | 3 |
| 6 | Duplikaty i leady z KRS | 3 |
| 7 | Poziom 2: automatyczny projekt oferty | 5 |
| 8 | Pętla uczenia z korekt użytkownika | 3 |
| 9 | Poziom 3: `auto_quote_policy` | 5 |

Etap 5 zrób wcześniej, niż wynika z kolejności, jeśli tylko będzie okazja. Przegapiona akceptacja oferty to najdroższa pojedyncza pomyłka operacyjna w spedycji, a wykrycie jej jest technicznie prostsze niż cała reszta tego aneksu.
