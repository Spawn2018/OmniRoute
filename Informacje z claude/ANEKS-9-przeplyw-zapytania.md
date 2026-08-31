# Aneks 9 — Przepływ zapytania: od klienta do agentów

Doprecyzowanie na podstawie wymagań. Zastępuje część 1 Aneksu 3 w zakresie interfejsu i wysyłki.

---

## 1. Korekta wcześniejszej rekomendacji

W Aneksie 8 sugerowałem limit odbiorców. **To było błędne dla przypadku, który opisujesz.**

Rozróżnienie, którego nie zrobiłem wyraźnie:

| | Efekt |
|---|---|
| Jeden mail, trzydzieści adresów w kopii | Agent widzi, że jest jednym z trzydziestu. Odpowiada wolniej, gorzej albo wcale |
| Trzydzieści indywidualnych, spersonalizowanych maili | Agent widzi zapytanie skierowane do niego. Odpowiada normalnie |

Przy indywidualnej wysyłce „zaznacz wszystkich" jest funkcją właściwą. Zostaje wyłącznie problem dostarczalności — techniczny, rozwiązywalny, opisany w sekcji 6.

---

## 2. Pełny przepływ

```
┌─ WEJŚCIE ─────────────────────────────────────────────────┐
│  A. Mail od klienta na dedykowaną skrzynkę                 │
│  B. Rejestracja ręczna przez handlowca po rozmowie         │
│     lub spotkaniu                                          │
└───────────────────────┬───────────────────────────────────┘
                        ▼
             ROZPOZNANIE I STRUKTURYZACJA
             → rfq + completeness_score + missing_fields
                        ▼
┌─ EKRAN ZAPYTANIA ─────────────────────────────────────────┐
│                                                            │
│  Gdynia → Callao · 2×40HC · meble · gotowość 15.09        │
│  Klient: [nazwa]        Kompletność: 85%                  │
│  ⚠ Brak: kod HS                                            │
│                                                            │
│  ┌── CO JUŻ MAM ──────────────────────────────────────┐   │
│  │ Cennik agenta Andes Cargo   2 340 USD   19 dni temu │   │
│  │ Cennik armatora Hapag       2 510 USD   34 dni temu │   │
│  │ ⚠ obie stawki bez opłat lokalnych w Callao          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                            │
│  [ Sprawdź stawki spot ]     ← API armatorów, na żądanie  │
│  [ Wyślij zapytanie do agentów ]  ← 34 agentów w Peru     │
│  [ Dopytaj klienta o kod HS ]                              │
│                                                            │
└───────────────────────┬───────────────────────────────────┘
                        ▼
             OKNO WYBORU AGENTÓW
                        ▼
             PODGLĄD SPERSONALIZOWANYCH MAILI
                        ▼
             WYSYŁKA INDYWIDUALNA
                        ▼
             ODBIÓR → EKSTRAKCJA → PORÓWNANIE → OFERTA
```

## 3. Wejście B — rejestracja ręczna

Handlowiec wraca ze spotkania albo kończy rozmowę. Trzy sposoby, wszystkie prowadzą do tego samego `rfq`:

**Formularz szybkiego wpisu** — minimum pól, reszta uzupełniana z historii klienta. Relacja, ładunek, gotowość, incoterm. Trzydzieści sekund.

**Wklejenie tekstu** — handlowiec wkleja notatkę ze spotkania albo fragment rozmowy. Ten sam ekstraktor co przy mailach wyciąga strukturę.

**Notatka głosowa** — nagranie z telefonu po wyjściu od klienta, transkrypcja, ekstrakcja. Dla handlowca w terenie to jedyny sposób, który faktycznie zostanie użyty. Wykorzystuje `faster-whisper` z katalogu, dobrze radzi sobie z polskim.

```sql
rfq
  ...
  input_method,     -- email | manual_form | pasted_text | voice_note
  raw_input_path,   -- nagranie albo oryginalny mail w MinIO
  registered_by     -- handlowiec, jeśli wpis ręczny
```

Wpis ręczny ma tę samą wagę co mailowy: liczy się do `time_to_quote`, do statystyk klienta i do mapy pokrycia.

## 4. Okno wyboru agentów

Otwiera się po kliknięciu, z filtrem ustawionym automatycznie na kraj portu docelowego z zapytania.

```
WYŚLIJ ZAPYTANIE — Gdynia → Callao (Peru)

Filtr:  [Peru ▾] [FCL ▾] [wszystkie sieci ▾]        34 agentów

☑ Andes Cargo SAC            WCA        Lima
  8 zapytań · odp. 3,2 h · najtańszy 5/8 · zgodność 100%
  
☑ Pacific Forwarding Peru    WCA, Globalia   Callao
  4 zapytania · odp. 6,8 h · ⚠ raz dopłata spoza oferty
  
☑ TransAndina Logistics      JCtrans    Lima
  brak historii
  
☐ Callao Marine Services     Conqueror  Callao
  2 zapytania · brak odpowiedzi
  
  ... 30 więcej

[ Zaznacz sugerowanych (3) ]  [ Zaznacz wszystkich (34) ]  [ Wyczyść ]

Wybrano: 3        Termin odpowiedzi: [48 h ▾]
                  Przypomnienie po: [24 h ▾]

                              [ Podgląd maili ]  [ Wyślij ]
```

**Sortowanie domyślne:** agenci z historią przed nowymi, w obrębie historii — po wyniku z karty wyników. Agenci, którzy nie odpowiedzieli na dwa ostatnie zapytania, na końcu i niezaznaczeni.

**„Zaznacz sugerowanych"** wybiera na podstawie relacji, nie tylko kraju — agent, który był konkurencyjny na Ameryce Zachodniej, ma pierwszeństwo przed tym, który obsługuje tylko Atlantyk.

**„Zaznacz wszystkich"** dostępne bez ograniczeń. Przy dużej liczbie system pokazuje informację o rozłożeniu wysyłki w czasie, a nie ostrzeżenie.

## 5. Personalizacja — jak ma wyglądać

Każdy agent dostaje osobną wiadomość. Warstwy personalizacji, od deterministycznej do generowanej:

**Warstwa 1 — dane (kod, zawsze):**
imię osoby kontaktowej, nazwa firmy, język korespondencji, waluta preferowana przez agenta, format tabeli zgodny z tym, w jakim zwykle odpowiada.

**Warstwa 2 — kontekst relacji (kod, z historii):**
- pierwszy kontakt → krótkie przedstawienie firmy i sieci, przez którą się kontaktujesz
- znany agent → nawiązanie do ostatniej współpracy: „jak przy przesyłce GD/2026/00318 w czerwcu"
- agent, który dawno nie odpowiadał → inny ton, bez wyrzutów

**Warstwa 3 — treść zapytania (kod, szablon):**
relacja, ładunek, gotowość, incoterm, wymagane pozycje kosztowe, termin odpowiedzi.

**Warstwa 4 — szlif językowy (model, opcjonalnie):**
naturalne sformułowanie w języku agenta. Model **nie zmienia danych** — dostaje gotową treść i poprawia wyłącznie styl. Zasada 4 obowiązuje.

```
Temat: Rate request Gdynia (PLGDY) → Callao (PECLL) | 2×40HC | ready 15.09

Dear Miguel,

Following our shipment GD/2026/00318 in June, we have a new enquiry
for the same lane.

  POL          Gdynia, Poland (PLGDY)
  POD          Callao, Peru (PECLL)
  Equipment    2 × 40'HC
  Commodity    Furniture (HS to follow)
  Ready        15 September 2026
  Incoterm     FOB Gdynia

Please quote including: ocean freight, DTHC, D/O fee, customs
clearance and delivery to Lima. We would appreciate your reply
by 30 August, 12:00 CET.

Best regards,
[podpis handlowca]

--
Reply to this email — our system will register your quotation
automatically.
```

Ostatnia linijka nie jest ozdobnikiem. Informuje agenta, że ma odpisać na ten adres, i podnosi wskaźnik odpowiedzi trafiających automatycznie.

## 6. Wysyłka — inżynieria dostarczalności

To jest jedyna realna trudność w całym module.

**Adres zwrotny per odbiorca, nie per zapytanie.**
Poprawka do Aneksu 3: token musi identyfikować parę zapytanie–agent.

```
rr-{request_token}-{recipient_token}@rates.klient.twojadomena.pl
```

Powód: agenci odpisują z innych adresów niż te, na które piszesz — ze skrzynek wspólnych, od kolegi, z telefonu. Bez tokenu w adresie zwrotnym nie wiesz, kto odpowiedział, i cała automatyzacja się sypie.

**Rozłożenie wysyłki w czasie.** Trzydzieści maili w jednej sekundzie z nowej domeny to gwarantowany spam. Wysyłaj z odstępem kilku–kilkunastu sekund, w tle. Dla użytkownika to niewidoczne, dla dostarczalności decydujące.

**Osobna subdomena wysyłkowa** z poprawnie skonfigurowanymi SPF, DKIM i DMARC. Nie mieszaj z domeną firmową klienta — problem z reputacją nie może zablokować jego zwykłej poczty.

**Rozgrzewanie domeny.** Nowa domena zaczyna od kilkunastu maili dziennie i zwiększa wolumen przez dwa–trzy tygodnie. Wbuduj to jako automatyczny limit początkowy.

**Okno czasowe odbiorcy.** Mail do Limy wysłany o trzeciej w nocy czasu lokalnego czeka do rana i konkuruje z całą poranną skrzynką. Kolejkuj na godziny robocze w strefie agenta — wskaźnik odpowiedzi rośnie zauważalnie.

**Obsługa odbić i skarg.** Twarde odbicie oznacza kontakt do weryfikacji. Skarga oznacza wpis na listę wykluczeń i trwałe zaprzestanie wysyłki.

**Nagłówki wątkowania.** `Message-ID`, `In-Reply-To`, `References` — żeby odpowiedź trafiła do wątku, a przypomnienie nie było nowym mailem.

```sql
rate_request_recipient
  ...
  reply_to_token,               -- unikalny per odbiorca
  message_id,                   -- do wątkowania
  scheduled_send_at,            -- okno czasowe odbiorcy
  sent_at, delivered_at, opened_at
  bounced_at, bounce_type
  responded_at, response_message_id
  reminder_sent_at, reminder_count
  status
```

## 7. Odbiór i porównanie

Odpowiedzi wpadają na adres z tokenem, więc przypisanie jest jednoznaczne. Dalej działa pipeline z głównej specyfikacji: treść maila, Excel albo PDF przechodzą przez tę samą ekstrakcję co cenniki.

```
ODPOWIEDZI — Gdynia → Callao        3 z 3 · termin minął

                    Andes Cargo   Pacific Fwd   TransAndina
Ocean freight FCL      2 280 USD     2 410 USD     2 195 USD
DTHC Callao              310 USD       290 USD       340 USD
D/O fee                   85 USD        90 USD        —  ⚠
Customs clearance        180 USD       165 USD       220 USD
Delivery Lima            240 USD       260 USD       255 USD
─────────────────────────────────────────────────────────────
RAZEM                  3 095 USD     3 215 USD    3 010 USD ⚠

Czas odpowiedzi            2,8 h         5,1 h        26,4 h
⚠ TransAndina: brak D/O fee — oferta niepełna, realnie ~3 095 USD
```

Ostrzeżenie o brakującej pozycji jest istotniejsze niż suma. Najtańsza oferta z niepełnym zakresem to najdroższa oferta po fakturze — i to jest dokładnie ta funkcja, która zwraca się w pierwszym miesiącu.

## 8. Co dzieje się w tle

Każde wysłane zapytanie i każda odpowiedź:

- zapisują się jako `rate_line` — **baza cen rośnie niezależnie od tego, czy wygrasz to zlecenie**
- aktualizują kartę wyników agenta: czas odpowiedzi, kompletność, konkurencyjność
- wzbogacają katalog: faktyczna osoba kontaktowa, obsługiwane porty, język
- zasilają mapę pokrycia: gdzie masz sprawdzonych agentów, gdzie białe plamy

## 9. Kolejność budowy

| Etap | Zakres | Dni |
|---|---|---|
| 1 | `rfq` + ekstrakcja z maila + ekran zapytania | 5 |
| 2 | Wejście ręczne: formularz i wklejanie tekstu | 2 |
| 3 | `rate_request` + okno wyboru agentów | 4 |
| 4 | Personalizacja warstwy 1–3, szablony per język | 3 |
| 5 | **Wysyłka: tokeny, rozłożenie, SPF/DKIM/DMARC, odbicia** | 5 |
| 6 | Odbiór, przypisanie po tokenie, ekstrakcja odpowiedzi | 3 |
| 7 | Widok porównawczy z wykrywaniem braków | 3 |
| 8 | Przypomnienia, okna czasowe, wątkowanie | 2 |
| 9 | Notatka głosowa | 2 |
| 10 | Szlif językowy modelem | 1 |

Etap 5 jest najbardziej niedoceniany i najczęściej niedoszacowany. Cała reszta może działać bezbłędnie, a jeśli maile trafiają do spamu, moduł nie istnieje.
