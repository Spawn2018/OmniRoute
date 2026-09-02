# Poczta — wiadomość fixture

Na `/mail` zapisujesz wiadomość przychodzącą ręcznie, jak w teście. To nie jest skrzynka z sieci.

1. Wejdź na Poczta. Góra ekranu to lista `inbound_message`, dół to znane adresy kontrahenta.
2. W `source_ref` zostaw pin `fixture://inbound-mail/…` albo `synth://…`. Adres IMAP albo Graph nie przejdzie.
3. Wpisz nadawcę, temat i treść. Status zawsze `draft` — serwer go ustawia, nie Ty.
4. Zapisz. Wiersz należy do Twojej firmy. Inny tenant go nie zobaczy.
5. Znane domeny i kontakty niżej to odczyt karty kontrahenta. `resolve_email` nie dopina jeszcze tej wiadomości do `party` (to następny krok).

Czego tu nie ma: IMAP, Graph, wysyłka, załącznik jako plik, extract z treści, `party_id` na wierszu.

Nazwy w kodzie: `inbound_message` · `source_ref` · status `draft`.
