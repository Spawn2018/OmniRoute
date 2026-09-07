# Adapter ERP / FK — instrukcja administratora

OmniRoute **wystawia** faktury (KSeF wychodzi z Omni). Do księgowości idą dwa strumienie: **przychodowe** (sprzedaż do klienta) i **kosztowe** (zakup od przewoźnika/dostawcy). ERP ich nie wystawia od nowa — księguje to, co dostanie. Marży nie liczy ERP i nie liczy model.

Nie włączaj wysyłki KSeF w Comarchu / Symfonii / Subiekcie dla tych samych numerów.

## Comarch ERP Optima

1. W Optimie sprawdź wersję (Standard/Premium) i czy partner Comarch sprzedał **licencję na API / dostęp integracyjny**.
2. Typowe środowisko: Windows + baza Optimy. Instalujemy **agenta Omni** na tym samym hoście (lub z dostępem COM do Optimy).
3. W Omni: Ustawienia organizacji → Integracje → Comarch Optima → adres agenta + dane operatora API (szyfrowane).
4. Mapowanie: seria FV **przychodowej** Omni → FS/sprzedaż w Optimie; seria FV **kosztowej** → FZ/zakup. Konta dekretu — pierwsza synchronizacja z potwierdzeniem księgowego.
5. Dokumentacja producenta: portal Comarch / partner. Nie ma jednego publicznego swaggera „dla wszystkich”.

## Comarch ERP XL

1. XL rozmawia natywnie przez **CDN API** (komponenty na serwerze XL), nie przez jeden oficjalny REST.
2. Agent Omni stoi przy serwerze XL (ciągły host; wyłączanie na noc psuje sync).
3. REST „do XL” u integratorów to nakładka na CDN — my wołamy CDN/SOAP, nie cudze API sklepu.
4. Licencja integracji: TO_VERIFY u partnera Comarch przed wdrożeniem.

## Symfonia (Sage / Cegid)

1. Włącz **WebAPI** w instalacji Symfonii (moduł / usługa na porcie, domyślnie często 8080 w LAN).
2. W panelu Symfonii utwórz **klucz aplikacji**.
3. Test: `GET /api/Ping` na hoście WebAPI.
4. Sesja: `GET /api/Sessions/OpenNewSession?deviceName=OmniRoute` z nagłówkiem `Authorization: Application {klucz}`, potem `Authorization: Session {guid}`.
5. Docs: [pomoc.symfonia.pl — WebAPI 2026, uwierzytelnianie](https://pomoc.symfonia.pl/data/api/webapi/2026/data/uwierzytelnianie_i_autoryzacja.htm).
6. W Omni wklej URL WebAPI + klucz. Jeśli Symfonia jest tylko w biurze — agent albo tunel, nie exposujemy SQL.

## Subiekt nexo (InsERT)

1. Potrzebna **Sfera**: w nexo PRO jest, w zwykłym nexo — dokupić.
2. Subiekt siedzi na **lokalnym SQL Server**. Agent Omni instalujesz obok, woła Sferę lokalnie, do chmury Omni idzie tylko szyfrowany outbound.
3. W Omni: typ bazy (nexo), firma, operator Sfery.
4. Mapuj dwie serie: FV przychodowa Omni → FS; FV kosztowa Omni → FZ (zakup). ZK/WZ tylko jeśli tenant chce też dokument magazynowy — nie zamiast faktury.

## Subiekt GT

1. Dokup **„Sfera dla Subiekta GT”** (osobny dodatek).
2. Reszta jak nexo: agent przy stanowisku/serwerze GT. To **inny** adapter niż nexo — nie mieszaj wersji.

## Inne (kolejka po P0)

- **enova365** — moduł WebAPI, REST + JWT, Swagger na instancji (`enova.pl` / dokumentacja Soneta).
- **WAPRO** Mag/Fakir — WebAPI integrator (Asseco), REST, nie dawaj loginu do MSSQL.
- SAP Business One Service Layer, Business Central OData — HZ.

## Połączenie w OmniRoute

1. Ustawienia organizacji → Integracje → ERP.
2. Wybierz system → wklej URL / zainstaluj agenta → test „ping”.
3. Mapowanie serii i kont — zatwierdza księgowy (HITL).
4. Włącz sync: po wystawieniu FV przychodowej (po KSeF) **oraz** po zatwierdzeniu FV kosztowej — dwa kolejki dokumentów, dwie serie w FK.
5. Rotacja haseł u operatora ERP → nowy sekret w Omni; stary unieważnij.

Nie wklejaj haseł SQL `sa` do Omni. Nie otwieraj portu 1433 na świat.
