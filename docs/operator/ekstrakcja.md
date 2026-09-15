# Ekstrakcja cennika

Na `/extractions` składasz szkic z tekstu albo pliku. Model tylko proponuje
kandydatów. Nic nie idzie do stawek, dopóki nie wciśniesz Akceptuj.

1. Ustaw sesję tenanta. Rodzaj szkicu zostaw `rate_line`, jeśli poprawiasz cennik.
2. Wybierz ścieżkę `text` albo `image`. `image` to tylko etykieta — plik i tak idzie przez obecny parser do tekstu.
3. Wklej tekst albo wybierz plik (PDF, tekst, `.xlsx` albo `.xls`). Przy Excelu
   wybierz arkusz przez `sheet_index` (od zera) albo `sheet_name` (dokładna nazwa).
   `.xlsx` czyta openpyxl (wartości z cache formuł, gdy Excel je zapisał).
   `source_ref` musi wskazywać dokument.
4. „Ekstrahuj → szkic”. Otwórz wiersz. Nowy szkic ma wersję 0. Ścieżka `image` nie uruchamia osobnego modelu na pikselach.
5. Popraw kod, kwotę jako tekst, walutę, notatkę, ramkę i pewność (tekst, nie liczba z modelu).
   Działa dla szkiców `rate_line`, `carrier_quote` i `tender_rfp`.
6. „Zapisz poprawkę” podnosi wersję o jeden i dopisuje poprzednich kandydatów
   do `payload.history` (JSONB, nie osobna tabela). Źródło i nierozpoznane fragmenty zostają.
7. Potem Akceptuj (stawka kupna) albo Odrzuć. Przy `rate_line` zaznacz checkboxami,
   których kandydatów zapisać — reszta zostaje w szkicu `pending`. Accept czyta
   bieżących kandydatów — nie historię. Quote/RFP nadal akceptujesz w całości.

Czego tu nie ma: cofanie do starej wersji, ponowne wołanie modelu, zapis `charge`,
rysowanie ramki na PDF. Marża zostaje na `/charges`.

Przy dwóch i więcej **zaznaczonych** kandydatach Akceptuj działa tylko gdy każdy
ma pewność co najmniej progu tenanta `hitl_confidence_min` z `/organization-settings`
(domyślnie 0,70; tekst `0.70` / `70%` / `green` / `yellow` / `high`).
Pusty, `orange`, `hold` albo niższy ułamek blokuje zbiorczą akceptację — popraw
pewność, zaznacz jednego kandydata albo podnieś próg w ustawieniach.

Nazwy w kodzie: `extraction_draft` · `payload.revision` · `payload.history` ·
`candidate_indexes` · `payload.extract_path` · `bbox_text` · `confidence_text` ·
`hitl_confidence_min` · brama zbiorcza 501.0 · partial 504.0 · ustawienie 505.0.
