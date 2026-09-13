# Ekstrakcja cennika

Na `/extractions` składasz szkic z tekstu albo pliku. Model tylko proponuje
kandydatów. Nic nie idzie do stawek, dopóki nie wciśniesz Akceptuj.

1. Ustaw sesję tenanta. Rodzaj szkicu zostaw `rate_line`, jeśli poprawiasz cennik.
2. Wklej tekst albo wybierz plik. `source_ref` musi wskazywać dokument.
3. „Ekstrahuj → szkic”. Otwórz wiersz. Popraw kod, kwotę jako tekst, walutę i notatkę.
4. „Zapisz poprawkę” zapisuje tylko listę kandydatów. Źródło i nierozpoznane fragmenty zostają.
5. Potem Akceptuj (stawka kupna) albo Odrzuć. Szkic już zaakceptowany nie przyjmie poprawki.

Czego tu nie ma: ponowne wołanie modelu, zapis `charge`, wersja szkicu, ramka na PDF,
pewność, edycja oferty kanału albo przyjęcia RFP. Marża zostaje na `/charges`.

Nazwy w kodzie: `extraction_draft` · `payload.candidates` · `amount_text` · `source_ref`.
