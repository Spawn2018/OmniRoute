Zaczynam research case studies Qargo TMS — najpierw pobiorę sitemap i stronę z listą case'ów, żeby znaleźć wszystkie URL-e.

I need to research all Qargo TMS customer case studies, so I'll start by checking the sitemap and cases listing page to gather the URLs.

---

Pierwsze dwa adresy nie działają. Próbuję alternatywnych ścieżek.

The sitemap gave a 500 and the cases page 404'd, so I should try alternate paths like the customers page, a resources/cases URL, or the specific wyvern-cargo case study example.

---

Znany case Wyvern Cargo działa — strona listingu jednak nie. Szukam pełnej listy case'ów przez wyszukiwarkę i inne warianty sitemap.

The Wyvern Cargo case study confirms the pattern, but I still need the full list of case studies since the sitemap and /cases/ paths both failed. I'll try alternate URLs without trailing slashes or www, check the sitemap index, search site:qargo.com/cases, and scan the main page navigation for links.

---

Znalazłem już 5 case'ów. Szukam pełnej listy — próbuję innych wariantów sitemap i strony "See all case studies".

I'm gathering more case study links from the site—Moran Logistics, Wyvern Cargo, CS Ellis Logistics, and Premier Refrigerated Trans so far.

---

Sitemap zwraca błąd przez narzędzie fetch — spróbuję pobrać go przez curl i sprawdzę robots.txt.

The sitemap 500 error might be temporary, or the fetch tool just can't handle XML properly—I should try curl via Shell instead, which may work better for XML files, and also check robots.txt to locate the sitemap.

---

Mam pełną listę: **44 unikalne case studies** (wersje EN). Wyvern Cargo już pobrany. Pobieram pozostałe 43 w partiach równoległych.

I've compiled the full list of case studies from Qargo's site, starting to enumerate the unique English case study slugs found under their cases URL path.

I've now got all 44 case study slugs listed out, including one I already fetched in full (Wyvern Cargo). That leaves 43 more to fetch, so I'm planning to batch these fetches in parallel to work through them efficiently.

---

Pobrano 7 z 44. Kontynuuję kolejne partie.

Seven entries done so far. Moving on to the next batch of cases to process: the platform science case study, Ellis Logistics, Dedeygere Frans en Zoon, Deny Logistics, Dhooghe Lifting Transport, Eskatrans, Evolution Connect, and FCE Transport.

There are still 37 more remaining after this batch — including Frank McCarthy Haulage, Freightforce, Hemisphere Freight, Vervoer De Smet, Jacobs Transport, Jan Zijderhand, Joda Freight, Kees Int Veen, Kekkila BVB, Kisjes, Leatrans, L Hunt and Sons, Link Up, Logibrex, Ninatrans, Pass Logistics, PE Express, Premier Logistics, Premier Refrigerated Transport, Road Truck Services, Roffes Transport, Roosenboom, Schiepers Transport, Streamline Shipping, Tyldesley Distribution, Uniserve, Van 't Kruis, Welchs Transport, and Wim Buytaert. I'll keep working through these in batches of six.

---

Wszystkie **44 case studies** pobrane w całości. Kompiluję raport po polsku.

Now that I have all 44 case studies, I'm planning the Polish-language report structure covering each company's profile, pre-Qargo problems, reasons for choosing Qargo, features used, and quantified results with quotes, followed by a synthesis ranking the most-praised features and recurring patterns.

Given the 1500-2500 word limit spans 44 cases, I realize a detailed per-case writeup would be too long, so I'll use a compact markdown table (company/country, segment/size, problems/reasons, features, results) instead, weaving the best quotes into the synthesis section rather than repeating them per case.

Starting to inventory the case data now — beginning with Wyvern Cargo (UK carrier plus pallet network plus warehouse operation), noting their pre-existing system gaps, why they switched, which features they adopted, and the resulting efficiency gains like reduced manual routing time and fewer missed collections.

I'm moving to Alders Bulk Logistics (BE bulk/ADR carrier, 120 vehicles, part of Altrea Group), capturing their need for a unified group TMS, why they chose this SaaS solution, and their fast rollout — under two months with same-day driver training.

Now I'm starting on Altrea Logistics Group itself as the third case.

Anglia Freight - regionalny przewoźnik z siecią paletową Palletline, 50 pojazdów. Wdrożenie wymuszone zapowiedzią zakończenia poprzedniego TMS, przeprowadzono 2500h testów na 5000 przesyłkach w sandboxie. Rezultaty: 6-8% redukcja przebiegu floty (200k mil/rok), 20+ min/pojazd/dzień oszczędności na cross-docku, redukcja nadgodzin o 8h/dzień przy 35k przesyłkach.

Mark Huisman Logistics (Holandia, Weurt) - przewoźnik groupage obsługujący Hiszpanię i Niemcy, 9 własnych aut plus ~30 trucków dziennie. Wcześniej korzystali z przestarzałego TMS bez aktualizacji od 2013, bez API i order splittingu, po 5 latach nieudanych prób budowy własnego systemu. Nowe funkcje obejmują order splitting, Qi order entry z PDF, AI do kontroli faktur zakupowych oraz integracje z Exact Online, Rietveld i Shippeo - efektem jest 95% redukcja czasu fakturowania (z 10h do 30min) i 8h oszczędności administracyjnych tygodniowo, plus około 10 poleconych klientów.

Teraz przechodzę do Moran Logistics (UK) - firmy zajmującej się transportem żywności w kontrolowanej temperaturze, działającej wielodepotowo, która wcześniej zarządzała wszystkim na arkuszach kalkulacyjnych.

przy Qargo nie było żadnych minusów. Funkcje: Exact API, wprowadzanie zamówień Qi, zarządzanie zadaniami, chatbot support. Wyniki: 10h/tydz oszczędności, 50% szybsze wprowadzanie zamówień (3min→1,5min), koniec z 5h piątkami, 4 systemy skonsolidowane w 1. Next: AI planning last-mile.

8. **CS Ellis** (UK, East Midlands) — 3PL (magazyn + transport, Palletline), 60 pojazdów, 170 pracowników, 31k miejsc paletowych, działają od 1933.

Przed Qargo: TMS bez rozwoju od dekady, Excel-style UI, godziny na order entry i invoicing, dostawca po akwizycji zapowiedział shutdown w 12 miesięcy. Wybrali Qargo dla partnerstwa jako early adopter. Funkcje: AI order entry z PDF, integracja Xero, network/subcontracting. Wyniki: order entry z 2h do instant (oszczędność 2-3h/dzień), invoicing -75% (1,5 dnia→0,5 dnia), jedna pracownica przeszła na part-time.

9. **Dedeygere Frans en Zoon** (BE, Pittem) — przewoźnik melasy/pasz, 30 trucków. Wcześniej custom database, ręczne eksporty do Excel, planowanie pen&paper — wybrali Qargo jako jeden program na cały workflow. Funkcje: AI scan dokumentów (waga, data, kierowca), CMR, Falko accounting, Peppol. Wyniki: order entry -25%, invoicing -30%. Next: planowanie w Qargo, digital CMR.

10. Teraz przechodzę do kolejnego case study — Deny Logistics z Belgii, firma 3PL.

Wyniki: +40% obrotu bez wzrostu FTE, 2 kliki zamiast 6-7, fakturowanie 2x szybciej, oszczędność €500/szt na komputerach pokładowych.

12. **Eskatrans** (BE) — kontenery + dywersyfikacja, ~125 trucków (15 na Słowacji). Przed: TMS tylko pod deep-sea, brak integracji księgowej z błędami OCR na PDF, zła struktura danych, diesel surcharge liczony klient po kliencie ręcznie. Dlaczego: COO znał Qargo z poprzedniej firmy, paperless osiągnięty w 2 tygodnie. Funkcje: rate cards ze strefami portowymi, portal dla 160-170 użytkowników.

Teraz opisuję driver app zintegrowany z Transics i AI, które rozpoznaje 60 kontenerów z jednego zdjęcia. Wyniki: fakturowanie skrócone z 2 tygodni do 2 dni (86% szybciej), diesel surcharge liczony w minuty, pełny paperless.

13. Zaczynam opisywać Evolution Connect (UK) — przewoźnik/kurier z flotą 50k...

Przechodzę do FCE Transport (NL), groupage do Europy Wschodniej. Wcześniej firma miała TMS bez driver app, order entry zajmował 3-4 minuty, a faktury czekały na powrót trucków tydzień lub dłużej przy ręcznej kontroli. Trafili przez LinkedIn outreach i byli entuzjastycznie nastawieni od pierwszego spotkania. Nowe funkcje: skanowanie PDF przez Qi, upload CMR w driver app, auto-integracja z Exact, API klienta, portal. Wyniki: -50% admin, order entry skrócony o połowę do 1 minuty, faktury w 1-2 dni, +€1,5M przychodu w 6 miesięcy, polecili 2-3 kolejne firmy.

Następnie Frank McCarthy Haulage (IE) — bulk/construction/kontenery/abnormal, działający od 1977, flota 46 trucks+trailers. Mieli problematyczny TMS, trafili przez demo. Nowe funkcje: scheduling/routing/load w jednym systemie, planowanie oparte na danych, śledzenie w czasie rzeczywistym. Wynik: redukcja pustych mil o 15-20%.

Zaczynam kolejny punkt, szesnasty...

Teraz FreightForce Distribution (UK) — 3PL obejmujący sieć palet (Pallex), groupage, FTL i magazyn, działający od 1998. Wcześniej mieli TMS z ogłoszonym końcem życia, obsługę CSV batch, padające procesy w tle, a budowanie rate card zajmowało tydzień. Trafili przez konsultanta i demo. Nowe funkcje: API Pallex w czasie rzeczywistym, integracja z Sage 50, Samsara, szablony/kopiowanie zleceń. Wyniki: rate cards w godziny zamiast tygodnia, mniej błędów bo system "sprawdza pracę zamiast ją wykonywać", szybsze fakturowanie, a nawet akwizycja drugiej firmy przeszła na Qargo. Plan: konsolidacja obu firm do końca 2026 i program szkoleń z driver app.

Siedemnasty punkt to Hemisphere Freight Services (UK, Ipswich) — globalny forwarder/3PL od 1989, z UK transport dept i 16 pojazdami. Wcześniej ręczne planowanie trwające do 16:00, silosy między działami, ręczne wyceny, i chase za PODs. Ben widział demo trzy lata wcześniej. Nowe funkcje: order entry przez email z Qi, portal z POD i ETA, rate cards LCL, Samsara, API sieci paletowych. Wyniki: -50% czasu planowania (koniec teraz o 13:30), -25% czasu customer service, śledzenie CO2/mileage pod kątem celu net-zero 2035.

Przechodzę do osiemnastego przypadku — Vervoer De Smet (BE), firma budowlana działająca w trybie JIT z flotą 30 ciężarówek.

Qi integracja z komputerem pokładowym, driver app do zdjęć dokumentów. Wyniki: fakturowanie -50% (2 dni→1), dokumenty transportowe <1 min, szybszy onboarding.

21. **Joda Freight** (UK) — haulage+warehousing, 50+ pojazdów, 3 magazyny, pierwszy klient UK. Przed: przestarzałe zarządzanie danymi, ręczne planowanie. Funkcje: auto-ekstrakcja zleceń, portal, drag&drop. Wyniki: zlecenia 15→2 min, 1h/dzień oszczędności planowania, ambasador marki.

22. **Kees in 't Veen** (NL) — płynne towary, 115 trucków, od 1987. Przed: bolt-on TMS z 2008. Dlaczego: LinkedIn, demo order entry (5→2,5 min). Funkcje: PDF reader, forecasted costs, live updates. Wyniki: 50% szybsze zlecenia.

23. **Kekkilä-BVB** (NL/FI) — producent podłoży ogrodniczych, 5 fabryk NL. Przed: custom moduł legacy, wiedza tylko w głowach planistów, onboarding do 2 lat, brak statusów...

Teraz przechodzę do funkcji resource allocation z auto-przydziałem podwykonawców, integracji Qi/D365, Trimble absence planner i Descartes EDI, oraz automatycznego naliczania mileage levy. Wyniki: 200-300 zleceń dziennie na 5 planistów, 90% auto-assign w 3 fabrykach, order entry poniżej minuty, 2x wolumen bez wzrostu zespołu.

24. **Kisjes** (NL) — ładunki nietypowe, 72 pojazdy, od 1904. Przed: TMS zbyt sztywny do re-planningu. Dlaczego: tydzień trialu, jednogłośne głosowanie, shadow running. Funkcje: łączenie zleceń w jeden trip, wizualizacje, POD, CO2 tracking. Wyniki: przełączenie niezauważalne dla klientów.

25. Przechodzę teraz do Leatrans International z Limerick w Irlandii — międzynarodowy import/export z chłodniami i kontenerami, flota 80 trucków i 140 naczep, ponad 30 lat na rynku, wcześniej borykający się z brakiem integracji i ręcznymi procesami.

Dlaczego wybrali: chmura, AI, zero przestoju przy wdrożeniu. Wyniki: przełączenie odczuwalne jak "switch flipped", szybsze fakturowanie, przechwytywanie POD, poprawa morale zespołu. Kolejne kroki: obsługa celna, operatorzy promów, alerty temperaturowe.

26. **L Hunt & Sons** (UK) — haulage/storage/abnormal loads od 1896. Przed: sztywny system, tylko 2 osoby potrafiły go obsługiwać. Funkcje: przeciąganie e-maili do zleceń, aplikacja kierowcy w czasie rzeczywistym, integracja z Webfleet i QuickBooks, portal podwykonawców. Wyniki: oszczędność 15+ godzin tygodniowo, pełna adopcja w kilka dni.

27. **Link-Up** — kurier ekspresowy obsługujący ładunki od 1g do 14t, w tym ADR i zwierzęta. Przed: przestarzały system, wolne fakturowanie, papierowa dokumentacja. Funkcje: panel boczny Outlooka zamieniający e-maile w zlecenia, szablony, tablica planowania z mapą na żywo, cyfrowe CMR, portal klienta. Wyniki: oszczędności czasowe, zero utraty danych przy migracji. Planują pilota WhatsApp i automatyczne cenniki.

28. Teraz zaczynam opisywać Logibrex z Belgii — spedycję bez własnej floty, obsługującą chemię, automotive i branżę spożywczą, działającą od 2013 roku, gdzie poprzedni system służył jedynie do fakturowania.

Dashboard z rentownością (klient/kierowca/truck), szablony, portal self-service, integracje Samsara/Xero, AI skanowanie POD. Wyniki: order entry 5min→30s-2min, oszczędność 9,5h/tydz, support 1 dzień→10 min.

31. **PE Express** (BE) — dystrybucja, 15 pojazdów. Przed: modułowy TMS (wszystko ekstra płatne), nadgodziny, Excel u planistów. Funkcje: portal klienta, AI order entry, route optimisation. Wyniki: -60% błędów fakturowania, wyższy zysk netto na trasę.

32. **Premier Logistics** (UK) — carrier + pallet network Palletforce, 110 pojazdów, 220 pracowników. Przed: TMS 15 lat, cyberatak, Excel równolegle. Dlaczego: LinkedIn, cloud, driver app "revolutionary". Funkcje: integracje Palletforce API, Transforium, Sage 50, Samsara, Outlook AI. Wyniki: 2-3h/dzień oszczędności w planowaniu, 30-45 min/noc komunikaty, 1h/noc POD.

Teraz przechodzę do case study 33 i 34: Premier Refrigerated Transport w Houston (private fleet Monterey Mushrooms, 51 trucków) — najszybsza konwersja dzięki dispatch team wybierającemu Qargo, funkcje Stops view i driver pay module, integracja z JDE i Samsara. Następnie Road Truck Services (IE) — jedyny dostawca z integracją out-of-box z Clarus WMS, redukcja czasu planowania z 5h do 1h, 100% ePOD, certyfikat Green Gold dzięki raportowaniu CO2.

Dalej przyglądam się Roffes Transport (UK, kurtynowe/general haulage) — porzucony poprzedni TMS i app, wdrożenie z polecenia partnera, planowanie skrócone do 11-12, faktury przyspieszone o 24h bez dodatkowych etatów. Roosenboom (NL, od 1992, 6 magazynów) — przejście z Excela przez system pośredni, wybór po 12 demo dzięki nowoczesnemu wyglądowi i czytnikowi PDF zleceń, redukcja czasu zapytań do podwykonawców z pół dnia do 30 minut. I zaczynam Schiepers Transport (BE, 10 trucków) — właściciel po 15 latach pen&paper i Excela, fakturowanie w niedziele, wdrożenie stałych cenników fakturowania.

40. **Uniserve** (UK) — gigant £1,6 mld, 89 spółek, 600 pojazdów. Przed: frustrujące systemy transportowe. Dlaczego: live demo z improwizowanymi scenariuszami, model cenowy revenue-based. Funkcje: OCR drag&drop, API, Samsara.

41. **Van 't Kruis** (NL) — bulk/kontenery, 30 trucków, 4. pokolenie. Przed: serwerowy TMS bez automatyzacji, ręczne skanowanie CMR. Dlaczego: konferencja Utrecht. Funkcje: driver app, POD sync, Exact Online. Wyniki: 100% redukcja skanowania POD/CMR, 5+h/tydz accounting.

42. **Welch's Transport** (UK, Cambridge) — 165 pracowników, 70 pojazdów, Palletline member. Przed: potrzeba centralizacji cloud. Dlaczego: cold call, demo, customizacja. Funkcje: tracking konsygnacji, PDA/driver app, koszty+revenue per job live dashboard, BI. Wyniki: -10% czasu operacyjnego (cel 30%), insighty 2h→<1h.

43. **Wim Buytaert Transport** (BE) — gazy przemysłowe, 10 kierowców, 25+ lat. Przed: paper + Sheets + Zapier, dispatch last-minute, alternatywy drogie. Dlaczego: artykuł, wiara w founderów. Funkcje: paperless, cloud, Trimble, Peppol. Wyniki: 2 miesiące wdrożenie, lepsza auditability, dispatch dzienny.

44. Wyvern Cargo już omówione.

Teraz przechodzę do syntezy — zaczynam od rankingu najczęściej chwalonych funkcji, gdzie AI order entry / Qargo Intelligence wyraźnie dominuje, pojawiając się w około trzydziestu case'ach.

Widzę, że kolejne miejsca zajmują fakturowanie z integracjami księgowymi (redukcje od 30% do 95% czasu w zależności od firmy), driver app z ePOD, portal klienta z redukcjami zapytań rzędu 25-30%, oraz planning board z oszczędnościami czasowymi sięgającymi kilkudziesięciu godzin tygodniowo. Teraz przechodzę do integracji API — sieci paletowe, Transporeon, systemy telematyczne.

Dalej idą tematy automatyzacji (Kekkilä 90% redukcji), dashboardy BI z rentownością per trip, route optimisation dającą 6-20% oszczędności na milach, wsparcie/chatboty z bardzo szybkim czasem odpowiedzi, cloud/SaaS jako czynnik decyzyjny oraz CO2 reporting jako rosnąca potrzeba klientów.

Przechodzę teraz do drugiej części — bolączek rynku TSL: przestarzałe systemy TMS bez rozwoju od dekady, interfejsy w stylu Excela, problem vendor lock-in związany z przejęciami dostawców i zapowiedziami zamknięcia systemów (aż cztery przypadki klientów mówiących, że ich system "umiera").

Notuję dalej ręczne wpisywanie zleceń z maili/PDF-ów, podwójną pracę w Excelu równolegle z TMS, wolne fakturowanie przez papierowe CMR wpływające na cashflow, brak integracji API/EDI i księgowych, papierologię (POD, CMR), wiedzę zamkniętą w głowach planistów wymagającą lat onboardingu, brak widoczności dostaw dla klientów, brak danych do podejmowania decyzji o rentowności, wysokie koszty rozwoju u starych dostawców za dodatkowe moduły oraz wolny support.

Teraz przechodzę do presji na marże i braków kadrowych, gdzie klienci chcą rosnąć bez zwiększania zatrudnienia. Patrzę też na wzorce czasu wdrożeń — od dwóch tygodni do sześciu miesięcy, zazwyczaj 1-2 miesiące, z fazowanym podejściem dla dużych wdrożeń wielolokalizacyjnych, oraz na sandbox jako standardową praktykę testowania przed pełnym wdrożeniem.

Analizuję metody migracji: hard cutover overnight, clean-break z dokańczaniem starych zleceń w starym systemie, parallel running trwający nawet kilka miesięcy oraz fazowane wdrożenia per depot zaczynające się od małych działów i rozszerzające się na tysiące zleceń. Zauważam też, że on-site support podczas go-live to niemal zawsze standard trwający 2-4 dni.

Teraz przyglądam się timingowi wdrożeń — firmy celowo wybierają ciche okresy jak przerwa świąteczna czy początek roku finansowego, choć niektóre wdrożenia (jak PRT) odbywały się tuż przed sezonem szczytowym mimo ryzyka. Dostrzegam też powtarzający się motyw oporu zespołu wobec zmiany.

FreightCE poświęca dedykowaną osobę na 2-3 miesiące wdrożenia, traktując je jako projekt operacyjny, nie IT.

Brakuje jeszcze e-CMR (De Smet czeka), messagingu WhatsApp (Wyvern, Link-Up pilot, Wim Buytaert) w trakcie rolloutu, oraz AI planning/route optimisation jako silnika sugestii (Portex czeka, Kekkilä chce, FCE zachwycone).

Głębszego raportowania/BI (Van Tiel chce revenue per truck bez Excela, Moran BigQuery/PowerBI, PRT dashboardy, Mark Huisman reporting jako kolejny krok), akredytowanego kalkulatora CO2 (Welch's), integracji celnych (Leatrans, Wim Buytaert UK customs), ferry/intermodal (Leatrans), Thermo King (PRT), time window booking przez Transporeon (TDS) — a także onboarding guidance.

Skatrans mówi o elastyczności jako "jeżdżeniu bez GPS", potrzebuje lepszego prowadzenia procesów. Dochodzi konfiguracja Samsara (FreightForce jeszcze dopracowuje), widoczność podwykonawców (Streamline) i głębsze API sieci paletowej (Welch's rebuild). Zbieram też cytaty o oczekiwaniach wobec TMS, zaczynając od słów Michela ten Hove, że system powinien pomagać rosnąć, a nie trzymać w miejscu.

Kolejne cytaty pokazują różne perspektywy — od poszukiwania innowacyjnego partnera (Havermans), przez porównanie technologii do sypialnej kabiny ciężarówki w dalekich trasach (Van Lierde), po kontrolę nad własnym losem dzięki Qargo (Roosenboom), marzenie o bezpapierowym przepływie danych z e-CMR (De Smet), nadzieję na widoczność na poziomie DPD (Gordon), potrzebę dostępnego wszędzie biura w chmurze (Buytaert), aż po stwierdzenie, że to nie tylko automatyzacja, ale całkiem nowy sposób pracy.

Teraz planuję strukturę artykułu — tabela z 44 wierszami dla każdego case study plus sekcje syntezy, celując w 1500-2500 słów łącznie. Przypisuję też kraje poszczególnym firmom: Wielka Brytania obejmuje Wyvern, Anglia, CS Ellis i kilkanaście innych; Belgia obejmuje Alders, Altrea, Eskatrans i pozostałe; Holandia obejmuje Mark Huisman, Portex, Jan Zijderhand i resztę.

I'll fold "dlaczego wybrali" and key functionality into the synthesis, but I should still cover each case individually since the user asked for per-case detail—firm name, context, and outcome.

Given the scope, I'll compromise with a table structured by company (country, segment, scale) alongside prior state/reason for switching, key features, and results, saving the best quotes for the synthesis section to keep things compact while hitting the required fields. Now I'm ready to start drafting the report.

I should output the full report as my final message to the parent agent. Double-checking the Wyvern figures: 75 vehicles, around 100 trailers, and over 130 employees.

Also noting Premier Logistics acquired WT Transport in December 2025, adding 110 vehicles and 220 employees, with go-live set between Christmas and New Year 2023. And for Welch's, 12 out of 32 Palletline members have signed on to Qargo.

Other go-live dates I'm tracking: Eskatrans on September 17 (hard cutover), Kekkilä on September 1 2025, PRT on November 1 2025, Mark Huisman on January 1 2026, Moran's Leeds site going live January 2026 over five working days, and CS Ellis already live since July 2024.

Continuing through the list: Deydeygere in June 2025, Jan Zijderhand mid-June 2025, Pass in January 2025, Link-Up in January 2024, and Anglia likely February 2023 though the year isn't explicitly stated.

Now I've got Joda as the first UK client, live in March 2023. Time to write up the report with these dates.

---

# Raport: Analiza 44 case studies klientów Qargo TMS

Przeanalizowałem komplet case studies opublikowanych na qargo.com (lista z `case-sitemap.xml`; strona listingu `/cases/` bez podstrony zwraca 404, ale wszystkie podstrony działają). Baza klientów: **16× Wielka Brytania, 13× Belgia, 10× Holandia, 3× Irlandia, 1× USA, 1× grupa UK/Norwegia** — rdzeń to przewoźnicy drogowi 10–125 pojazdów oraz 3PL/spedycje, z rosnącą liczbą członków sieci paletowych (Palletline, Palletforce, Pallex).

## Przegląd wszystkich case'ów

| Firma (kraj, segment, skala) | Sytuacja przed / powód zmiany | Podkreślane funkcje | Skwantyfikowane wyniki |
|---|---|---|---|
| **Wyvern Cargo** (UK, przewoźnik + sieć paletowa Palletforce; 75 aut, ~100 naczep, 130 os.) | Legacy TMS bez API (Palletforce: EDI→API), ręczny routing 150–200 palet/dzień, papierowe POD | Auto-routing palet, AI order entry, ePOD w driver app, portal z ETA, bulk invoicing | Zmiana wieczorna kończy 2–3 h wcześniej; −90% ręcznego routingu; −90% nieodebranych awizacji; wzrost bez nowych etatów |
| **Alders Bulk Logistics** (BE, bulk/ADR; 120 aut) | Grupa szukała jednego SaaS TMS | Praca zadaniowa, AI do dokumentów | Wdrożenie w 1 miesiąc; szkolenie biura 1 dzień, kierowcy 10 min |
| **Altrea Logistics Group** (BE, grupa: intermodal, cysterny, bulk; 4 dywizje) | 3 różne TMS-y po akwizycjach; śledzenie tankkontenerów i intermodalu | Moduł network (wymiana zleceń w grupie), planowanie naczep, self-billing podwykonawców | 5 spółek zmigrowanych przed harmonogramem; 2 wdrożenia w czasie planowanym na 1 |
| **Anglia Freight** (UK, przewoźnik regionalny, Palletline; 50 aut) | Dostawca ogłosił koniec TMS | Optymalizacja tras, skanowanie cross-dock, portal | −6–8% przebiegu floty (~200 tys. mil/rok); +20 min/pojazd/dzień; −8 h nadgodzin dziennie |
| **Mark Huisman Logistics** (NL, drobnica/groupage ES-DE; ~30 aut dziennie) | TMS bez aktualizacji od 2013, brak API i dzielenia zleceń; 5 lat nieudanej budowy własnego TMS | Order splitting, Qi (PDF→zlecenie), AI-kontrola faktur zakupowych, Exact/Shippeo | Fakturowanie −95% (10 h/tydz. → 30 min); +8 h/tydz. po integracji Shippeo |
| **Moran Logistics** (UK, chłodnie food, multi-depot) | Całość na arkuszach, telematyka niepołączona z planowaniem | Live-widok stopów na ścianie operacyjnej, wielojęzyczny driver app, Qi auto-tagowanie tras, API klienta, auto-telefony ETA | 0 nieudanych dostaw na go-live; depot Leeds live w 5 dni; adopcja kierowców w 48 h |
| **Portex Logistics** (NL, spedycja multimodalna road/ocean/air/rail) | 4 osobne systemy; 5 h w każdy piątek na ręczny eksport do Exact; błędy OCR | API do Exact, Qi order entry, zarządzanie zadaniami | 10 h/tydz. oszczędności; order entry −50% (3 min → 1,5 min); 4 systemy → 1 |
| **CS Ellis** (UK, 3PL, Palletline; 60 aut, 170 os.) | TMS bez rozwoju od dekady; po akwizycji dostawcy zapowiedź wyłączenia w 12 mies. | AI order entry, Xero, zlecenia dla podwykonawców w platformie | Order entry: 2 h dziennie → niemal natychmiast; fakturowanie −75%; pracownica przeszła na część etatu |
| **Dedeygere Frans en Zoon** (BE, melasa/pasze; 30 aut) | Własna baza danych, planowanie na papierze, ręczne eksporty do Excela | AI-odczyt dokumentów, Peppol, księgowość Falko | Order entry −25%; fakturowanie −30% |
| **Deny Logistics** (BE, 3PL/spedycja chemii i ADR, road/sea/air) | Windows-owy legacy, papierowe teczki morskie, zespoły 2-os. bez zastępowalności | Qi (zlecenia + faktury dostawców), portal klienta zamiast wysyłanych Exceli | Go-live w niecały tydzień; solo-dni bez nadgodzin |
| **D'Hooghe Lifting** (BE, dźwigi/transport) | MS Office: te same dane wpisywane 4×, zlecenia po WhatsApp/telefonie | All-in-one: oferta→plan→faktura, aplikacja mobilna zamiast komputerów pokładowych (500 €/szt.) | +40% obrotu bez proporcjonalnego zatrudnienia; wpis w 2 kliknięcia zamiast 6–7; fakturowanie 2× szybciej |
| **Eskatrans** (BE, kontenery + dywersyfikacja; ~125 aut) | TMS tylko pod deep-sea; faktury przez PDF+OCR z błędami; dopłata paliwowa zmieniana klient po kliencie | Cenniki (strefy portowe), portal, driver app + Transics, AI (odczyt 60 nr. kontenerów z 1 zdjęcia) | Cykl fakturowania 2 tyg. → 2 dni (−86%); zmiana dopłaty paliwowej w minuty; 160–170 użytkowników portalu |
| **Evolution Connect** (UK, kurier/przewoźnik; 50 kierowców) | Stary TMS zmienił model na opłaty per user | Drag&drop z maili, driver app w cenie, Sage | 100 zleceń wprowadzonych w 10 min; awaria w weekend rozwiązana <5 min |
| **FCE Transport** (NL, drobnica Europa Wsch.) | Brak driver app; faktury czekały na fizyczny powrót trucków z CMR | Qi PDF-scan, upload CMR z trasy, auto-księgowanie Exact, portal | −50% administracji; order entry 3–4 min → 1 min; faktury w 1–2 dni zamiast tygodnia; +1,5 mln € przychodu w 6 mies. |
| **Frank McCarthy Haulage** (IE, bulk/budowlanka/kontenery; 46 jednostek) | Niewydolny TMS | Planowanie+routing+load w jednym, decyzje na danych | −15–20% pustych przebiegów |
| **FreightForce Distribution** (UK, 3PL, sieć Pallex) | TMS end-of-life; wymiana danych przez CSV-batche i padające procesy; cennik budowany tydzień | API Pallex real-time, szablony, Samsara, Sage 50 | Cenniki w godziny zamiast tygodnia; „zespół sprawdza pracę zamiast ją wykonywać"; przejęta 2. firma wdrożona na Qargo |
| **Hemisphere Freight** (UK, globalny forwarder/3PL; 16 aut w UK) | Planowanie gotowe o 16:00, silosy, ręczne wyceny | Qi z maili, portal (POD, ETA), cenniki LCL, API sieci paletowych | −50% czasu planowania (koniec o 13:30); −25% czasu obsługi klienta |
| **Vervoer De Smet** (BE, budowlanka JIT; 30 aut, 100 naczep) | TMS z lat 90., sztywny, wadliwa integracja z aplikacją kierowcy | 5 kryteriów: przejrzystość, szybkie zlecenia, driver app, AI + AI-helpdesk, moduły cenowe | Szybszy obieg informacji; czekają na e-CMR |
| **Jacobs Transport** (BE, FTL BE/NL/DE/FR; 95→110 aut) | Nowe funkcje tylko za dopłatą; 1–1,5 h dziennie ręcznej aktualizacji list naczep; słaby Transporeon | Integracja Transporeon (TIAP), jeden widok planowania, portal | ~5 h/tydz. na naczepach; −30% zapytań klientów (~3 h/tydz.) |
| **Jan Zijderhand** (NL, stal: kręgi, blachy; 100+ lat) | Nie-cloudowy system z przestojami; nauka systemu zajmowała rok | Qi w dodatku Outlook, komputer pokładowy, zdjęcia dokumentów z kabiny | Fakturowanie −50% (2 dni → 1); list przewozowy dostępny <1 min — pierwszy raz w historii firmy |
| **Joda Freight** (UK, przewoźnik + magazyny; 50+ aut) | Pierwszy klient UK; archaiczne IT, ręczne planowanie | Auto-ekstrakcja zleceń, portal, drag&drop zmiany tras | Złożone zlecenie 15 min → 2 min; ~1 h dziennie na planowaniu; ambasador Qargo (10+ referencji) |
| **Kees in 't Veen** (NL, przewozy płynne; 115 aut, 300 tankkontenerów) | Bolt-on TMS z 2008 r. | Czytnik PDF w order entry, prognozowane koszty zleceń, live-tracking dla klientów | Order entry 5 min → 2,5 min („crazy fast") |
| **Kekkilä-BVB** (NL, logistyka producenta podłoży; 5 fabryk) | Wiedza planistyczna „w głowach" (wdrożenie planisty do 2 lat), brak statusów | **Resource allocation** (auto-przydział przewoźnika), Qi, integracje D365/Trimble/Descartes, auto-naliczanie holenderskiej opłaty kilometrowej | 200–300 zleceń/dzień na 5 planistów; 90% zleceń przydzielanych automatycznie; order entry 5–10 min → <1 min; 2× wolumen bez wzrostu zespołu |
| **Kisjes** (NL, ładunki nietypowe; 72 pojazdy) | Dobry, ale za mało elastyczny TMS (lokalizacje bez adresów, ciągłe re-planowanie) | Wizualizacje/kolory na planning boardzie, łączenie zleceń wielu klientów w 1 trasę, zdjęcia POD, dane CO₂ | Przełączenie niezauważalne dla klientów (tydzień sandbox + „shadow running") |
| **Leatrans** (IE, międzynarodowy; 80 aut, 140 naczep) | Brak integracji i automatyzacji | Cloud, AI-podsumowania zleceń, POD-capture, driver app | Go-live „jak pstryknięcie przełącznika"; wyraźnie szybsze fakturowanie |
| **L Hunt & Sons** (UK, haulage + ładunki ponadgabarytowe; od 1896) | Sztywny TMS, obsługiwały go tylko 2 osoby, rozwój za dopłatą | Przeciąganie maili → zlecenie (Qi), driver app, Webfleet, QuickBooks, portal podwykonawców | 15+ h/tydz. mniej administracji; 100% adopcji zespołu w kilka dni |
| **Link-Up** (BE, kurier ekspresowy 1 g–14 t, ADR) | Przestarzały system, dopłaty za każdy dodatek, papierowe CMR | Panel Outlook (mail→zlecenie), szablony, planning board + mapa live, portal | Kilka godzin tygodniowo mniej administracji; zero utraty danych przy migracji |
| **Logibrex** (BE, spedycja bez własnej floty) | TMS tylko do fakturowania, brak chmury i EDI | AI order entry, weryfikacja faktur podwykonawców, self-billing, cenniki „ldm vs waga" | Przetwarzanie faktur przychodzących −50%; praca bez papieru |
| **Ninatrans** (BE, time-critical, 7 krajów; chłodnie/FTL/LTL/cysterny/air-RFS) | Custom TMS + Windows-owy system przejętej spółki (środowisko Mac); nieskalowalny | Stałe trasy 1 kliknięciem (2500 z 4000 tripów/mies.), auto-dispatch, cenniki z paliwem i mytem, portal, transfer zleceń między krajami | −30% zapytań o status; 30–60 min dziennie na dispatchu; rentowność na poziomie trasy |
| **Pass Logistics** (UK, multi-dywizyjny; 16 ciągników, 150 zleceń/tydz.) | Legacy bez dostępu www; wsparcie z 1-dniowym oczekiwaniem | Dashboard rentowności (klient/kierowca/truck), portal self-service, AI-odczyt POD, Samsara, Xero | Order entry 5 min → 30 s–2 min (9,5 h/tydz.); wsparcie 1 dzień → maks. 10 min |
| **PE Express** (BE, dystrybucja/express; 15 aut) | Modułowy TMS — wszystko za dopłatą; nadgodziny; Excel u planistów | Portal (klient sam wprowadza zlecenia), AI order entry, optymalizacja tras | −60% błędów fakturowania; wyższy zysk netto na kurs dzięki optymalizacji |
| **Premier Logistics** (UK, Palletforce; 110 aut, 220 os.) | Dostawca TMS przejęty, niedotrzymane obietnice, potem cyberatak; planowanie równolegle w Excelu | API Palletforce (koniec 10–15 plików dziennie), Outlook-AI, portal z 2FA, Sage, Samsara | 2–3 h/dzień na planowaniu; 30–45 min/noc na komunikatach do 50 kierowców; ~10 h/tydz. w księgowości; **+50–60% wzrostu haulage przy 1 nowym etacie** |
| **Premier Refrigerated Transport** (US, flota własna Monterey Mushrooms; 51 trucków, 6,7 mln mil/rok) | Korporacyjny nakaz JD Edwards; przestarzały dispatch; wymóg modułu **driver pay** (stawki za mile/dropy/detention) | Widok „Stops" (jak tablica lotów), driver pay, API JDE + Samsara + Qlik | „Najszybsza i najgładsza z 3 konwersji TMS w karierze"; go-live tuż przed szczytem sezonu |
| **Road Truck Services** (IE, transport+magazyn+cło) | Gubione ePOD-y zagrażały relacjom; planowanie 4–5 h co wieczór | Jedyna integracja out-of-the-box z Clarus WMS; mapa live; wielojęzyczny driver app; raport CO₂ | Planowanie −80% (5 h → 1 h); 100% skutecznych ePOD; **go-live w 2 tygodnie**; utrzymany certyfikat Green Gold |
| **Roffes Transport** (UK, kurtyny, papier/opakowania) | Pierwszy TMS (2023) zawiódł: aplikacja porzucona przez kierowców, POD przetwarzane 3 dni | Drag&drop planning board, multi-scan POD (tylko wyjątki ręcznie), Xero | ~30 h/tydz. na planowaniu (koniec o 11–12 zamiast 15–16); faktury o 24 h szybciej; zero dodatkowych etatów |
| **Roosenboom** (NL/Benelux; 6 magazynów, 20+ aut) | Excel + osobny system administracyjny (dwustopniowo, godziny dziennie) | Czytnik PDF zleceń i faktur zakupowych; masowe zapytania do podwykonawców | Kontrola podwykonawców: pół dnia → 30 min; odpowiedź supportu <10 min |
| **Schiepers Transport** (BE; 10 trucków, właściciel sam w biurze) | 15 lat długopisu i Excela; fakturowanie w niedziele | Fakturowanie ze stałych cenników, rozliczenia godzinowe, obrót per truck | 25 faktur/h zamiast całego popołudnia; „odzyskane niedziele" |
| **Streamline Shipping** (UK/NO, 250 os., 11 oddziałów; haulage/forwarding/DG/wyspy) | 20-letni system; następny TMS został zamknięty; raporty ręczne | 6–7 konfiguracji planning boardów per zespół, **tasks/automatyzacje**, compliance pojazdów w planowaniu | Widoczność całej sieci w jednym systemie; integracje przestały być barierą kosztową |
| **TDS Tyldesley** (UK, pallet-pooling/papier; 100 aut, 140 naczep) | TMS bez integracji z Transporeon → ręczny import, zgubione zlecenia | Integracja Transporeon TIAP | Wyeliminowany „pełny etat na wpisywanie zleceń"; koniec podjazdów po cudze ładunki |
| **Uniserve** (UK, gigant £1,6 mld, 89 spółek, 600 pojazdów) | Frustracja z istniejących systemów transportowych | OCR drag&drop, API, Samsara; model opłat powiązany z obrotem klienta | (Wdrożenie w toku) — cel: widoczność „jak w DPD" |
| **Van 't Kruis** (NL, bulk/kontenery: pasze, stal; 30 aut, 101 lat) | Serwerowy TMS bez importu zleceń i danych; ręczne skanowanie każdego CMR | Driver app (grafik widoczny w niedzielę), sync POD, Exact Online, Qi | −100% skanowania POD/CMR; 5+ h/tydz. w księgowości |
| **Welch's Transport** (UK, Palletline; 70 aut, 165 os.) | Potrzeba jednej chmurowej platformy | Rentowność każdego zlecenia na żywo (pence-per-mile), BI-dashboard, PDA/driver app | −10% czasu operacyjnego dziennie (cel 30%); przygotowanie analiz na spotkanie 2 h → <10 min; z polecenia 6 przewoźników i 12 z 32 członków Palletline |
| **Van Tiel** (NL, port Rotterdam, kontenery/cysterny; 45–50 aut) | Statyczny TMS + stare komputery pokładowe; wsparcie ticketowe trwało dni | Równoczesna wymiana TMS + telematyki (Platform Science); Qi drag&drop | Order entry −30–50%; korekta godzin kierowców −50%; tablety w 45 autach w 3 dni |
| **Wim Buytaert** (BE, gazy kriogeniczne; 10 kierowców) | Papier + samoróbka Google Sheets/Zapier; dispatch na ostatnią chwilę, administracja do nocy | Paperless, chmura, zarządzanie zdalne, Peppol, Trimble | W pełni operacyjni w 2 miesiące; dispatch w ciągu dnia, audytowalność dokumentów |

## SYNTEZA

### 1. Ranking funkcji, które realnie sprzedają ten system

1. **AI-owe wprowadzanie zleceń (Qargo Intelligence: e-mail/PDF → zlecenie)** — wymieniane w ~30 z 44 case'ów i najczęściej kwantyfikowane: od −25% (Dedeygere) przez −50% (Portex, FCE, Kees) po 5 min → 30 s (Pass). To funkcja-haczyk na demach („order entry is crazy fast").
2. **Fakturowanie + integracje księgowe** (Exact, Xero, Sage, QuickBooks, Odoo, Falko, Peppol) — najmocniejsze liczby całego zbioru: −95% (Mark Huisman), 2 tyg. → 2 dni (Eskatrans), −75% (CS Ellis). Argument uderza w cashflow, nie w wygodę.
3. **Aplikacja kierowcy + ePOD** — wielojęzyczność jako wyróżnik (Moran, RTS, Roffes); eliminacja papieru i skanowania (Van 't Kruis −100%); kluczowa dla przyspieszenia faktur (FCE: CMR z kabiny zamiast czekania na powrót auta).
4. **Portal klienta** — mierzalnie tnie telefony „gdzie moja dostawa": −30% zapytań (Ninatrans, Jacobs), −25% czasu obsługi (Hemisphere), 160–170 użytkowników (Eskatrans); u Premier Logistics stał się argumentem sprzedażowym w przetargach.
5. **Planning board (drag&drop, mapa live)** — Roffes ~30 h/tydz., RTS −80%, Hemisphere −50%; dla planistów to pierwszy „efekt wow" na demo.
6. **Integracje API** — sieci paletowe (Palletforce/Palletline/Pallex), Transporeon (TIAP), telematyka (Samsara, Webfleet, Transics, Trimble, Platform Science), ERP (D365, JD Edwards), WMS (Clarus). Dla TDS i Wyvern integracja była *jedynym* powodem zmiany TMS.
7. **Automatyzacje reguł (resource allocation, tasks)** — 90% auto-przydziału (Kekkilä), stałe trasy 1 kliknięciem (Ninatrans); Streamline nazywa „tasks" najpotężniejszą funkcją platformy.
8. **Rentowność i BI na poziomie trasy** — marża widoczna przy planowaniu, nie na koniec miesiąca (Welch's, Pass, Ninatrans, Roffes — dane do decyzji o rozbudowie floty).
9. **Optymalizacja tras** — −6–8% przebiegu floty (Anglia, ~200 tys. mil/rok), −15–20% pustych mil (McCarthy).
10. **Wsparcie i tempo rozwoju produktu** — czat zamiast ticketów: odpowiedzi <10 min (Roosenboom, Pass) vs dni u starych dostawców; wielu klientów kupuje „partnera, nie software".
11. Wątki wschodzące: **raportowanie CO₂** (RTS utrzymał certyfikat Green Gold; Kisjes, Hemisphere) i **model cenowy** (abonament bez 50 tys. € wdrożenia — Mark Huisman; opłata od obrotu — Uniserve).

### 2. Powtarzające się bolączki rynku TSL

- **Umierające legacy TMS-y**: brak rozwoju od dekady, interfejs „jak Excel z 1996", a w aż 4 przypadkach dostawca ogłosił koniec systemu (Anglia, CS Ellis, FreightForce, Streamline); do tego akwizycje dostawców, podwyżki per-user i cyberatak (Premier). Zmiana TMS bywa wymuszona, nie wybrana.
- **Podwójne/wielokrotne wpisywanie**: te same dane 4× (D'Hooghe), Excel równolegle z TMS (Premier, PE Express), całe planowanie w arkuszach (Moran) lub na papierze (Dedeygere, Schiepers, Roffes do 2023).
- **Fakturowanie jako wąskie gardło cashflow**: czekanie na papierowe CMR z trucków, wielodniowe przetwarzanie POD.
- **Brak API w starym świecie**: przejście sieci paletowych z EDI na API, CSV-batche, ręczne przenoszenie zleceń z Transporeon, faktury przez PDF+OCR.
- **Wiedza w głowach ludzi**: wdrożenie planisty do 2 lat (Kekkilä), klienci „w głowie właściciela" (D'Hooghe), zespoły 2-osobowe bez zastępowalności (Deny).
- **Ślepota na marżę**: brak rentowności per trasa/pojazd — przy obecnych cenach paliwa to „absolutna konieczność" (Schiepers).
- **Ekonomia dodatków**: każdy moduł i rozwój za dopłatą (PE Express, L Hunt, Jacobs — AI „za extra"), komputery pokładowe po 500 €/szt.
- Tło rynkowe: kurczące się marże, trudność zatrudnienia i przerzucanie obowiązków przez spedytorów/armatorów na przewoźnika (Eskatrans) — stąd naczelny motyw wszystkich case'ów: **„rosnąć bez zatrudniania"** (Premier: +50–60% przy 1 etacie; Kekkilä: 2× wolumen tym samym zespołem).

### 3. Wzorce wdrożeń

- **Czas**: od 2 tygodni (RTS — sytuacja awaryjna) i miesiąca (Alders), przez typowe 2–5 miesięcy, po fazowane wdrożenia wielodepotowe (Moran, Altrea — miesiącami, depot po depocie). Depot Leeds u Morana: pełne go-live w 5 dni roboczych.
- **Sandbox jako rytuał**: niemal każdy case — od rekordowych 2500 h testów na 5000 próbnych przesyłkach (Anglia) po radę Streamline: „przetestuj pełną drogę jednego zlecenia przez jeden dzień". U Jana Zijderhanda dostępność sandboxa była wprost kryterium wyboru dostawcy.
- **Trzy strategie migracji**: (a) twarde przecięcie „overnight" (Alders, Eskatrans, Pass — stary system wyłączony w dniu startu), (b) czysty podział — stare zlecenia dokańczane w starym systemie (Deny), (c) równoległa praca dwóch systemów tygodniami (Evolution — 3 miesiące, Hemisphere, PRT, „shadow running" u Kisjes). Terminy wybierane w martwe okresy: między świętami (Premier, Welch's), 1 stycznia = nowy rok finansowy (Mark Huisman); wyjątkiem PRT — świadome go-live tuż przed szczytem sezonu.
- **Onboarding na miejscu jako standard**: 2–4 dni obecności zespołu Qargo przy starcie, w tym praca zmianowa dzień/noc (Moran) i dostępność przez weekend (PRT). To najczęściej chwalony element całej relacji.
- **Opór zespołu**: bariera jest u właścicieli/starszego pokolenia (rodzice De Smeta; ojciec u Welch's nazwał syna „wariatem") i u długoletnich planistów — łamana taktyką „replicate first, innovate later" (CS Ellis) i pokazaniem konkretu (Premier: start 50 kierowców jednym kliknięciem). **Kierowcy adoptują najszybciej**: 10 min szkolenia (Alders), 48 h (Moran), pełna flota od 1. dnia (Roffes). Warunek sukcesu: wewnętrzny champion — dedykowana osoba ucząca się systemu (FCE oddelegowało pracownika na 2–3 miesiące; rada Mark Huisman: „zdobądź tę osobę — to robi całą różnicę").
- Ciekawy mechanizm sprzedaży: **klienci-ambasadorzy** (Joda, Welch's — 12/32 członków Palletline, FCE, Mark Huisman ~10 poleconych) — sieci paletowe działają jak kanał wirusowy.

### 4. Czego klientom nadal brakuje / obietnice na przyszłość

- **e-CMR** — wprost wyczekiwany (De Smet: „paperless dataflow dałby nam przewagę — to byłby ideał").
- **Komunikacja WhatsApp** w platformie i driver app — w rolloucie (Wyvern „zespół nie może się doczekać", pilot u Link-Up, plan u Wim Buytaert).
- **AI-planowanie / optymalizacja jako silnik sugestii** — najczęstsze „next": Portex (międzynarodowy last-mile), Kekkilä (specjalistyczny sprzęt), FCE.
- **Głębsze raportowanie i BI** — Van Tiel chce tygodniowych widoków przychód/koszt per truck „bez odbudowywania wszystkiego w Excelu"; Moran sięga po BigQuery/Power BI; Welch's czeka na akredytowany kalkulator CO₂.
- **Integracje branżowe w kolejce**: cło/customs (Leatrans, Wim Buytaert), operatorzy promowi, monitoring temperatury Thermo King (PRT), rezerwacja okien czasowych w Transporeon (TDS), pełniejsze API sieci paletowych (Welch's), widoczność podwykonawców (Streamline), dopracowanie konfiguracji Samsara (FreightForce).
- **Cień elastyczności**: Eskatrans nazywa swobodę konfiguracji „jazdą bez GPS" — bez dyscypliny procesów każdy użytkownik znajduje własną, niekoniecznie dobrą ścieżkę. To najbardziej szczera krytyka w całym zbiorze — poza nią case'y (z natury marketingowe) przemilczają porażki; jedyne przyznane trudności to integracje księgowe (QuickBooks u L Hunt), pierwsze wdrożenie Pallex (FreightForce) i mapowanie EDI (Kekkilä).

**Cytaty-syntezy oczekiwań wobec TMS:** „System ma pomagać ci rosnąć, a nie trzymać cię w miejscu" (FCE); „Nie wysłałbyś dziś kierowcy w trasę międzynarodową autem bez sypialni — ta sama logika dotyczy technologii" (Eskatrans); „Szukaliśmy nowoczesnej technologii, ale przede wszystkim innowacyjnego partnera, który myśli razem z nami" (Altrea); „Qargo znaczy, że pozostajemy panami własnego losu" (Roosenboom); „Zmiana TMS to zmiana wszystkiego — nie sama automatyzacja, ale nowy sposób pracy. Ale gdy ludzie się zaadaptują, jest lepiej pod każdym względem" (Wyvern).

---

## Źródła (44 case studies, qargo.com)

1. https://www.qargo.com/cases/wyvern-cargo/ · 2. https://www.qargo.com/cases/alders-bulk-logistics/ · 3. https://www.qargo.com/cases/altrea-logistics-group/ · 4. https://www.qargo.com/cases/anglia-freight/ · 5. https://www.qargo.com/cases/case-study-mark-huisman/ · 6. https://www.qargo.com/cases/case-study-moran-logistics/ · 7. https://www.qargo.com/cases/case-study-portex-logistics/ · 8. https://www.qargo.com/cases/case-study-van-tiel-platform-science/ · 9. https://www.qargo.com/cases/cs-ellis-logistics/ · 10. https://www.qargo.com/cases/dedeygere-frans-en-zoon/ · 11. https://www.qargo.com/cases/deny-logistics/ · 12. https://www.qargo.com/cases/dhooghe-lifting-transport/ · 13. https://www.qargo.com/cases/eskatrans/ · 14. https://www.qargo.com/cases/evolution-connect/ · 15. https://www.qargo.com/cases/fce-transport-b-v/ · 16. https://www.qargo.com/cases/frank-mccarthy-haulage/ · 17. https://www.qargo.com/cases/freightforce-distribution/ · 18. https://www.qargo.com/cases/hemisphere-freight-services/ · 19. https://www.qargo.com/cases/how-vervoer-de-smet-achieved-x/ · 20. https://www.qargo.com/cases/jacobs-transport-warehousing/ · 21. https://www.qargo.com/cases/jan-zijderhand/ · 22. https://www.qargo.com/cases/joda-freight/ · 23. https://www.qargo.com/cases/kees-int-veen/ · 24. https://www.qargo.com/cases/kekkila-bvb/ · 25. https://www.qargo.com/cases/kisjes/ · 26. https://www.qargo.com/cases/leatrans-international/ · 27. https://www.qargo.com/cases/l-hunt-and-sons/ · 28. https://www.qargo.com/cases/link-up/ · 29. https://www.qargo.com/cases/logibrex/ · 30. https://www.qargo.com/cases/ninatrans-case-study-unified-transport-operations-with-qargo-tms/ · 31. https://www.qargo.com/cases/pass-logistics/ · 32. https://www.qargo.com/cases/pe-express/ · 33. https://www.qargo.com/cases/premier-logistics/ · 34. https://www.qargo.com/cases/premier-refrigerated-transport-qargo-case-study/ · 35. https://www.qargo.com/cases/road-truck-services/ · 36. https://www.qargo.com/cases/roffes-transport/ · 37. https://www.qargo.com/cases/roosenboom/ · 38. https://www.qargo.com/cases/schiepers-transport/ · 39. https://www.qargo.com/cases/streamline-shipping-group/ · 40. https://www.qargo.com/cases/tyldesley-distribution-services-transport/ · 41. https://www.qargo.com/cases/uniserve/ · 42. https://www.qargo.com/cases/van-t-kruis/ · 43. https://www.qargo.com/cases/welchs-transport/ · 44. https://www.qargo.com/cases/wim-buytaert-qargo-case-study/

Lista pozyskana z https://www.qargo.com/case-sitemap.xml (sitemap index: https://www.qargo.com/sitemap_index.xml); strona główna https://www.qargo.com/ posłużyła do kontekstu produktowego.

Now I'll write the complete report in Polish, aiming for 1500-2500 words with a source list included.

---

Raport gotowy powyżej — obejmuje wszystkie 44 case studies Qargo (16 UK, 13 BE, 10 NL, 3 IE, 1 US, 1 UK/NO), tabelę per-case z problemami, funkcjami i skwantyfikowanymi wynikami, czteropunktową syntezę (ranking funkcji, bolączki rynku TSL, wzorce wdrożeń, braki/roadmapa) oraz pełną listę źródeł URL.