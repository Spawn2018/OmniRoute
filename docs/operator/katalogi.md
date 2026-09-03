# Katalogi zapisu

Wpisujesz rekord z pochodzeniem. Nie ma luźnego stringa zamiast kodu. Kwota to Decimal z walutą. Model językowy tych ekranów nie obsługuje.

Ekrany, które **zapisują** (INSERT/upsert), nie tablice-odczyty:

- kody opłat, kody HS/CN, numery UN, sieci — kod / nazwa / aliasy
- stawki kupna — niemutowalne, `source_ref`; zmiana = nowy wiersz
- opłaty — kupno i sprzedaż na jednym wierszu; marża z pary, nie z arkusza
- kurs NBP, extra portowe, oferty kanału — katalog, nie live HTTP. Na extra portowych „Dopasuj warunek” pokazuje wiersze, których `applies_when` jest dokładnie taki jak wpisałeś. To nie dopisuje opłaty ani marży.
- porty, strefy taryfowe, terminale — UN/LOCODE / zakres pocztowy / ISPS
- sieci `/networks` — katalog sieci oraz ręczny członek (`member_code` + nazwa) w wybranej sieci. „Zapisz zapytanie” dopisuje `carrier_inquiry` do wybranego członka (status `draft`, bez kwoty). Nie portal. Nie live HTTP. Nie dopasowanie do kontrahenta.
- ustawienie `default_currency`, `quotation_number_prefix`, `quotation_print_template` — allowlista, nie sekret, nie licznik oferty
- SOP klienta — treść + akceptacja procedury. Checkbox „Blokuj auto” zabrania automatu; świadomy `mailto:` i tak wymaga kliknięcia. Nie generator zadań.
- poczta `/mail` — `inbound_message` z `fixture://` / `synth://` albo ingest `graph://` / `imap://` + `external_id` (ten sam id = ten sam wiersz). Nie live skrzynka. Nie send.
- outbox `/outbox` — zdarzenie `inbound_message_saved` po zapisie wiadomości. Ten sam subject = ten sam wiersz. Nie Temporal. Nie dispatch.
- zlecenie `/shipments` — zapis `shipment` z wyceny z kontrahentem. How-to: [zlecenie.md](zlecenie.md). Nie tracking. Nie kwota na tym wierszu.
- tracking `/tracking` — zapis `tracking_event` na zleceniu. How-to: [tracking.md](tracking.md). Nie mapa. Nie AIS. Czas podaje operator.
- dokumenty `/shipment-documents` — zapis `shipment_document` na zleceniu. How-to: [dokument-zlecenia.md](dokument-zlecenia.md). Nie bajty. Nie wydruk. Skan zostaje na ekstrakcji.
- wyjątki `/exceptions` — zapis `operational_exception` na zleceniu. How-to: [wyjatek.md](wyjatek.md). Nie mapa. Nie filtr wycen bez POL/POD.
- EDI `/edi` — zapis `edi_message` na zleceniu. How-to: [edi.md](edi.md). Nie parser. Nie live HTTP. Oferta kanału zostaje na `/channel-quotes`.
- faktury `/invoices` — zapis `sales_invoice` na zleceniu i numer sesji (`ksef_ref`). How-to: [faktura.md](faktura.md). Nie live HTTP. Nie kwota na tym wierszu. Sprzedaż zostaje na `/charges`.
- wieża `/watchtower` — lista wyjątków + pending S11 (Akceptuj/Odrzuć). How-to: [wieza.md](wieza.md). HITL na `/ai`. Leniwy panel mapy, nie kafelki.
- decyzje `/decisions` — pending na `subject_id`; Akceptuj albo Odrzuć z `lock_version`. Dwa okna, dwa Akceptuj: drugi dostaje konflikt. Nie accept extractu. Nie send.
- powiadomienia `/notifications` — zapisany inbox `unread`/`read` z `source_ref`. Tablica pending HITL/wycen zostaje odczytem. Nie send.
- szkic maila `/ai` — `mail_draft` obok extractu. Werdykt na `/decisions`. Po Akceptuj: „Wyślij w kliencie” zapisuje `sent` i daje `mailto:`. SOP `blocks_auto` nie blokuje tego kliknięcia. Nie czat. Nie Graph HTTP. Nie accept extractu.

Czego tu nie ma: 70 osobnych instrukcji na pulpity odczytu. Zlecenie: [zlecenie.md](zlecenie.md). Tracking: [tracking.md](tracking.md). Dokument: [dokument-zlecenia.md](dokument-zlecenia.md). Wyjątek: [wyjatek.md](wyjatek.md). Wieża: [wieza.md](wieza.md). EDI: [edi.md](edi.md). Faktura: [faktura.md](faktura.md). Ścieżka extract → stawka → opłata → wycena jest w [ścieżka-pieniędzy.md](ścieżka-pieniędzy.md). Kontrahent: [kontrahent.md](kontrahent.md).

Nie licz w przeglądarce. Nie wklejaj kursu NBP w kwotę oferty.
