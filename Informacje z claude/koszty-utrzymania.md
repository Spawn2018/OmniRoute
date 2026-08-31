# Koszty utrzymania systemu — model dla twórcy

Stan cen: sierpień 2026. Kurs przyjęty: 1 USD ≈ 4,00 PLN, 1 EUR ≈ 4,30 PLN. Zweryfikowane stawki API Claude na dzień 26 sierpnia 2026.

---

## 1. Faza budowy (miesiące 1–12)

To, co płacisz, zanim system komukolwiek służy.

| Pozycja | Miesięcznie | Uwagi |
|---|---|---|
| Cursor Pro | ~85 PLN | $20 |
| Claude (subskrypcja do pracy nad kodem) | 85–850 PLN | Pro $20 / Max $100–200. Przy tej skali projektu Max się zwraca |
| Serwer developerski (Hetzner CPX31, 4 vCPU / 8 GB) | ~60 PLN | €14 |
| Storage na cenniki testowe (1 TB) | ~20 PLN | €4 |
| Domena | ~10 PLN | ~120 PLN/rok |
| API Claude — testy ekstrakcji | 40–160 PLN | zależnie od intensywności iteracji |
| **Razem faza budowy** | **300–1 200 PLN/mies.** | ~4–14 tys. PLN rocznie |

**Koszt niewidoczny, a największy:** twój czas. Realistycznie 800–1 000 godzin na fazy 1–4. Licząc alternatywny koszt twojej godziny przy 120–150 PLN, to **100–150 tys. PLN**. To jest prawdziwa cena tego projektu i warto ją mieć wypisaną, zanim porównasz z abonamentem za gotowy system.

---

## 2. Koszt AI — najczęściej przeszacowywany

Aktualne stawki Claude API: <cite index="106-1">Haiku 4.5 kosztuje $1 za milion tokenów wejściowych i $5 za wyjściowe, Sonnet 5 to $2/$10 do 31 sierpnia 2026, potem $3/$15, Opus 5 to $5/$25. Trafienie w cache kosztuje 10% ceny bazowej wejścia, a Batch API obniża wejście i wyjście o połowę.</cite>

### Koszt jednego cennika

Typowy arkusz FCL po ekstrakcji przez Docling to ~20 tys. tokenów wejścia, odpowiedź strukturalna ~5 tys. tokenów wyjścia. Na Sonnet 5 po zakończeniu promocji ($3/$15):

```
wejście:   0,020 M × $3  = $0,060
wyjście:   0,005 M × $15 = $0,075
                    razem ≈ $0,14  (≈ 0,55 PLN)
```

Duży, wieloarkuszowy cennik (60 tys. / 12 tys. tokenów) ≈ $0,36 (≈ 1,45 PLN).

**Średnio przyjmij 1 PLN za cennik.** Przez Batch API — 50 gr.

### Efekt pamięci szablonów

Po kilku miesiącach ~80% cenników parsuje się deterministycznie, bez wywołania modelu. Realny koszt spada pięciokrotnie.

### Wnioski, które zmieniają planowanie

Przy 60 cennikach miesięcznie płacisz **około 12 PLN**. Nie 1 200. LLM nie jest kosztem tego systemu — kosztem jest infrastruktura i twój czas. Wszystkie decyzje architektoniczne typu „użyjmy słabszego modelu, żeby oszczędzić" są na tej skali bezprzedmiotowe. Używaj najlepszego modelu, jaki daje najwyższą skuteczność ekstrakcji, bo różnica w rachunku to kilkadziesiąt złotych, a różnica w błędnej stawce na ofercie to kilka tysięcy.

Odwrotnie działa copilot i text-to-SQL: tam koszt generuje częstotliwość pytań, nie objętość dokumentu. Przy 200 zapytaniach miesięcznie ze schematem bazy w kontekście to ~50 PLN, a z buforowaniem promptu (schemat się nie zmienia) spada do ~15 PLN.

---

## 3. Trzy scenariusze eksploatacji

### A. Tylko ty — LOGMAR i HHL

| Pozycja | Miesięcznie |
|---|---|
| Serwer (CPX31, aplikacja + baza + workery) | ~60 PLN |
| Object storage 1 TB (cenniki źródłowe, dokumenty) | ~20 PLN |
| Backup poza serwerem | ~25 PLN |
| API Claude — ekstrakcja (~60 cenników) | ~12 PLN |
| API Claude — copilot i raporty | ~15–50 PLN |
| Monitoring, Sentry, Langfuse — self-hosted | 0 PLN |
| KSeF, GUS/REGON, biała lista VAT, kursy NBP | 0 PLN |
| Certyfikat kwalifikowany (pieczęć do KSeF) | ~35 PLN | *~400 PLN/rok* |
| Domena | ~10 PLN |
| **Razem** | **180–220 PLN/mies.** |

### B. Pięciu klientów zewnętrznych

| Pozycja | Miesięcznie |
|---|---|
| Serwer aplikacyjny (CPX41) | ~130 PLN |
| Serwer bazodanowy (CPX41, oddzielny) | ~130 PLN |
| Object storage 3 TB | ~55 PLN |
| Backup z PITR | ~60 PLN |
| API Claude — ekstrakcja (~300 cenników, 20% przez LLM) | ~60 PLN |
| API Claude — copilot (~1 500 zapytań, z cache) | ~120 PLN |
| Powiadomienia SMS (alerty ETA, wygasające stawki) | ~50 PLN |
| Certyfikaty, domeny, drobne | ~50 PLN |
| **Razem** | **~650 PLN/mies.** |

Koszt krańcowy jednego klienta: **60–90 PLN miesięcznie.**

### C. Dwudziestu klientów

| Pozycja | Miesięcznie |
|---|---|
| Serwer dedykowany (AX52 lub 3× CPX51) | ~450 PLN |
| Replika bazy + storage 10 TB | ~250 PLN |
| Backup i DR | ~150 PLN |
| API Claude — ekstrakcja (~1 200 cenników) | ~250 PLN |
| API Claude — copilot i raporty | ~450 PLN |
| SMS, mail transakcyjny | ~200 PLN |
| Certyfikaty, domeny, licencje | ~150 PLN |
| **Razem** | **~1 900 PLN/mies.** |

Koszt krańcowy jednego klienta: **~95 PLN.** Przy cenie abonamentu 1 200–2 500 PLN marża brutto przekracza 92%.

---

## 4. Co jest darmowe, a wygląda drogo

- **KSeF** — API i środowisko testowe bez opłat. Płacisz tylko za certyfikat kwalifikowany do pieczęci, ~300–600 PLN rocznie
- **GUS/REGON (BIR)** — klucz API za darmo po złożeniu wniosku
- **Biała lista podatników VAT** — API Ministerstwa Finansów, bez opłat
- **VIES** — bez opłat
- **Kursy NBP** — publiczne API, bez limitów w praktyce
- **UN/LOCODE** — dane publiczne
- **Cała warstwa monitoringu** — Sentry, Langfuse, Grafana, Uptime Kuma we własnym hostingu kosztują tylko RAM

---

## 5. Koszty, o których się zapomina

| Pozycja | Skala |
|---|---|
| **Utrzymanie** | 15–20% rocznie kosztu wytworzenia. Przy 1 000 godzin budowy to 150–200 godzin rocznie tylko na to, żeby nie przestało działać |
| **Zmiany regulacyjne** | Schema KSeF już raz się zmieniła. Każda zmiana FA to kilkadziesiąt godzin |
| **Wycofywanie modeli** | Modele są wycofywane. Twoje prompty i zbiór testowy muszą przeżyć migrację — dlatego `promptfoo` i `label-studio` nie są opcjonalne |
| **Wsparcie klientów** | Przy pięciu klientach to 10–20 godzin miesięcznie. Przy dwudziestu — etat |
| **Aktualizacje bezpieczeństwa** | Kilka godzin miesięcznie, niezależnie od skali |
| **Awaria** | Nie „czy", tylko „kiedy". Budżetuj dzień pracy kwartalnie |

---

## 6. Podsumowanie liczbowe

| | Faza budowy | Solo | 5 klientów | 20 klientów |
|---|---|---|---|---|
| Gotówka miesięcznie | 300–1 200 PLN | ~200 PLN | ~650 PLN | ~1 900 PLN |
| Gotówka rocznie | 4–14 tys. PLN | 2,4 tys. PLN | 7,8 tys. PLN | 23 tys. PLN |
| Twój czas rocznie | 800–1 000 h | ~150 h | ~350 h | etat + wsparcie |

**Wniosek, który ma znaczenie biznesowe:** koszty gotówkowe tego systemu są nieistotne. Nawet w wariancie na dwadzieścia firm mieszczą się w cenie jednego abonamentu, który ci klienci dziś płacą komuś innemu. Ograniczeniem nie są pieniądze — jest nim twój czas, a przy trzecim czy czwartym kliencie wsparcie zacznie zjadać godziny, których potrzebujesz na rozwój.

To jest moment, w którym decyduje się, czy to jest narzędzie dla LOGMAR-u, czy produkt. Warto wiedzieć wcześniej, bo obie odpowiedzi są dobre — ale prowadzą do zupełnie innych decyzji projektowych.
