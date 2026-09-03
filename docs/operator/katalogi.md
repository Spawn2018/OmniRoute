# Katalogi zapisu

Wpisujesz rekord z pochodzeniem. Nie ma luźnego stringa zamiast kodu. Kwota to Decimal z walutą. Model językowy tych ekranów nie obsługuje.

Ekrany, które **zapisują** (INSERT/upsert), nie tablice-odczyty:

- kody opłat, kody HS/CN, numery UN, sieci — kod / nazwa / aliasy
- stawki kupna — niemutowalne, `source_ref`; zmiana = nowy wiersz
- opłaty — kupno i sprzedaż na jednym wierszu; marża z pary, nie z arkusza
- kurs NBP, extra portowe, oferty kanału — katalog, nie live HTTP. Na extra portowych „Dopasuj warunek” pokazuje wiersze, których `applies_when` jest dokładnie taki jak wpisałeś. To nie dopisuje opłaty ani marży.
- porty, strefy taryfowe, terminale — UN/LOCODE / zakres pocztowy / ISPS
- ustawienie `default_currency`, `quotation_number_prefix`, `quotation_print_template` — allowlista, nie sekret, nie licznik oferty
- SOP klienta — treść + akceptacja procedury. Checkbox „Blokuj auto” mówi, że zatwierdzona procedura zabrania automatu (wysyłka przyjdzie później). Nie generator zadań.
- poczta `/mail` — `inbound_message` z `fixture://` albo `synth://`; status `draft`; nie IMAP
- decyzje `/decisions` — pending na `subject_id`; Akceptuj albo Odrzuć z `lock_version`. Dwa okna, dwa Akceptuj: drugi dostaje konflikt. Nie accept extractu. Nie send.
- powiadomienia `/notifications` — zapisany inbox `unread`/`read` z `source_ref`. Tablica pending HITL/wycen zostaje odczytem. Nie send.
- szkic maila `/ai` — `mail_draft` obok extractu, status `draft`. Werdykt na `/decisions`. Nie czat. Nie send. Nie accept extractu.

Czego tu nie ma: 70 osobnych instrukcji na pulpity odczytu (zlecenie, tracking, FV). Ścieżka extract → stawka → opłata → wycena jest w [ścieżka-pieniędzy.md](ścieżka-pieniędzy.md). Kontrahent: [kontrahent.md](kontrahent.md).

Nie licz w przeglądarce. Nie wklejaj kursu NBP w kwotę oferty.
