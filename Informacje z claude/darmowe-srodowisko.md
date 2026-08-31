# Darmowe środowisko — co udźwignie, a gdzie jest granica

Stan na sierpień 2026.

**Wniosek na wstępie:** całą fazę budowy przeprowadzisz za zero złotych, na sprzęcie mocniejszym niż płatny VPS za 60 zł. Produkcji z cudzymi danymi handlowymi na darmowym tierze nie postawisz — i nie z powodu wydajności, tylko z powodu umowy powierzenia i braku SLA. Granica przebiega dokładnie w momencie pierwszego klienta zewnętrznego.

---

## 1. Warstwa lokalna — najważniejsza i całkowicie darmowa

90% pracy przez pierwsze pół roku wykonasz na własnym laptopie. Docker Compose, zero kosztu, zero limitów, pełna kontrola.

```yaml
# docker-compose.dev.yml — cały stack lokalnie
services:
  postgres:      # baza + pgvector + pg_trgm
  redis:         # cache
  minio:         # storage dokumentów, S3-kompatybilny
  mailpit:       # przechwytywanie maili testowych
  langfuse:      # telemetria promptów, self-hosted
  api:           # FastAPI
  worker:        # procrastinate
  web:           # Vite dev server
```

Wszystko poza tym, co wymaga internetu (API Claude, KSeF sandbox, portale armatorów), działa offline.

**Wymagania:** 16 GB RAM wystarczy z zapasem, 32 GB komfortowo. Docling i Marker do parsowania cenników są najbardziej wymagające — jeśli laptop siada, wynieś je do osobnego kontenera na serwerze z punktu 2.

## 2. Darmowy serwer w chmurze — Oracle Always Free

Najmocniejsza darmowa oferta na rynku, ale z pułapkami.

### Co dostajesz

- **Ampere A1 (ARM): 2 OCPU + 12 GB RAM** — po cichej redukcji z 4 OCPU i 24 GB, obowiązującej od 15 czerwca 2026. Oracle nie opublikował ogłoszenia ani nie powiadomił użytkowników; zmieniono dokumentację i tyle. Instancje przekraczające nowy limit są usuwane od 18 sierpnia
- 200 GB block storage NVMe
- 10 TB transferu wychodzącego miesięcznie
- 2 mikroinstancje AMD (1/8 OCPU, 1 GB RAM) — na drobiazgi
- Bez terminu wygaśnięcia

### Pułapki, o których trzeba wiedzieć

**Wybór regionu jest nieodwracalny.** Zasoby Always Free są przypisane do regionu domowego i nie da się go później zmienić. Wybierz taki, który obsługuje kształty Ampere A1 — duże regiony z trzema domenami dostępności mają lepszą dostępność sprzętu niż jednodomenowe.

**„Out of host capacity".** Regiony amerykańskie potrafią odmawiać przez godziny lub dni; Frankfurt, Singapur i Tokio zwykle udostępniają instancję w kilka minut. Dla ciebie Frankfurt jest optymalny — bliski, w UE, dobra dostępność.

**Karta wymagana.** Weryfikacja tożsamości z tymczasową blokadą 1 USD. Zasoby Always Free nie są obciążane.

**Odzyskiwanie nieaktywnych instancji.** Utrzymuj minimalne obciążenie, żeby instancja nie została uznana za porzuconą.

**ARM.** Sprawdź, czy obrazy Docker mają wersje ARM64. Większość ma, ale nie wszystkie. Parsowanie dokumentów na ARM CPU jest wolniejsze — w praktyce bez znaczenia, bo ciężką ekstrakcję i tak robi API Claude.

**Zmiany bez zapowiedzi.** To, co wydarzyło się w czerwcu, może się powtórzyć. Nie buduj na tym niczego, czego utrata bolałaby bardziej niż jeden wieczór.

## 3. Darmowe usługi zewnętrzne

| Usługa | Limit darmowy | Do czego |
|---|---|---|
| **GitHub** | prywatne repo bez limitu, Actions 2 000 min/mies, Codespaces 60 h/mies | kod, CI, środowisko w przeglądarce |
| **Cloudflare** | DNS, WAF, Tunnel, R2 do 10 GB | **Tunnel jest kluczowy** — pokazujesz demo z laptopa bez publicznego IP i bez hostingu |
| **Neon** | Postgres 0,5 GB + gałęziowanie | osobna kopia bazy per pull request |
| **Supabase** | 500 MB bazy, 1 GB storage, auth | jeśli pójdziesz skrótem do multi-tenancy |
| **Sentry** | 5 000 zdarzeń/mies | błędy produkcyjne |
| **PostHog** | 1 mln zdarzeń/mies | analityka użycia — hojny limit, wystarczy długo |
| **Langfuse Cloud** | plan darmowy | alternatywa dla self-hosted |
| **Better Stack** | monitoring podstawowy | alert, gdy padnie |
| **Cal.com** | self-hosted | umawianie demo |
| **Loom** | 25 nagrań do 5 min | demo dla spedytorów |
| **Figma** | 3 pliki | szkic interfejsu |
| **Linear** | do 250 zadań | zadania i błędy |
| **Hugging Face Spaces** | CPU | demo Streamlit twojego silnika rentowności |

## 4. Darmowe API — branżowe i polskie

Tu nie ma haczyka, to naprawdę jest darmowe:

- **KSeF** — API i środowisko testowe bez opłat
- **GUS BIR (REGON)** — klucz po wniosku; `bigzbig/regonapi` ma sandbox działający **bez klucza**, możesz zacząć dziś
- **Biała lista podatników VAT** — API Ministerstwa Finansów
- **VIES** — weryfikacja VAT UE
- **NBP** — kursy walut, tabela A
- **Portale deweloperskie armatorów** — Maersk, CMA CGM, Hapag-Lloyd mają samoobsługowe rejestracje z sandboxami
- **UN/LOCODE** — dane publiczne
- **GDELT, FRED, Eurostat** — do modułu rynkowego z Aneksu 2

## 5. Co nie będzie darmowe

| Pozycja | Koszt | Czy warto oszczędzać |
|---|---|---|
| API Claude | ~12–50 zł/mies przy twoim wolumenie | **Nie.** To nie jest koszt tego systemu |
| Backup poza serwerem | ~25 zł/mies | **Absolutnie nie.** Utrata bazy kończy firmę |
| Domena | ~120 zł/rok | nie ma na czym |
| Certyfikat kwalifikowany (KSeF) | 300–600 zł/rok | wymagany |
| OC działalności IT | kilka tys. zł/rok | **Nie.** System liczy ceny, błąd to szkoda majątkowa |

Razem minimum realne: **około 100 zł miesięcznie** przez całą fazę budowy, licząc z API i backupem.

## 6. Gdzie przebiega granica

Darmowy tier kończy się nie na wydajności, tylko na trzech rzeczach, których nie da się obejść:

**Umowa powierzenia.** Przy pierwszym kliencie zewnętrznym potrzebujesz dostawcy, który podpisze DPA i wskaże lokalizację przetwarzania. Duzi (Oracle, AWS, GCP) dają to nawet przy darmowym koncie — mniejsi platformy często nie.

**SLA.** Darmowy tier nie ma żadnego. Nie możesz obiecać klientowi dostępności na infrastrukturze, która może zostać wyłączona bez powiadomienia — a właśnie zobaczyłeś, że Oracle potrafi zmienić warunki bez ogłoszenia.

**Backup i odtwarzanie.** 200 GB block storage to nie jest kopia zapasowa. Potrzebujesz `pgbackrest` z odtwarzaniem do punktu w czasie i składowaniem poza tym samym dostawcą.

**Moment przejścia: pierwszy płacący klient zewnętrzny.** Nie wcześniej — to strata pieniędzy. Nie później — to ryzyko, którego nie chcesz brać.

Docelowo: Hetzner CPX31 za około 60 zł miesięcznie, dane w Niemczech lub Finlandii, DPA dostępne, plus backup poza dostawcą. Przejście z Oracle na Hetzner to przeniesienie tego samego `docker-compose`.

## 7. Konfiguracja startowa — kolejność

**Dziś:**
1. Docker Compose lokalnie, cały stack z punktu 1
2. Repozytorium prywatne na GitHubie
3. Konto Oracle Cloud, region **Frankfurt**, instancja A1 2 OCPU / 12 GB
4. Cloudflare: domena, DNS, Tunnel do laptopa

**W tym tygodniu:**
5. Wniosek o klucz GUS BIR (kilka dni oczekiwania — złóż teraz)
6. Rejestracje w portalach deweloperskich Hapaga, Maerska, CMA CGM
7. Konto testowe KSeF
8. Neon — darmowa baza z gałęziowaniem pod pull requesty

**Gdy pojawi się pierwszy kod:**
9. Sentry, PostHog, Langfuse — darmowe plany
10. Renovate na repozytorium

Wszystko powyżej: zero złotych, poza domeną.

## 8. Ostrzeżenie na koniec

Darmowe środowisko jest właściwym wyborem na fazę budowy i błędnym na produkcję. Kuszące będzie zostanie na nim „jeszcze chwilę" po pierwszym kliencie, bo działa i nic nie kosztuje.

Nie rób tego. Nie z powodu wydajności — 2 OCPU i 12 GB spokojnie obsłuży pięciu klientów. Z powodu tego, że w dniu, w którym Oracle zmieni warunki po raz kolejny albo instancja zostanie odzyskana jako nieaktywna, będziesz tłumaczył spedytorowi, dlaczego nie widzi swoich stawek. Sześćdziesiąt złotych miesięcznie to najtańsze ubezpieczenie w całym tym projekcie.
