# Ścieżka pieniądza

Operator nie liczy marży na ekranie. Kwota kupna siedzi na niezmienialnej stawce. Sprzedaż i kupno spotykają się na jednym wierszu opłaty. Oferta tylko **kopiuje** bieżącą stawkę — nie przelicza.

1. Wchodzisz na kolejkę szkiców. Model językowy **proponuje** linie z cennika. Nic z tego nie jest jeszcze w stawek ani w marży.
2. Recenzent akceptuje albo odrzuca. Dopiero akceptacja zapisuje stawkę kupna z pochodzeniem (`source_ref`). Odrzut zostawia szkic poza katalogiem.
3. Na katalogu stawek widać kwotę i walutę nierozłącznie. Zmiana stawki to nowy wiersz, nie edycja starego.
4. Na katalogu opłat operator podaje kupno i sprzedaż. Marża liczy się z tej pary w domenie, nie w arkuszu i nie w modelu.
5. Wycena bierze **aktualną** stawkę danego kodu (ta bez następcy) i wstawia ofertę z tą kwotą. Brak stawki = luka, nie zgadywanie. Na `/quotations` możesz wybrać zapytanie z poczty (`customer_rfq`) i kod HS/CN z katalogu. Kontrahent musi już siedzieć na zapytaniu (Dopasuj nadawcę). Porty i kod opłaty podajesz Ty. Kod towarowy nie zmienia kwoty. Kwota nadal schodzi ze stawki — nie wpisujesz jej i model jej nie liczy. „Porównanie odpowiedzi” pokazuje wycenę i ofertę kanału obok siebie. „Zapisz marżę” zapisuje opłatę (kupno z kanału, sprzedaż z wyceny); marża liczy się w domenie, nie w przeglądarce.
6. Na dokumencie oferty „Nadaj numer” zapisuje etykietę z prefiksu organizacji (ustawienia), nie z głowy i nie z modelu. Drugie kliknięcie nie zmienia numeru. „Drukuj” chowa menu i nagłówek arkuszem 57.0 — to nie nowy PDF i nie wysyłka.

Czego tu nie ma: przeliczenia kursem NBP na kwocie, magazynu, WZ, aplikacji na telefon. Kurs średni NBP jest katalogiem do podglądu. Zlecenie i FV to na razie odczyt tych samych kwot, nie osobna księga.

Nazwy w kodzie: `extraction_draft` → `rate_line` → `charge` (`margin`) → `quotation`.
