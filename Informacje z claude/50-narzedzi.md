# 50 narzędzi — poza Claude i Cursorem

Usługi i aplikacje, nie repozytoria. Ceny orientacyjne, sierpień 2026. Oznaczenia: **[0]** darmowe lub darmowy plan wystarczający, **[$]** płatne, **[!]** wdrożyć od razu.

---

## A. Praca z kodem i AI (9)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 1 | **Claude Code** [!] | Agent terminalowy do zadań wieloplikowych: migracje w 12 plikach naraz, refaktory, których Cursor nie ogarnia. Uzupełnia Cursora, nie zastępuje | w subskrypcji |
| 2 | **Projekty w Claude** [!] | Wrzuć tam wszystkie pliki spec'a. Każda rozmowa startuje z pełnym kontekstem systemu zamiast tłumaczenia od zera | w subskrypcji |
| 3 | **Anthropic Console** [!] | Warsztat promptów z porównaniem wersji obok siebie. Tu iterujesz prompt ekstrakcji, nie w kodzie | per użycie |
| 4 | **Repomix** albo **gitingest** | Pakuje całe repo w jeden plik pod kontekst modelu. Nieocenione przy pytaniu „co jeszcze muszę zmienić" | [0] |
| 5 | **v0.dev** | Generuje komponenty UI z opisu. Szybki szkic ekranu przed dopracowaniem w Cursorze | [$] ~$20/mies. |
| 6 | **Warp** | Terminal z AI i historią poleceń. Skraca pracę operacyjną wokół projektu | [0] / [$] |
| 7 | **OpenRouter** | Jedno API do kilkuset modeli. Do porównania, który model najlepiej parsuje twoje cenniki — bez zakładania konta u każdego dostawcy | per użycie |
| 8 | **Voyage AI** albo **Jina Embeddings** | Embeddingi jako usługa. Alternatywa dla lokalnego modelu przy mapowaniu nazw opłat | per użycie |
| 9 | **GitHub Copilot** | Autouzupełnianie w tle, inny model niż Cursor. Warto mieć drugą opinię przy kodzie krytycznym | [$] ~$10/mies. |

## B. Baza danych (6)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 10 | **Neon** [!] | Postgres z gałęziowaniem bazy. **Osobna kopia bazy per pull request** — testujesz migrację na realnych danych bez ryzyka. Przy jednoosobowym zespole to sieć bezpieczeństwa | [0] / od $19 |
| 11 | **Supabase** | Postgres + auth + storage + RLS z pudełka. Rozważ jako skrót do multi-tenancy zamiast budowania od zera | [0] / $25 |
| 12 | **DBeaver** | Klient SQL, wszystko obsługuje, darmowy | [0] |
| 13 | **TablePlus** | Szybszy i przyjemniejszy, płatny | [$] ~$90 raz |
| 14 | **Azimutt** | Wizualna eksploracja schematu. Przy 40 tabelach jedyny sposób, żeby ogarnąć całość wzrokiem | [0] |
| 15 | **dbdiagram.io** | Model danych jako tekst → diagram. Dobre wejście dla Cursora i do rozmów z klientem | [0] / [$] |

## C. API i testowanie (4)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 16 | **Bruno** | Klient API działający lokalnie, kolekcje trzymane w gicie. Lepszy od Postmana, bo nie wymaga konta i chmury | [0] |
| 17 | **Hoppscotch** | Wersja przeglądarkowa, gdy nie chcesz instalować | [0] |
| 18 | **ngrok** | Tunel do lokalnego serwera. Niezbędny przy webhookach z KSeF i EmailEngine | [0] / [$] |
| 19 | **Mailtrap** | Przechwytywanie maili testowych. Zanim wyślesz ofertę testową prawdziwemu klientowi | [0] |

## D. Hosting i wdrożenie (6)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 20 | **Hetzner** [!] | Najlepszy stosunek mocy do ceny w Europie. Serwery w Niemczech i Finlandii — dane w UE, argument sprzedażowy | od €5/mies. |
| 21 | **Cloudflare** [!] | DNS, WAF, ochrona przed botami, R2 jako storage bez opłat za transfer, Tunnel zamiast otwierania portów | [0] w większości |
| 22 | **Railway** | Deploy bez konfiguracji. Dobre na środowisko demonstracyjne dla klientów | [$] od $5 |
| 23 | **Fly.io** | Aplikacja blisko użytkownika, dobre skalowanie do zera | [$] per użycie |
| 24 | **Vercel** | Hosting frontendu, jeśli oddzielisz go od API | [0] / [$] |
| 25 | **Coolify** | Własne PaaS na serwerze Hetznera. Deploy przez `git push` bez płacenia za Railway | [0] self-hosted |

## E. Obserwowalność (5)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 26 | **Sentry** [!] | Błędy produkcyjne ze śladem stosu i kontekstem. Pierwsza rzecz po pierwszym wdrożeniu | [0] do 5 tys. zdarzeń |
| 27 | **Langfuse Cloud** [!] | Historia promptów, kosztów i opóźnień. Bez tego pipeline ekstrakcji jest czarną skrzynką | [0] / od $29 |
| 28 | **Better Stack** | Monitoring dostępności z powiadomieniem na telefon. Dowiadujesz się przed klientem | [0] / [$] |
| 29 | **Axiom** | Logi z hojnym darmowym planem | [0] do 500 GB |
| 30 | **PostHog Cloud** [!] | Kto czego używa. Zbudujesz dwadzieścia funkcji, klienci użyją pięciu — bez tego nie wiesz których | [0] do 1 mln zdarzeń |

## F. Praca i dokumentacja (5)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 31 | **Linear** | Zadania i błędy. Szybki, nie przeszkadza. Przy jednej osobie wystarczy darmowy plan | [0] / $8 |
| 32 | **Obsidian** | Notatki lokalnie w markdownie — te same pliki, które czyta Cursor i Claude | [0] |
| 33 | **Excalidraw** | Szkice architektury, które nie udają dokumentacji | [0] |
| 34 | **Figma** | Projekt interfejsu przed kodowaniem. Nawet szkicowo — oszczędza przerabianie ekranów | [0] |
| 35 | **Tldraw** | Szybkie diagramy z eksportem, dobrze współpracuje z modelami | [0] |

## G. Sprzedaż produktu (7)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 36 | **Loom** [!] | Nagranie demo systemu. **W sprzedaży jednoosobowego SaaS to najskuteczniejsze narzędzie** — wysyłasz pięciominutowy film zamiast umawiać spotkanie, klient ogląda o 22:00 | [0] / $15 |
| 37 | **Cal.com** | Umawianie demo bez wymiany maili | [0] self-hosted |
| 38 | **Attio** albo **HubSpot Free** | CRM na proces sprzedaży. Ironiczne, ale nie prowadź go w Excelu | [0] / [$] |
| 39 | **Paddle** [!] | Rozliczenia jako Merchant of Record — **przejmuje obowiązek VAT w całej UE**. Przy sprzedaży do Czech, Niemiec czy Litwy oszczędza ci rejestracji VAT OSS i księgowości transgranicznej | ~5% + $0,50 |
| 40 | **Stripe** | Alternatywa, tańsza, ale VAT rozliczasz sam | 1,4–2,9% |
| 41 | **Crisp** | Czat wsparcia w aplikacji | [0] / [$] |
| 42 | **Typedream** albo **Framer** | Strona produktowa bez kodowania. Nie buduj jej w Reakcie — to strata tygodnia | [$] ~$15 |

## H. Polska administracja (5)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 43 | **Środowisko testowe KSeF** [!] | Wersja demo Ministerstwa Finansów. Integrację testujesz tu, nie na produkcji | [0] |
| 44 | **Wniosek o klucz GUS BIR** [!] | Autouzupełnianie kontrahenta po NIP. Wniosek trwa kilka dni — złóż na starcie, nie gdy będzie potrzebny | [0] |
| 45 | **API białej listy VAT** | Weryfikacja rachunku bankowego kontrahenta | [0] |
| 46 | **Certyfikat kwalifikowany** (KIR, Certum, EuroCert) | Pieczęć elektroniczna do KSeF i podpisu dokumentów | ~300–600 zł/rok |
| 47 | **API NBP** | Kursy do przeliczeń walutowych, tabela A | [0] |

## I. Firma i bezpieczeństwo (3)

| # | Narzędzie | Po co | Koszt |
|---|---|---|---|
| 48 | **Bitwarden** albo **1Password** [!] | Hasła i klucze API. Nie w `.env` w repozytorium | [0] / ~$3 |
| 49 | **Doppler** albo **Infisical** | Sekrety per środowisko, wstrzykiwane przy deployu | [0] / [$] |
| 50 | **Ubezpieczenie OC działalności IT** [!] | Broker specjalizujący się w IT. Twój system liczy ceny — błąd to szkoda majątkowa u klienta. Jedna z pozycji, przy której nie ma sensu oszczędzać | kilka tys. zł/rok |

---

## Minimum na start

Dziewięć pozycji, reszta gdy będzie potrzebna:

**Claude Code** + **Projekty w Claude** + **Anthropic Console** (masz w subskrypcji) · **Neon** · **Hetzner** · **Cloudflare** · **Sentry** · **Langfuse** · **Bitwarden**

Koszt: około 150 zł miesięcznie ponad to, co już płacisz.

## Trzy, które warto wdrożyć wcześniej, niż podpowiada intuicja

**Neon z gałęziowaniem bazy** — bo pierwszą migrację, która zepsuje dane, zrobisz w trzecim miesiącu, a nie w trzynastym.

**Loom** — bo nagrasz demo tego, co masz po fazie 1, wyślesz do trzech spedytorów i dostaniesz odpowiedź na pytanie „czy to komuś potrzebne" pół roku przed tym, niż planowałeś.

**Wniosek o klucz GUS** — bo trwa kilka dni i zawsze okazuje się potrzebny akurat w piątek wieczorem.
