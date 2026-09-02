# Katalogi zapisu

Wpisujesz rekord z pochodzeniem. Nie ma luźnego stringa zamiast kodu. Kwota to Decimal z walutą. Model językowy tych ekranów nie obsługuje.

Ekrany, które **zapisują** (INSERT/upsert), nie tablice-odczyty:

- kody opłat, kody HS/CN, numery UN, sieci — kod / nazwa / aliasy
- stawki kupna — niemutowalne, `source_ref`; zmiana = nowy wiersz
- opłaty — kupno i sprzedaż na jednym wierszu; marża z pary, nie z arkusza
- kurs NBP, extra portowe, oferty kanału — katalog, nie live HTTP
- porty, strefy taryfowe, terminale — UN/LOCODE / zakres pocztowy / ISPS
- ustawienie `default_currency` — allowlista, nie sekret
- SOP klienta — treść + akceptacja procedury, nie generator zadań

Czego tu nie ma: 70 osobnych instrukcji na pulpity odczytu (zlecenie, tracking, FV). Ścieżka extract → stawka → opłata → wycena jest w [ścieżka-pieniędzy.md](ścieżka-pieniędzy.md). Kontrahent: [kontrahent.md](kontrahent.md).

Nie licz w przeglądarce. Nie wklejaj kursu NBP w kwotę oferty.
