# Ekstrakcja cennika

Na `/extractions` składasz szkic z tekstu albo pliku. Model tylko proponuje
kandydatów. Nic nie idzie do stawek, dopóki nie wciśniesz Akceptuj.

1. Ustaw sesję tenanta. Rodzaj szkicu zostaw `rate_line`, jeśli poprawiasz cennik.
2. Wybierz ścieżkę `text` albo `image`. `image` to tylko etykieta — plik i tak idzie przez obecny parser do tekstu.
3. Wklej tekst albo wybierz plik. `source_ref` musi wskazywać dokument.
4. „Ekstrahuj → szkic”. Otwórz wiersz. Nowy szkic ma wersję 0. Ścieżka `image` nie uruchamia osobnego modelu na pikselach.
5. Popraw kod, kwotę jako tekst, walutę, notatkę, ramkę i pewność (tekst, nie liczba z modelu).
6. „Zapisz poprawkę” podnosi wersję o jeden. Źródło i nierozpoznane fragmenty zostają.
7. Potem Akceptuj (stawka kupna) albo Odrzuć. Szkic już zaakceptowany nie przyjmie poprawki.

Czego tu nie ma: historia kopii wiersza, ponowne wołanie modelu, zapis `charge`,
rysowanie ramki na PDF, edycja oferty kanału albo przyjęcia RFP. Marża zostaje na `/charges`.

Nazwy w kodzie: `extraction_draft` · `payload.revision` · `payload.extract_path` · `bbox_text` · `confidence_text`.
