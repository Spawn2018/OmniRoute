# Aneks 10 — Poczta: wysyłka, odbiór, kontakty

Zastępuje sekcję 6 Aneksu 9.

---

# CZĘŚĆ 1 — WYSYŁKA Z FIRMOWEJ SKRZYNKI UŻYTKOWNIKA

## 1.1 Co to zmienia

| | Osobna subdomena wysyłkowa | Skrzynka użytkownika |
|---|---|---|
| SPF, DKIM, DMARC | musisz skonfigurować | już działa |
| Rozgrzewanie domeny | 2–3 tygodnie | niepotrzebne |
| Reputacja nadawcy | budujesz od zera | istnieje od lat |
| Rozłożenie wysyłki w czasie | konieczne | zalecane, ale mniej krytyczne |
| Odbiór przez agenta | nieznany nadawca | znany adres, często już w kontaktach |
| Kopia w „Wysłane" u handlowca | brak | jest |
| Odpowiedź agenta | na adres z tokenem | do skrzynki handlowca |

Cała sekcja o dostarczalności z Aneksu 9 przestaje być problemem. **Zostaje jeden nowy: jak rozpoznać, która odpowiedź dotyczy którego zapytania.**

## 1.2 Trzy poziomy dopasowania odpowiedzi

Buduj wszystkie trzy. Działają kaskadowo.

**Poziom 1 — nagłówki wątkowania (podstawowy, ~85% przypadków)**

Przy wysyłce zapisujesz `Message-ID` oraz `conversationId`. Odpowiedź zawiera je w `In-Reply-To` i `References`. Dopasowanie jest jednoznaczne i nie wymaga niczego od agenta.

```sql
rate_request_recipient
  ...
  sent_message_id,       -- Message-ID wysłanej wiadomości
  conversation_id,       -- wątek u dostawcy poczty
  reply_token            -- do poziomu 2 i 3
```

Zawodzi, gdy agent pisze nową wiadomość zamiast odpowiadać — co robi około jednego na siedmiu.

**Poziom 2 — adres z plusem (uzupełniający)**

```
From:     jan.kowalski@spedytor.pl
Reply-To: jan.kowalski+rr7f3a91@spedytor.pl
```

Odpowiedź trafia do własnej skrzynki handlowca, ale z tokenem w adresie. Microsoft 365 obsługuje adresowanie z plusem po włączeniu przez administratora, Google natywnie. Sprawdź to przy podłączaniu konta i wyłącz ten poziom, jeśli dostawca nie wspiera.

**Poziom 3 — token w temacie (ostatnia deska ratunku)**

```
Temat: Rate request Gdynia → Callao | 2×40HC [REF: RR-7F3A91]
```

Brzydkie, ale ratuje przypadek, w którym agent pisze zupełnie nową wiadomość, kopiując temat. Trzymaj token krótki i na końcu.

**Poziom 4 — dopasowanie kontekstowe (gdy wszystko zawiedzie)**

Nieznana wiadomość z domeny agenta, do którego wysłałeś zapytanie w ostatnich 72 godzinach, zawierająca stawki na tę relację. System proponuje przypisanie, człowiek potwierdza jednym kliknięciem. Nie zgaduje po cichu.

## 1.3 Wysyłka techniczna

**Microsoft 365 — przez Graph, nie SMTP.**
Wysyłka jako użytkownik z uprawnieniem delegowanym. Wiadomość ląduje w folderze „Wysłane" handlowca, co jest istotne: widzi własną korespondencję w Outlooku tak, jakby napisał ją sam. Buduje zaufanie do systemu szybciej niż jakakolwiek funkcja.

**Google Workspace — Gmail API**, analogicznie.

**Pozostali — SMTP z OAuth albo hasłem aplikacji.**

`postalsys/emailengine` z katalogu obsługuje wszystkie trzy pod jednym interfejsem — to jest dokładnie ten przypadek użycia, do którego został zbudowany.

**Podpis.** Pobierz podpis użytkownika przy podłączaniu konta albo pozwól wkleić. Mail ma wyglądać jak jego mail, nie jak wygenerowany.

**Rozłożenie w czasie.** Nadal zalecane przy trzydziestu odbiorcach — nie z powodu reputacji, tylko limitów dostawcy. Microsoft 365 ma limit wiadomości na godzinę i na dobę. Przy wysyłce hurtowej kolejkuj z odstępem i pokazuj postęp.

## 1.4 Ograniczenia do przewidzenia

- **Limity dostawcy.** M365 i Google mają dobowe limity wysyłki. Przy trzydziestu odbiorcach nieistotne, przy stu — trzeba je znać i pokazać użytkownikowi
- **Urlop handlowca.** Zapytanie wysłane z jego skrzynki, odpowiedź wpada do jego skrzynki, a on jest na wakacjach. Potrzebujesz skrzynki zespołowej jako alternatywnego nadawcy dla zapytań, które ma obsłużyć dział, nie osoba
- **Rotacja pracowników.** Odejście handlowca nie może zabrać historii. Wiadomości i tak zapisujesz u siebie — skrzynka jest kanałem, nie archiwum

---

# CZĘŚĆ 2 — INTEGRACJA CZY DODATEK DO OUTLOOKA

## 2.1 Rozstrzygnięcie

**Potrzebujesz obu, ale do różnych rzeczy — i integracja serwerowa jest pierwsza.**

| | Integracja serwerowa | Dodatek do Outlooka |
|---|---|---|
| Działa bez włączonego komputera | tak | nie |
| Działa na telefonie | tak | ograniczenie |
| Wymaga kliknięcia użytkownika | nie | tak |
| Łapie wszystko | tak | tylko to, co kliknięte |
| Zakres dostępu do skrzynki | do ustalenia | minimalny |
| Skrzynki wspólne | tak | z ograniczeniami |
| Nakład | ~1 tydzień | ~2 tygodnie, osobny stos |

**Rozstrzygające:** automatyczne przechwytywanie odpowiedzi agentów **musi** być serwerowe. Cała wartość pętli RFQ polega na tym, że odpowiedzi wpadają i parsują się bez udziału człowieka. Dodatek wymagający kliknięcia niweczy sens funkcji.

## 2.2 Rozwiązanie problemu prywatności

Najczęstszy zarzut przy integracji serwerowej brzmi „nie chcę, żebyście czytali całą moją skrzynkę". Jest uzasadniony i ma czyste rozwiązanie techniczne.

**Nie czytaj skrzynki. Czytaj wątki, które sam założyłeś.**

Skoro to ty wysyłasz zapytanie, znasz `conversationId`. Odpytujesz dostawcę wyłącznie o te konkretne wątki. Nie masz wglądu w żadną inną korespondencję — ani technicznie, ani w logach.

Do tego jeden dedykowany folder na to, czego nie zainicjowałeś:

```
Skrzynka handlowca
├── Odebrane                    ← system NIE ma wglądu
├── Wysłane                     ← tylko zapis własnych wysyłek
└── Spedycja/Cenniki            ← system czyta TYLKO ten folder
    (reguła Outlooka albo ręczne przeniesienie)
```

Agent przysyła cennik bez zapytania? Handlowiec przenosi do folderu, system przetwarza. Reguły przenoszące automatycznie po nadawcy da się stworzyć programowo, gdy klient sobie tego zażyczy.

Ten model sprzedaje się sam w rozmowie z działem IT klienta: **„nie mamy dostępu do skrzynki, mamy dostęp do wątków, które sami założyliśmy, plus jednego folderu"**. To jest różnica między wdrożeniem w tydzień a trzymiesięczną analizą bezpieczeństwa.

## 2.3 Kiedy dodatek do Outlooka

W drugiej kolejności, do rzeczy, w których liczy się osąd człowieka:

- **„Zarejestruj jako zapytanie"** — handlowiec dostaje maila od klienta i decyduje, że to zapytanie ofertowe. Jedno kliknięcie zamiast przeklejania
- **„Dołącz do zlecenia"** — korespondencja operacyjna przypisana do konkretnego job file'a
- **Panel boczny** — przy mailu od znanego kontrahenta pokazuje jego otwarte zlecenia, limit kredytowy, ostatnie oferty

To są funkcje wygody, nie fundament. Buduj po tym, jak serwerowa część działa.

## 2.4 Kolejność

```
Etap 1 (tydzień)      Graph + Gmail API przez EmailEngine
                      wysyłka jako użytkownik, odczyt własnych wątków
Etap 2 (2 dni)        dedykowany folder na cenniki niezamówione
Etap 3 (3 dni)        IMAP jako zapas dla pozostałych dostawców
Etap 4 (2 tygodnie)   dodatek do Outlooka — rejestracja i panel boczny
```

---

# CZĘŚĆ 3 — AUTOMATYCZNE KONTAKTY

Twój pomysł jest dobry i rozwiązuje problem, którego nie da się rozwiązać inaczej: agenci odpisują z adresów, których nie masz w bazie.

## 3.1 Mechanizm

```
Przychodzi wiadomość z nieznanego adresu
        ↓
[1] DOPASOWANIE DOMENY
    domena znana → wysoka pewność, sugestia do kolejki
    domena podobna do znanej → ⚠ OSTRZEŻENIE, nie sugestia (patrz 3.4)
    domena darmowa (gmail, 163, qq) → poziom 2
    domena nieznana → poziom 3
        ↓
[2] KONTEKST WĄTKU
    odpowiedź na zapytanie wysłane do agenta X
    → przypisz do X z wysoką pewnością, niezależnie od domeny
    (to rozwiązuje większość przypadków z darmowych skrzynek)
        ↓
[3] PODPIS
    ekstrakcja: imię i nazwisko, stanowisko, firma,
    telefon, komórka, adres, strona
    + załącznik vCard, jeśli jest
        ↓
[4] KOLEJKA WERYFIKACJI
    karta z danymi, wszystkie pola edytowalne
    użytkownik: zatwierdza / poprawia / przypisuje do innej firmy / odrzuca
        ↓
[5] ZAPIS + NAUKA
    domena dopisana do party_email_domain
    następny kontakt z tej domeny → poziom 1
```

## 3.2 Ekstrakcja podpisu

Dwuetapowo, zgodnie z zasadą 4:

**Kod:** wykrycie bloku podpisu (separator, ostatnie linie, powtarzalność w historii wątku), wyodrębnienie numerów telefonów i adresów przez wyrażenia regularne, sprawdzenie załącznika vCard.

**Model:** wyciągnięcie stanowiska, nazwy firmy i roli z bloku tekstu — bo podpisy są nieregularne i wielojęzyczne. Zwraca strukturę, nie prozę.

Podpisy chińskich i wietnamskich agentów mają układ, którego reguły nie obejmą. Tu model jest właściwym narzędziem, ale wynik zawsze idzie do weryfikacji.

## 3.3 Model danych

```sql
party_email_domain
  id, party_id, domain, is_primary
  confidence, confirmed_by, confirmed_at

contact_suggestion
  id, organization_id
  source_message_id, from_email, from_name
  suggested_party_id, match_method,   -- domain | thread | name | manual
  match_confidence
  extracted jsonb,                     -- imię, stanowisko, telefon, firma
  status,                              -- pending | accepted | rejected | merged
  reviewed_by, reviewed_at,
  created_contact_id NULL
```

## 3.4 Ten sam mechanizm wykrywa podszycie

To jest najważniejsza konsekwencja, której nie było w twoim opisie.

Skoro system dopasowuje po domenie, to **automatycznie widzi domeny podobne do znanych**:

```
⚠ UWAGA — możliwe podszycie

Wiadomość od: miguel@andes-cargo.com
Znana domena:  andescargo.com  (Andes Cargo SAC, 8 zapytań)

Różnica: dodany myślnik
Treść zawiera: zmiana rachunku bankowego

→ NIE dodawaj kontaktu automatycznie
→ Zweryfikuj innym kanałem przed jakąkolwiek płatnością
```

Zmiana rachunku bankowego przysłana z domeny łudząco podobnej to najczęstszy schemat oszustwa w spedycji. Mechanizm, który budujesz dla wygody, jest jednocześnie zabezpieczeniem — i to jest funkcja, o której warto mówić przy sprzedaży.

Reguła twarda: **domena podobna, ale nie identyczna, nigdy nie generuje sugestii dodania. Generuje ostrzeżenie.**

## 3.5 Wymogi prawne

Dane osobowe pracowników twojego kontrahenta. Podstawą jest uzasadniony interes w kontaktach handlowych, ale wiąże się z obowiązkami:

- **informacja o przetwarzaniu** dostępna dla osób, których dane zbierasz — link w stopce wysyłanych wiadomości wystarczy
- **retencja** — kontakt nieużywany przez X lat do usunięcia
- **usunięcie na żądanie** — funkcja w systemie, nie procedura ręczna
- **umowa powierzenia** twojego klienta musi obejmować ten typ danych
- **automatyzacja bez nadzoru** jest tu ryzykowna — dlatego kolejka weryfikacji nie jest wygodą, tylko wymogiem

## 3.6 Efekt po roku

Baza kontaktów przestaje wymagać utrzymania. Każda korespondencja ją wzbogaca: nowe osoby, aktualne telefony, zmiany stanowisk, faktyczne adresy, z których agenci odpisują.

To jest ten sam wzorzec, który przewija się przez cały projekt: **funkcja wykonuje zadanie dziś i zostawia po sobie dane, które jutro czynią ją lepszą.** Karta wyników agenta, katalog sieci, słownik aliasów opłat, elastyczność cenowa — wszystkie działają tak samo. Konkurent może skopiować każdą z osobna, ale nie może skopiować roku twoich danych.
