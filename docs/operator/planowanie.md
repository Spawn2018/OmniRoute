# Planowanie

Na `/planning` dyspozytor otwiera **leniwy overlay przejazdów**. To nie mapa GPS i nie wieża wyjątków.

1. Zaloguj się. Wejdź na Planowanie.
2. Rozwiń „Pokaż overlay przejazdów”. Wtedy dopiero wczytuje się osobny chunk JS — nie ma go w paczce startowej.
3. Lista to te same `trip`, co na zleceniach: numer i opcjonalny `route_label`. Nie ma współrzędnych i nie ma kafelków OSM.

Czego tu nie ma: leaflet, mapbox, `tile.openstreetmap.org`, cztery widoki Timeline/Blocks/Table/Legs, klawiatura N10, select&drop, polygon, podkłady X8, SQL marży, live HTTP.

Nazwy w kodzie: `planning` · `trip` · `/planning`.
