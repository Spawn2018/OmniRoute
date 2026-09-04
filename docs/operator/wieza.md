# Wieża

Wieża składa już istniejące joby na jednym ekranie `/watchtower`. Nie ma nowej tabeli.

1. Lista wyjątków to te same wiersze co na `/exceptions`. Zapisu wyjątku tu nie ma — idź na wyjątki.
2. Pending S11 to decyzje ze statusem `pending`. Akceptuj albo Odrzuć woła to samo API co `/decisions`, z `lock_version`. Dwa okna, dwa kliknięcia: drugi dostaje konflikt.
3. HITL extract zostaje na `/ai`. Wieża tylko linkuje, nie robi drugiego extractu.
4. Panel mapy ładuje się dopiero po kliknięciu. W paczce początkowej go nie ma. Nie ma AIS.
5. Na górze tablicy stoją trzy liczniki z tych samych list: wyjątki, pending S11, szkice. To nie jest mapa.
6. Szkice maila to te same wiersze co na `/ai`. Zapisu szkicu tu nie ma — idź na `/ai`.

Czego tu nie ma: nowy moduł, leaflet, czas przybycia liczony, live AIS, drugi silnik decyzji, czat.

Nazwy w kodzie: `watchtower` · `operational_exception` · `operator_decision` · `mail_draft`.
