# Katalogi zapisu

Wpisujesz rekord z pochodzeniem. Nie ma luźnego stringa zamiast kodu. Kwota to Decimal z walutą. Model językowy tych ekranów nie obsługuje.

Ekrany, które **zapisują** (INSERT/upsert), nie tablice-odczyty:

- kody opłat, kody HS/CN, numery UN, sieci — kod / nazwa / aliasy
- stawki kupna — niemutowalne, `source_ref`; zmiana = nowy wiersz
- opłaty — kupno i sprzedaż na jednym wierszu; marża z pary, nie z arkusza
- kurs NBP, extra portowe, oferty kanału — katalog, nie live HTTP. Na extra portowych „Dopasuj warunek” pokazuje wiersze, których `applies_when` jest dokładnie taki jak wpisałeś. To nie dopisuje opłaty ani marży.
- porty, strefy taryfowe, terminale — UN/LOCODE / zakres pocztowy / ISPS
- ustawienie `default_currency`, `quotation_number_prefix`, `quotation_print_template` — allowlista, nie sekret, nie licznik oferty
- SOP klienta — treść + akceptacja procedury. Checkbox „Blokuj auto” zabrania automatu; świadomy `mailto:` i tak wymaga kliknięcia. Nie generator zadań.
- poczta `/mail` — `inbound_message` z `fixture://` / `synth://` albo ingest `graph://` / `imap://` + `external_id` (ten sam id = ten sam wiersz). Nie live skrzynka. Nie send.
- outbox `/outbox` — zdarzenie `inbound_message_saved` po zapisie wiadomości. Ten sam subject = ten sam wiersz. Nie Temporal. Nie dispatch.
- decyzje `/decisions` — pending na `subject_id`; Akceptuj albo Odrzuć z `lock_version`. Dwa okna, dwa Akceptuj: drugi dostaje konflikt. Nie accept extractu. Nie send.
- powiadomienia `/notifications` — zapisany inbox `unread`/`read` z `source_ref`. Tablica pending HITL/wycen zostaje odczytem. Nie send.
- szkic maila `/ai` — `mail_draft` obok extractu. Werdykt na `/decisions`. Po Akceptuj: „Wyślij w kliencie” zapisuje `sent` i daje `mailto:`. SOP `blocks_auto` nie blokuje tego kliknięcia. Nie czat. Nie Graph HTTP. Nie accept extractu.

Czego tu nie ma: 70 osobnych instrukcji na pulpity odczytu (zlecenie, tracking, FV). Ścieżka extract → stawka → opłata → wycena jest w [ścieżka-pieniędzy.md](ścieżka-pieniędzy.md). Kontrahent: [kontrahent.md](kontrahent.md).

Nie licz w przeglądarce. Nie wklejaj kursu NBP w kwotę oferty.
