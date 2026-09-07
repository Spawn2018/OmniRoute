# Podkłady map — instrukcja dla administratora tenanta

To jest szkic pomocy w aplikacji (ekran Ustawienia organizacji → Mapa). Klucze szyfruje OmniRoute kluczem tenanta. Nie wklejaj kluczy do czatu z supportem ani do ticketu.

OmniRoute **nie sprzedaje** map. Płacisz dostawcy bezpośrednio. My tylko wołamy jego kafelki z Twoim kluczem.

## 1. Co robi użytkownik, a co admin

| Kto | Co |
|---|---|
| Każdy użytkownik | W **Ustawieniach użytkownika → Mapa** włącza i wyłącza darmowe podkłady oraz wybiera domyślny. Bez kluczy. |
| Administrator organizacji | W **Ustawieniach organizacji → Mapa** dodaje płatnych dostawców (klucz API) i decyduje, które z nich widzi zespół. |

## 2. Darmowe podkłady (nic nie kupujesz)

Włączasz je u siebie. Działają od razu:

- **OpenFreeMap** — mapa drogowa, kilka stylów (jasny / ciemny / liberty). Bez rejestracji.
- **OpenTopoMap** — rzeźba terenu.
- **CyclOSM** — drogi rowerowe / dojazd.
- **Humanitarian (HOT)** — czytelna w kryzysie / słabym kontraście.
- **Geoportal GUGiK** — ortofotomapa i mapa topograficzna Polski (dane otwarte).
- **Esri World Imagery** — zdjęcia lotnicze (zostaw atrybucję Esri).

Nie używamy serwera kafelków `openstreetmap.org` jako produkcyjnego CDN — tak każe polityka fundacji OSM. Dane OSM i tak są w OpenFreeMap / Geoportalu.

Opcja zaawansowana: **własny plik Protomaps (PMTiles)** na Waszym storage — bez abonamentu mapowego. Wymaga hostowania pliku; nie jest to „klucz API”.

## 3. Płatne podkłady — skąd wziąć klucz

We wszystkich przypadkach: załóż konto u dostawcy → utwórz klucz → **ogranicz go do Waszej domeny** (np. `app.wasza-firma.pl`) → wklej w OmniRoute → zapisz. Klucz bez ograniczenia domeny może ktoś ukraść i wypalić Wam budżet.

### Mapbox

1. Wejdź na [account.mapbox.com](https://account.mapbox.com/) i załóż konto.
2. Access tokens → Create a token.
3. Wklej **public token** (`pk.…`) do OmniRoute. Secret token (`sk.…`) zostaw w Mapbox — nie nadaje się do mapy w przeglądarce.
4. W Mapbox: URL restrictions na Waszą domenę.
5. Cennik: [mapbox.com/pricing](https://www.mapbox.com/pricing) — darmowy próg, potem za ładowania mapy.

### MapTiler

1. [cloud.maptiler.com](https://cloud.maptiler.com/) → Sign up.
2. Account → API keys → skopiuj klucz.
3. Wklej do OmniRoute. Wybierz styl (streets, outdoor, satellite).
4. Cennik: [maptiler.com/cloud/pricing](https://www.maptiler.com/cloud/pricing).

### Google Maps Platform

1. [console.cloud.google.com](https://console.cloud.google.com/) → nowy projekt.
2. Włącz **Maps JavaScript API** (i ewentualnie Map Tiles API).
3. Klucze API → utwórz klucz → ograniczenie HTTP referrer + ograniczenie do tych API.
4. Podłącz kartę rozliczeniową — bez niej mapa często nie wstanie.
5. Wklej klucz do OmniRoute.
6. Cennik: [developers.google.com/maps/billing-and-pricing](https://developers.google.com/maps/billing-and-pricing).

### HERE

1. [platform.here.com](https://platform.here.com/) → rejestracja.
2. Utwórz aplikację / API key (HERE v3: `apiKey`).
3. Wklej do OmniRoute. Styl: raster lub wektor (wg dokumentacji HERE Map).
4. Uwaga licencyjna: HERE jako **podkład** ≠ licencja na telematykę floty. Routing ciężarowy to osobny produkt.
5. Cennik: [here.com/get-started/pricing](https://www.here.com/get-started/pricing).

### TomTom

1. [developer.tomtom.com](https://developer.tomtom.com/) → Register.
2. Dashboard → API Keys.
3. Włącz Map Display API. Wklej klucz do OmniRoute.
4. Cennik: [developer.tomtom.com/help/account/pricing](https://developer.tomtom.com/help/account/pricing).

### PTV (Logistics)

1. Konto [developer.myptv.com](https://developer.myptv.com/).
2. Klucz do Map / Raster Maps (osobno od Routing API używanego do myta).
3. Wklej do OmniRoute.
4. Cennik według umowy PTV.

### Stadia Maps (w tym style Stamen)

1. [client.stadiamaps.com](https://client.stadiamaps.com/) → Sign up.
2. Properties → API key.
3. Wklej do OmniRoute. Style: Alidade, Osmium, Stamen Toner/Terrain/Watercolor.
4. Cennik: [stadiamaps.com/pricing](https://stadiamaps.com/pricing).

### Thunderforest

1. [thunderforest.com](https://www.thunderforest.com/) → Account.
2. Klucz + styl (Transport, Outdoors, Atlas, Neighbourhood).
3. Dobry pod ciężarówki (warstwa Transport).
4. Cennik na stronie konta.

### Jawg

1. [www.jawg.io](https://www.jawg.io/) → Lab / Access token.
2. Wklej token do OmniRoute.

### Azure Maps (następca Bing)

1. [portal.azure.com](https://portal.azure.com/) → utwórz zasób Azure Maps.
2. Klucz z zakładki Authentication (primary key).
3. Wklej do OmniRoute.
4. Wymaga subskrypcji Azure.

### Esri ArcGIS

1. [developers.arcgis.com](https://developers.arcgis.com/) → API key.
2. Włącz basemap services.
3. Wklej do OmniRoute. Atrybucja Esri obowiązkowa.

### Geoapify / LocationIQ

1. Geoapify: [myprojects.geoapify.com](https://myprojects.geoapify.com/) → API key.  
   LocationIQ: [locationiq.com](https://locationiq.com/) → dashboard.
2. Wklej klucz. Tańsze progi niż Google/Mapbox — sprawdź limit kafelków.

## 4. Po wklejeniu klucza w OmniRoute

1. Test: otwórz mapę planowania — podkład musi się załadować, atrybucja widoczna.
2. Jeśli szara mapa: zły klucz, brak billing u Google, albo domena nie jest na allowlist.
3. Rotacja: nowy klucz u dostawcy → wklej nowy w OmniRoute → stary unieważnij u dostawcy.
4. Wyłączenie: admin gasi podkład — użytkownicy wracają do darmowego.

## 5. Czego tu nie ma

- OmniRoute nie trzyma Waszej karty mapowej.
- Klucz nie idzie do PostHog ani do logów.
- Routing / myto / geokodowanie to **osobne** klucze (często ten sam vendor, inny produkt) — nie mieszaj z podkładem.
