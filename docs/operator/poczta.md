# Poczta — wiadomość fixture

Na `/mail` zapisujesz wiadomość przychodzącą ręcznie, jak w teście. To nie jest skrzynka z sieci.

1. Wejdź na Poczta. Góra ekranu to lista `inbound_message`, dół to znane adresy kontrahenta.
2. W `source_ref` zostaw pin `fixture://inbound-mail/…` albo `synth://…`. Adres IMAP albo Graph nie przejdzie.
3. Wpisz nadawcę, temat i treść. Opcjonalnie Message-ID i In-Reply-To — to nagłówki wątku poczty, nie `external_id` skrzynki. Puste pola zostają puste. Status zawsze `draft` — serwer go ustawia, nie Ty.
4. Zapisz. Wiersz należy do Twojej firmy. Inny tenant go nie zobaczy.
5. Znane domeny i kontakty niżej to odczyt karty kontrahenta. Przycisk „Dopasuj nadawcę” woła `resolve_email` na adresie z wiadomości i zapisuje `party_id` — nie tworzy nowej karty.
6. „Extract HITL” wysyła temat i treść na kolejkę szkiców. Akceptacja stawki jest na ekstrakcjach, nie tutaj.
7. „Utwórz RFQ” robi zapytanie ofertowe z tej wiadomości. Jedna wiadomość = jedno zapytanie. Kod HS/CN wybierasz z katalogu i „Podpnij HS” — to etykieta ładunku, nie kwota. Numer UN z katalogu towarów niebezpiecznych podpinasz „Podpnij UN” — też etykieta, nie kwota. „Wycena” otwiera `/quotations` z tym RFQ — kwota schodzi ze stawki, nie stąd.

Czego tu nie ma: IMAP, Graph, wysyłka, załącznik jako plik, liczenie kwot, automatyczne składanie wątku z Message-ID.

Nazwy w kodzie: `inbound_message` · `source_ref` · `rfc822_message_id` · `in_reply_to` · status `draft`.
