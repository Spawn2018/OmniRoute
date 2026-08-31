# Aneks 17 — Zgodność regulacyjna

Nie jestem prawnikiem i to nie jest opinia prawna. Poniższe ustalenia opierają
się na publicznie dostępnych źródłach i wymagają weryfikacji z kancelarią
przed pierwszą umową. Podaję je, bo **dwa z nich zmieniają projekt systemu**,
a nie tylko dokumentację.

---

# 1. MAPA REŻIMÓW

| Reżim | Dotyczy cię | Termin |
|---|---|---|
| **AI Act** | **tak, moduł oceny kredytowej jako wysokiego ryzyka** | 2.12.2027 |
| **Cyber Resilience Act** | częściowo, do oceny | 11.09.2026 · 11.12.2027 |
| RODO | tak, w pełni | obowiązuje |
| Dyrektywa o odpowiedzialności za produkt | tak — obejmuje oprogramowanie | transpozycja do 9.12.2026 |
| NIS2 | pośrednio, przez klientów | obowiązuje |
| Sankcje UE | tak, odpowiedzialność karna | obowiązuje |
| Kontrola eksportu (podwójne zastosowanie) | tak | obowiązuje |
| Prawo baz danych sui generis | tak, katalogi sieci | obowiązuje |
| Prawo konkurencji | tak, przy danych cenowych | obowiązuje |
| KSeF | tak | wg harmonogramu MF |
| Prawo autorskie | tak, IMDG i dane indeksowe | obowiązuje |

---

# 2. AI ACT — NAJWAŻNIEJSZE USTALENIE ⚠

## 2.1 Wirtualny CFO to system wysokiego ryzyka

(cite index="76-1">Sztuczna inteligencja oceniająca zdolność kredytową osób fizycznych jest systemem wysokiego ryzyka na mocy AI Act, załącznik III punkt 5(b); wykrywanie oszustw jest z tego wyłączone.</cite>

Moduł M-15, który zaprojektowaliśmy jako Wirtualnego Dyrektora Finansowego,
ocenia zdolność kredytową kontrahentów. **Jednoosobowa działalność gospodarcza
to osoba fizyczna.** Twój system w obecnym kształcie mieści się w załączniku III.

(cite index="70-1">Bezpieczna przystań z artykułu 6(3) pozwala uniknąć klasyfikacji wysokiego ryzyka, jeśli system nie stwarza istotnego ryzyka dla zdrowia, bezpieczeństwa lub praw podstawowych, ale decyzje kredytowe wpływające na dostęp osób do produktów finansowych rzadko spełniają ten warunek, a organy zapowiedziały, że będą uważnie analizować samoocenę.</cite>

## 2.2 Co to oznacza w obowiązkach

Jako dostawca systemu wysokiego ryzyka: (cite index="72-1">zarządzanie ryzykiem (art. 9), zarządzanie danymi (art. 10), dokumentacja techniczna (art. 11 i załącznik IV), rejestrowanie (art. 12), przejrzystość i instrukcje (art. 13), nadzór człowieka (art. 14), dokładność i odporność (art. 15), system zarządzania jakością (art. 17), ocena zgodności (art. 43), rejestracja (art. 49).</cite>

(cite index="75-1">Dostawcy muszą przeprowadzić ocenę zgodności, wdrożyć system zarządzania jakością, zarejestrować się w bazie UE, nanieść oznakowanie CE i przygotować dokumentację techniczną. Wdrażający muszą przeprowadzić ocenę wpływu na prawa podstawowe, wdrożyć nadzór człowieka i dokumentować całe użycie systemu wysokiego ryzyka.</cite>

Kary: (cite index="70-1">do 15 milionów euro albo 3% globalnego rocznego obrotu.</cite>

**Dla jednoosobowej firmy to jest nieproporcjonalne obciążenie.** Ocena
zgodności, oznakowanie CE i rejestracja w bazie UE to program na kwartały,
nie na tydzień.

## 2.3 Termin

(cite index="73-1">Po Digital Omnibus, uzgodnionym 7 maja 2026, samodzielne systemy wysokiego ryzyka z załącznika III — w tym ocena zdolności kredytowej — obowiązują od 2 grudnia 2027. Przepisy o przejrzystości z artykułu 50(1) obowiązują od 2 sierpnia 2026; zakazy praktyk i wymóg kompetencji w zakresie AI od 2 lutego 2025; przepisy o modelach ogólnego przeznaczenia od 2 sierpnia 2025.</cite>

(cite index="75-1">Przedłużenie jest wyłącznie czasowe: żaden obowiązek nie został usunięty.</cite>

## 2.4 Rozwiązanie projektowe — i jest proste

Załącznik III punkt 5(b) mówi o **osobach fizycznych**. Spółka z ograniczoną
odpowiedzialnością nie jest osobą fizyczną.

**Decyzja: ogranicz automatyczną ocenę zdolności kredytowej wyłącznie do osób
prawnych.** Dla jednoosobowych działalności system pokazuje dane źródłowe —
sprawozdania, wpisy w rejestrach, historię płatniczą — **bez wyliczania punktacji
i bez sugerowania limitu**. Decyzję podejmuje człowiek na podstawie danych.

To rozwiązuje jednocześnie drugi problem, który już mieliśmy w projekcie:

(cite index="70-1">Wyrok w sprawie SCHUFA z 2023 roku oznacza, że prawa z artykułu 22 RODO stosują się już na etapie scoringu, co czyni nadzór człowieka wymogiem projektowym, a nie reaktywnym ujawnieniem.</cite>

**Konsekwencje dla M-15:**

```sql
-- rozszerzenie credit_assessment
  subject_legal_form,        -- legal_person | natural_person
  scoring_enabled bool,      -- FALSE dla natural_person, wymuszone kodem
  ai_involvement,            -- none | data_aggregation | scoring
  decision_maker_user_id,    -- zawsze wypełnione
  decision_rationale text    -- art. 86: prawo do wyjaśnienia
```

Reguła w kodzie, nie w regulaminie: dla `natural_person` silnik punktowy się
nie uruchamia. Test jednostkowy tego pilnuje.

## 2.5 Co obowiązuje już teraz

**Kompetencje w zakresie AI** (od lutego 2025) — masz obowiązek zapewnić, że
osoby obsługujące system rozumieją jego działanie i ograniczenia. Praktycznie:
sekcja w dokumentacji użytkownika i potwierdzenie zapoznania przy wdrożeniu.

**Przejrzystość, artykuł 50(1)** (od sierpnia 2026) — użytkownik musi wiedzieć,
że rozmawia z systemem AI albo że treść została wygenerowana. Dotyczy twojego
copilota (M-58) i maili generowanych do agentów (M-30).

**Wykrywanie oszustw jest wyłączone** z załącznika III — moduł M-54 jest
poza reżimem wysokiego ryzyka.

---

# 3. CYBER RESILIENCE ACT

## 3.1 Terminy — pierwszy jest za dwa tygodnie

(cite index="80-1">Rozporządzenie weszło w życie 10 grudnia 2024. Główne obowiązki obowiązują od 11 grudnia 2027, a obowiązki sprawozdawcze od 11 września 2026. 27 lipca 2026 Komisja opublikowała praktyczne wytyczne.</cite>

## 3.2 Czy dotyczy cię — odpowiedź jest niejednoznaczna

(cite index="81-1">Oferty wyłącznie w modelu SaaS są zasadniczo objęte odrębnie przez NIS2 i pozostają poza zakresem CRA.</cite>

(cite index="84-1">Aplikacja webowa używana wyłącznie przez przeglądarkę oraz strona internetowa, która jedynie prezentuje informacje, zasadniczo nie są produktami z elementami cyfrowymi. Wchodzą w zakres tylko wtedy, gdy kwalifikują się jako zdalne przetwarzanie danych wspierające funkcję produktu.</cite>

**Twoja aplikacja webowa: prawdopodobnie poza zakresem.**

**Ale dodatek do Outlooka (M-33) to oprogramowanie instalowane u klienta.**
To zmienia kwalifikację i wymaga oceny. To samo dotyczyłoby ewentualnej
aplikacji mobilnej.

(cite index="82-1">Organizację można uznać za producenta, gdy opracowuje produkt cyfrowy — albo zleca jego opracowanie — i wprowadza go na rynek pod własną nazwą lub znakiem towarowym.</cite>

## 3.3 Co zrobić niezależnie od kwalifikacji

Infrastruktura wymagana przez CRA jest dobrą praktyką i przydaje się w NIS2
oraz w rozmowach z działami bezpieczeństwa klientów:

```
□ SBOM generowany automatycznie w CI (CycloneDX przez syft)
□ Polityka ujawniania podatności + plik security.txt
□ Proces obsługi zgłoszeń: 24 h wstępne, 72 h pełne, 14 dni raport końcowy
□ Rejestr podatności w zależnościach (Renovate + trivy + pip-audit)
□ Zadeklarowany okres wsparcia produktu
```

Kary za naruszenie: (cite index="79-1">do 15 milionów euro albo 2,5% światowego rocznego obrotu.</cite>

**Rekomendacja:** wdrażaj SBOM i politykę ujawniania od pierwszego tygodnia.
Koszt: dwa dni. Nawet jeśli CRA cię nie obejmie, pierwszy klient korporacyjny
o SBOM zapyta.

---

# 4. RODO — POZA TYM, CO JUŻ WIEMY

## 4.1 Podpowierzenie — było, przypominam wagę

Wysyłasz cenniki i dokumenty klienta do zewnętrznego API modelu. To jest
podpowierzenie i musi być w umowie z nazwą dostawcy, lokalizacją przetwarzania
i retencją. Klient, który dowie się po fakcie, ma podstawę do rozwiązania umowy
i zgłoszenia naruszenia.

## 4.2 Artykuł 22 i prawo do wyjaśnienia

Decyzja kredytowa wobec jednoosobowej działalności to zautomatyzowana decyzja
wywołująca skutki prawne. Wymaga prawa do interwencji człowieka, wyrażenia
stanowiska i zakwestionowania.

Do tego artykuł 86 AI Act: (cite index="72-1">osoba, wobec której podjęto decyzję na podstawie systemu wysokiego ryzyka z załącznika III, ma prawo do jasnego i zrozumiałego wyjaśnienia roli, jaką AI odegrała w tej decyzji.</cite>

**Konsekwencja projektowa:** sekcja „podstawa wyliczenia" w opinii kredytowej
nie jest ozdobnikiem. Jest realizacją obowiązku prawnego i musi być
przechowywana razem z decyzją.

## 4.3 Ocena skutków dla ochrony danych

Systematyczne przetwarzanie danych kontrahentów na dużą skalę z profilowaniem
wymaga oceny skutków. Zrób ją przed pierwszym klientem zewnętrznym, nie po.

## 4.4 Dane osób trzecich

Automatyczne kontakty (M-11) zbierają dane pracowników kontrahentów twojego
klienta. Podstawą jest uzasadniony interes, ale wiąże się z obowiązkiem
informacyjnym — link w stopce wysyłanych wiadomości wystarczy — oraz retencją
i usunięciem na żądanie.

---

# 5. ODPOWIEDZIALNOŚĆ ZA PRODUKT

Nowa dyrektywa o odpowiedzialności za produkty wadliwe **wprost obejmuje
oprogramowanie**, w tym aktualizacje i systemy AI. Transpozycja do prawa
krajowego do grudnia 2026.

Kluczowa zmiana: odpowiedzialność na zasadzie ryzyka, nie winy. Wadliwe
oprogramowanie powodujące szkodę majątkową rodzi odpowiedzialność niezależnie
od dochowania staranności.

**Konsekwencje:**
- ograniczenie odpowiedzialności w umowie nie działa wobec tej dyrektywy tak,
  jak wobec odpowiedzialności kontraktowej
- **ubezpieczenie OC działalności IT przestaje być opcją** — z listy „warto"
  przechodzi do „konieczne"
- dokumentacja testów i procesu jakości staje się materiałem dowodowym

To jest dodatkowy argument za bramkami jakości z części VI planu: nie tylko
dobra praktyka, ale dowód należytej staranności.

---

# 6. NIS2 — POŚREDNIO, ALE REALNIE

Transport i logistyka to sektor objęty dyrektywą. Twoi więksi klienci mogą być
podmiotami ważnymi albo kluczowymi. **Obowiązki w zakresie bezpieczeństwa
łańcucha dostaw przechodzą wtedy na ciebie jako dostawcę.**

Praktycznie oznacza to, że przy sprzedaży do większego spedytora dostaniesz
kwestionariusz bezpieczeństwa. Przygotuj się:

```
□ Polityka bezpieczeństwa informacji
□ Zarządzanie podatnościami (masz z CRA)
□ Plan reagowania na incydenty z terminami zgłoszeń
□ Kopie zapasowe i plan ciągłości działania
□ Kontrola dostępu i uwierzytelnianie wieloskładnikowe
□ Rejestr podprzetwarzających
□ SBOM
```

Większość tego masz w module M-76. Brakuje polityki bezpieczeństwa i planu
ciągłości — to dokumenty, nie kod.

---

# 7. SANKCJE I KONTROLA EKSPORTU

## 7.1 To nie jest tylko funkcja produktu

Naruszenie sankcji UE to odpowiedzialność karna, w Polsce z realnymi sankcjami
za obrót z podmiotami objętymi ograniczeniami. Twój moduł M-53 nie jest
udogodnieniem — jest narzędziem, które chroni twojego klienta przed
odpowiedzialnością.

**Ale uwaga na własną odpowiedzialność:** jeśli twój system deklaruje
sprawdzanie sankcji i przeoczy trafienie, klient wskaże ciebie. Stąd:

- `list_versions` przy każdym skanowaniu — dowód, na jakiej wersji sprawdzano
- jasne zastrzeżenie: system wspiera weryfikację, nie zastępuje obowiązków klienta
- brak automatycznego zwalniania — trafienie zawsze do decyzji człowieka

## 7.2 Towary podwójnego zastosowania

Kod HS zestawiony z wykazem kontrolnym daje **sygnał, nie klasyfikację**.
Klasyfikacja podwójnego zastosowania wymaga wiedzy eksperckiej i pozostaje
obowiązkiem eksportera. System sygnalizuje, nie rozstrzyga.

---

# 8. PRAWA DO DANYCH I KONKURENCJA

## 8.1 Bazy danych sui generis

Katalogi członków sieci spedycyjnych są chronione prawem sui generis.
Masowe pobranie zawartości jest naruszeniem, nawet gdy pojedyncze dane nie są
chronione. Architektura z M-12 — kopia per tenant, importowana na podstawie
własnego członkostwa klienta — jest odpowiedzią na to ryzyko i musi zostać.

## 8.2 Prawo konkurencji — pułapka przy efektach sieciowych

Zestawianie danych cenowych między konkurującymi spedytorami, nawet
zanonimizowanych, to ryzyko zmowy cenowej. Architektura wielodostępna
z pełną izolacją czyni to strukturalnie niemożliwym.

**Powiedz to wprost w rozmowie handlowej i zapisz w umowie.** To buduje
zaufanie zamiast je niszczyć, a jednocześnie chroni cię przed pokusą
zbudowania „benchmarku" z cudzych danych.

## 8.3 Dane indeksowe

Indeksy frachtowe są dostępne publicznie na poziomie zbiorczym, ale dane
historyczne i szczegółowe wymagają subskrypcji. Możesz pokazać publiczny poziom
z podaniem źródła. **Nie możesz zbudować z niego własnej bazy historycznej
i redystrybuować klientom.** Model: klient wnosi własną subskrypcję.

## 8.4 IMDG i IATA DGR

Teksty tych kodeksów są chronione prawem autorskim. Załączniki ADR są
publikowane bezpłatnie przez EKG ONZ. Buduj z tego drugiego źródła, nie kopiuj
tekstu przepisów.

---

# 9. ZMIANY W DOKUMENTACJI

## 9.1 Nowy moduł

### M-78 · Zgodność regulacyjna produktu
**Domena:** N (platforma) · **Spec:** `regulatory.md`

| Obiekty | Funkcje |
|---|---|
| `ai_system_inventory` · `ai_interaction_log` · `sbom_snapshot` · `vulnerability_report` · `incident_report` · `dpia_record` | rejestr systemów AI z klasyfikacją ryzyka · logi wywołań AI (art. 12) · SBOM w CI · obsługa zgłoszeń podatności z terminami · ocena skutków · deklaracja przejrzystości AI (art. 50) |

**Repozytoria:** `anchore/syft` (SBOM) · `aquasecurity/trivy` · `pyupio/safety`

## 9.2 Zmiany w istniejących modułach

**M-15 (Wirtualny CFO)** — zmiana zasadnicza:
> Automatyczna ocena punktowa i wyliczanie limitu **wyłącznie dla osób prawnych**.
> Dla osób fizycznych prowadzących działalność: prezentacja danych źródłowych
> bez punktacji i bez sugerowanego limitu. Wymuszone kodem i testem, nie regulaminem.

**M-56 (RODO)** — rozszerz o: ocenę skutków, rejestr podprzetwarzających
jako dokument dla klienta, obowiązek informacyjny w stopce wiadomości.

**M-58, M-30** — deklaracja, że treść jest generowana przez AI (art. 50).

**M-53** — zastrzeżenie o charakterze wspierającym, nie zastępującym.

## 9.3 Nowe zasady w `AGENTS.md`

> 15. Ocena punktowa zdolności kredytowej wyłącznie dla osób prawnych.
>     Dla osób fizycznych: dane, nie punktacja.
> 16. Każde wywołanie modelu w ścieżce decyzyjnej jest logowane
>     z wersją modelu, wejściem, wyjściem i identyfikatorem decydenta.
> 17. Treść generowana przez AI i widoczna dla osoby trzeciej
>     jest jako taka oznaczona.

## 9.4 Zmiany w harmonogramie

| Plaster | Zakres | Kiedy |
|---|---|---|
| `0.10` | SBOM w CI, security.txt, polityka ujawniania | **faza 0** — przed 11.09.2026 |
| `0.11` | `ai_interaction_log`, rejestr systemów AI | faza 0 |
| `2.14` | Deklaracja przejrzystości AI w interfejsie | faza 2 |
| `7.15` | Ocena skutków dla ochrony danych | przed pierwszym klientem |
| `9.6a` | M-15 z ograniczeniem do osób prawnych | faza 9 |

## 9.5 Dokumenty poza kodem

Do przygotowania z kancelarią przed pierwszą umową:

```
□ Umowa SaaS z ograniczeniem odpowiedzialności
□ Umowa powierzenia z listą podprzetwarzających
□ Polityka prywatności i obowiązek informacyjny
□ Regulamin usługi
□ Polityka bezpieczeństwa informacji
□ Plan ciągłości działania
□ Rejestr czynności przetwarzania
□ Ocena skutków dla ochrony danych
□ Polityka retencji
□ Polityka ujawniania podatności
□ Deklaracja o systemach AI i ich roli
□ Ubezpieczenie OC działalności IT
```

---

# 10. TRZY WNIOSKI

**① Ogranicz ocenę kredytową do osób prawnych.** Jedna decyzja projektowa
wyprowadza cię spod reżimu systemów wysokiego ryzyka AI Act, którego jednoosobowa
firma nie udźwignie. Koszt: funkcja dla części klientów jest uboższa.
Zysk: brak oceny zgodności, oznakowania CE i rejestracji w bazie UE.

**② SBOM i polityka ujawniania podatności w pierwszym tygodniu.** Obowiązki
sprawozdawcze CRA ruszają 11 września 2026. Nawet jeśli twoja aplikacja webowa
jest poza zakresem, dodatek do Outlooka może nie być — a infrastruktura i tak
przyda się przy NIS2 i przy pierwszym kwestionariuszu bezpieczeństwa.

**③ Ubezpieczenie OC przestaje być opcją.** Nowa dyrektywa o odpowiedzialności
za produkt obejmuje oprogramowanie i wprowadza odpowiedzialność na zasadzie
ryzyka. Umowne ograniczenie odpowiedzialności nie chroni przed nią tak, jak
przed odpowiedzialnością kontraktową.

**Przed pierwszą umową:** przegląd z kancelarią specjalizującą się w prawie
nowych technologii. Wszystko powyżej to mapa obszarów do sprawdzenia, nie
zastępstwo opinii.
