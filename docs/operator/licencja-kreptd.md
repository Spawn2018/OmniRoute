# Licencja KREPTD

Na `/kreptd-licences` zapisujesz **numer licencji KREPTD/GITD** przy istniejącym kontrahencie. To nie pobranie z kreptd.gitd.gov.pl i nie Citizen API.

1. Wejdź na Licencja KREPTD. Wklej `party_id` kontrahenta tenanta.
2. Wpisz numer licencji (8–64 znaki, musi zawierać cyfrę). Nie wklejaj URL.
3. „Zapisz licencję KREPTD” z `source_ref` (`fixture://kreptd-licence/…` albo `tenant:manual`).

Czego tu nie ma: scrape HTML, Citizen API, certyfikat, kolumny na `party`, `party_document`, scoring osoby, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Kontrahent zostaje na `/parties`. Dokumenty C8 zostają leftover.

Nazwy w kodzie: `kreptd_licence` · `party_id` · `licence_no` · `source_ref`.
