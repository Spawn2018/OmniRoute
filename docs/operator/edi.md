# Komunikat EDI

Dopasowanie oferty kanału do lane wyceny to jeszcze nie komunikat. Wiersz powstaje, gdy go **zapiszesz** na `/edi`, na konkretnym zleceniu (jest kontrahent).

1. Najpierw zapisz zlecenie na `/shipments`.
2. Wejdź na EDI. Wklej `shipment_id`, rodzaj (`noted`, `outbound` albo `other`) i `source_ref` (`fixture://edi-message/…` albo `tenant:manual`).
3. „Zapisz komunikat” wstawia wiersz. System nic nie parsuje i nic nie wysyła.

Czego tu nie ma: parser, treść komunikatu, live HTTP, auto-wiersz z oferty kanału, kwota na tym wierszu.

Nazwy w kodzie: `edi_message` · `message_kind` · `source_ref`.
