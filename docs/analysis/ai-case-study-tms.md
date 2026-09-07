# Audyt case studies AI w TMS / spedycji (2024–2026)

**Data:** 2026-09-07. **Język:** polski. **Postawa:** sceptyczna.
**Zakres:** gdzie vendor deklaruje oszczędność czasu i czy da się to zmierzyć (przed/po, N, metoda), czy to slogan.
**Nie jest to plaster.** Nie zmienia `CURRENT.md` ani `PLAN-REALIZACJA.md`.

## Werdykt w jednym akapicie

Liczby, które da się obronić, dotyczą **wąskiego jobu** (order entry z PDF/maila, cykl POD→faktura, matching dokumentu, ETA w oknie ±2 h) i prawie zawsze mieszają AI z wymianą TMS, ePOD, portalem i integracją FK. Hasło **„−75% adminu”** (Qargo), **„do 95% mniej czasu na zlecenie”** (Alpega landing), **„AI w iSPEED”** (interLAN) i **„GenAI w Infios TM”** (dawny MercuryGate) **nie mają metodologii publicznej**. Najlepszy pomiar w zbiorze to **A/B Transporeon × Anheuser-Busch (45 dni)** oraz **project44 ETA (+28 pp, 500+ FTL, zdefiniowane okno)**. Żaden publiczny case nie uzasadnia auto-charge, auto-linku FV, GAN na skanie ani auto-scoringu kredytowego.

## Metoda audytu

1. Vendor case / landing / PR / Forrester TEI / Gartner MQ (cytaty publiczne) / McKinsey (tylko z URL).
2. Lokalne kompilacje: 44 case’y Qargo, 59 newsów, dossier SPEED/iSPEED, `docs/analysis/benchmark-tms-2026.md` §10 i rejestr odrzuceń.
3. Pytania do każdej liczby: **jaki job?** **przed/po?** **N klientów / N zleceń?** **okno czasu?** **grupa kontrolna?** **czy atrybucja to AI, czy cały TMS?**
4. Vendor −75% admin **bez** metody = pewność **niska**, niezależnie od liczby cytowań w newsach.

### Skala pewności

| Pewność | Kryterium |
|---|---|
| Wysoka | Nazwany klient, przed/po na tym samym jobie, okno, N lub wolumen, metoda (pilot/A-B/model z metryką). |
| Średnia | Nazwany klient + liczba, ale case na stronie vendora; brak kontroli; atrybucja AI/TMS zmieszana. |
| Niska | „Up to”, landing, PR własny, N=0, brak baseline. |
| Bardzo niska | Blog wtórny, LinkedIn, „agent reroutuje tysiące kontenerów” bez primary URL vendora. |

## Tabela: vendor / case → Omni

| Vendor / case | Co AI (deklaracja) robi | KPI podany | Metoda pomiaru | Pewność | Wniosek dla Omni |
|---|---|---|---|---|---|
| **Qargo Intelligence** (landing Qi) | Order entry z maila/PDF; Document Intelligence (plomb, kontener); matching POD; self-billing FV zakupu; RAG jakości skanu; detekcja podpisu; AI-streszczenie firmy | **75%** czasu powtarzalnego adminu; **2 h**/planer/dzień; **−65%** czasu FV; **−70%** obsługi dokumentów; **70%** jobów prosto do processingu; **−50%** czasu na POD; **−50%** email admin; **90%** trafności zleceń (blog vs legacy) | Brak N, braku próby, braku definicji „adminu”. Kompozyt z landing + blog XII 2024 / VII 2025. | **Niska** | **Nie kopiuj autonomii.** Kopiuj **HITL**: szkic pól + review + Create (Qi sam mówi „review and hit Create”). **Nie** auto-generuj FV zakupu. **Nie** auto-scoring z „company summaries”. |
| **Qargo / Joda Freight** | Auto-ekstrakcja zleceń klienta | Złożone zlecenie **15 min → 2 min**; ~**1 h/dzień** planowania (drag&drop, nie LLM) | Jeden named champion (Luke Ryan), case ~2023, go-live III 2023. Sam przyznaje błędy przecinka w wadze. Ambasador vendora (bias). | **Średnia** (KPI order entry); planowanie = UI, nie AI | **Kopiuj HITL M-20** na RFQ/zlecenie. Mierz min/zlecenie przed/po na tenancie, nie „75%”. |
| **Qargo / CS Ellis** | AI order entry z PDF + Xero | Order entry **2 h/dzień → nearly instant**; fakturowanie **−75%** (1,5 dnia → 0,5 dnia) | Named UK 3PL, live od VII 2024. Brak logów czasowych; −75% to cały obieg FV (ePOD+Xero), nie sam OCR. | **Średnia** na FV; **niska** atrybucja „to AI” | Time-to-invoice skraca **ePOD + FK**, nie LLM. Omni: Photo POD + HITL FV (§13m), nie auto-link. |
| **Qargo / Mark Huisman** | Qi PDF→zlecenie; AI-kontrola FV zakupowych; Exact/Shippeo | Fakturowanie **10 h/tydz. → 30 min (−95%)**; +8 h/tydz. po Shippeo | Named NL, go-live 1 I 2026. −95% = TMS+FK+Shippeo. Brak próby czasowej. | **Średnia** (named + przed/po); atrybucja AI **niska** | Nie sprzedawaj „AI ścięło 95%”. Mierz osobno: extract min, match FV, sync Exact. |
| **Qargo / Eskatrans** | AI: 60 nr kontenerów z 1 zdjęcia; reszta = cenniki, portal, Transics | Cykl FV **2 tyg. → 2 dni (−86%)** | Named BE ~125 aut. −86% to paperless+driver app, nie model. | **Średnia** na cashflow; AI **niska** | Photo POD quality (bez GAN) + ref na wydruku. Nie obiecuj OCR 60 kontenerów bez testu. |
| **Qargo / Pass Logistics** | AI order entry + AI odczyt POD | Order entry **5 min → 30 s–2 min** (~9,5 h/tydz.) | Named UK, ~150 zleceń/tydz. Brak stopera niezależnego. | **Średnia** | Dobry KPI produktowy: **sekundy na szkic**, nie % adminu. |
| **Qargo / Kekkilä-BVB** | Qi + **resource allocation** (auto-przydział przewoźnika) | **90%** zleceń auto-assign; order entry 5–10 min → **<1 min**; 2× wolumen bez FTE | Named producent, 200–300 zleceń/dzień, 5 planistów. 90% to **reguły**, nie LLM. | **Średnia** (reguły); AI extract **średnia** | Auto-assign = dane/reguły (M-03), HITL na wyjątku. **Nie** agent kupujący fracht. |
| **Qargo / Portex, FCE, Kees** | Qi order entry | Portex 3→1,5 min; FCE 3–4→1 min; Kees 5→2,5 min | Named, powtarzalny rząd wielkości (połowa czasu wpisu). N=3 anegdoty, ten sam vendor. | **Średnia** | Wzorzec: **połowa czasu wpisu** przy review. Realistyczny cel M-20, nie −75%. |
| **interLAN iSPEED** | „AI wczytuje zlecenia z e-maili i dokumentów”, wskazuje kluczowe zapisy; projekt UIAI | **Brak liczby** | Premiera TransLogistica 4–6 XI 2025. Strona produktu i ispeed.eu: import SID/plików, zero KPI, zero named case AI. SPEED 54 = Delphi, nie AI. | **Niska** (funkcja); KPI = **brak** | Nie benchmarkuj iSPEED jako dowodu ROI. Luka rynku PL: web + HITL extract + KSeF (deterministyczny XML, nie LLM). |
| **Alpega TMS landing** | „Automated tendering & dispatch”; document capture na Transport Execution | **Do 95%** mniej czasu order processing; **80%+** process-cost; ePOD: FV **z tygodni do dni** | Landing. 95% nie ma N. | **Niska** | 95% = slogan. Nie kopiuj. |
| **Forrester TEI Alpega TMS** (VIII 2025, commissioned) | **Nie AI.** TMS + Smart Booking (dock). Automatyzacja komunikacji i dokumentacji eksportowej | **150% ROI / 8 mies. payback**; **80%** czasu freight management; raporty 2 h/region/tydz. × 15 regionów | **N=1** wywiad (UK CPG, €430M+, 380 os., Alpega od 2022). Baseline: **15 min** maila + **5 min** docs / zlecenie. Wolumen 6k→15k zleceń. Forrester: **50% productivity recapture**, −10% risk. | **Średnia** (metoda TEI, N=1, **nie AI**) | Użyj TEI jako wzoru **pomiaru** (min/zlecenie × wolumen × recapture), nie jako dowodu LLM. 80% to EDI/portal, nie extract. |
| **Transporeon Autonomous Procurement / Anheuser-Busch** | Rule-based AI + behavioral science na spot (nie genAI dokumentów) | Pilot: **double-digit** spadek kosztu spot vs stary proces; **+24 h** lead time vs cykl 16:00 | **A/B 45 dni**, połowa ładunków losowo w starym procesie, połowa w AP (I 2021; case PDF wciąż w obiegu 2024–26). Named. | **Wysoka** (metoda); job = **zakup spot**, nie extract | **Nie kopiuj autonomii zakupowej** do Omni (carrier agent = HZ). Kopiuj **pomiar A/B** i guardrails ceny. |
| **Transporeon / Pfeifer Group** | To samo AP | **84%** automatyzacji assignmentu spot (16% ręcznie) | Named, case vendora, brak okna/wolumenu w publicznym tekście. | **Średnia** | Reguły + sufit ceny. Człowiek na 16%. Wzorzec HITL, nie 100% agent. |
| **Transporeon / James Hardie** | AP | **11,7%** oszczędności frachtu; marketing: 90% match, do 12% taniej, **70%** quoting | Event + strona AI. 11,7% bez protokołu w HTML. 70% quoting = **unnamed** „European LSP” (turnover +150%). | **Niska–średnia** | Nie cytuj 70%/150% bez nazwy. |
| **Transporeon Visibility / Saint-Gobain Isover** | Predykcja przyjazdu (nie LLM) | **90–95%** transportów trackowanych; **−40%** zapytań o status; ~€50k kar | Named, visibility. Check-calls, nie dokumenty. | **Średnia** | Mapuj na wieżę + Prediction Ledger, **nie** na M-20. LLM nie liczy ETA (`006-telematics-hub.md`). |
| **Transporeon Freight Audit / ASICS** | Audit stawek (reguły), nie genAI | **70%** szybsza analiza kosztów | Named quote, brak baseline minut. Labor −30% = managed service landing. | **Niska–średnia** | Matching FV = SQL + HITL (§13m). Nie auto-pay. |
| **Infios TM** (MercuryGate) | „Generative AI accelerates document processing and order creation”; agentic exceptions | **Brak liczby** w karcie produktu | Rebrand, cytat Ben Darling o szybkości zmian vs scraping. Zero named case minut. | **Niska** | Lukę wypełniają **third-party** (Alfabolt „60% less entry / 5 min touch” — vendor integrator, nie MG). Nie kopiuj agentic exceptions. |
| **PaperEntry / V. Alexander** (warstwa na CargoWise, nie native TMS) | GenAI extract CI/PL → CargoWise | **80%** efficiency; auto-publish **2,8 min**; **2 000+ h/rok**; ID **99,1%**, extract **98,7%** | Named forwarder/broker. Vendor case. Brak niezależnego audytu. | **Średnia** | Najbliższy **M-20** poza Qargo/Forto. Kopiuj: pewność pola + próg + HITL. Nie 98,7% jako SLA. |
| **Forto FlashDoc** (1 VII 2025) | GenAI: klasyfikacja 12 typów docs (waybill, packing list, customs, FV), extract, push do IT; flaga niepewności | **Do 53 min**/shipment; **>20%** efektywności ops managera; **95%** accuracy | **Wewnętrzny** Forto „od początku roku” / „>6 miesięcy”. Brak N przesyłek, brak definicji accuracy (pole vs dokument). HITL przy uncertainty, self-learning z korekt. | **Średnia** (named vendor na sobie); **niska** na zewnątrz | **Kopiuj HITL + flagę niepewności.** 53 min = „up to”. Nie auto-zapis. Flash by Forto (agent booking→FV) = **nie kopiuj autonomii**. |
| **Flexport Winter 2026** (primary) | AI agent audytu zgłoszeń celnych; AI opt. wykorzystania kontenera; AI Search; tłumaczenia | Error rate **0,2%** (szacunek **10×** vs branża); consolidation **do 10%** cost — **rekomendacja do approve**; notyfikacje **−80%** | Primary URL produktu. 0,2% bez mianownika (ile zgłoszeń, jaki błąd). 10% = „up to” + HITL. −80% to filtr notyfikacji, nie AI. | **Średnia** na 0,2% (primary, słaba definicja); 10% **niska** | Cło: model **klasyfikuje szkic**, broker **akceptuje**. Opt. kontenera = rekomendacja, nie auto-book. **Nie** auto-credit. |
| **Flexport 68% zgłoszeń bez brokera** | Automated Entry Preparation / HTS ML | **68%** shipments without human broker; HTS **94%** first-pass, **−40%** czasu brokera | **Ecommerce Times** cytuje Flex Forward V 2026 — **brak primary URL Flexport** w tym audycie. | **Bardzo niska** | Nie wkładaj do pitcha Omni. Jeśli kiedyś primary — i tak PL ≠ US HTS; HITL zostaje. |
| **Flexport „40% operacji AI”** | Agenci frachtu | 8% (I 2025) → 40% (III/VIII 2026); reroute 2300 kontenerów | LinkedIn / blogi wtórne, nie flexport.com. | **Bardzo niska** | Ignoruj. |
| **project44 ETA engine** (2 X 2025) | ML (ensemble, classifier, transformer, error-correction); **nie** LLM | **+28 pp** accuracy na horyzoncie **10 h**, okno **±2 h**; 10 modeli prod.; **500+** FTL shipperów; case’y +20–25 / +35 / +8 pp | Metryka zdefiniowana. N duży. Tenant-specific models. | **Wysoka** (ETA); **nie dotyczy** extract | **Prediction Ledger**: ta sama dyscyplina (MAE, okno, coverage, retrening). LLM **nie** liczy ETA. |
| **project44 / Cargoways, Family Leisure, RR Donnelley** | Visibility, nie genAI docs | Cargoways **−80%** check calls; Family Leisure **−75%** „where’s my order”; RR Donnelley **700–900** połączeń/dzień mniej | Named, ale check-call ≠ AI dokument. Family Leisure case stary (sezon 2016+). | **Średnia** (visibility) | Portal + tracking link (§13i) **bez LLM**. Quote engagement = piksel/PDF, nie model. |
| **Gartner MQ TMS 2026** (30 III 2026, cytaty Oracle/Manhattan/SAP) | Trend: GenAI i **agentic AI** (sloty, exceptions, freight procurement) | **Brak KPI czasu** w publicznych cytatach | MQ za paywallem. Publiczne PR powtarzają zdanie o różnicowaniu produktem AI. | **Niska** jako dowód ROI | Trend ≠ zmierzony job. Nie cytuj Gartnera jako „−X% admin”. |
| **McKinsey: Succeeding in the AI supply-chain revolution** | AI SCM (forecast, IBP, fizyczny flow) | Early adopters: **−15%** logistics cost, **−35%** inventory, **+65%** service vs wolniejsi | Artykuł branżowy (metals/mining URL). **Nie TMS, nie 2024–26 extract.** Porównanie vs konkurenci, nie przed/po. | **Niska** dla jobu spedytora | Nie używać w argumentacji M-20. |
| **McKinsey: Beyond automation / gen AI** (17 IV 2025, podcast) | GenAI docs, virtual dispatcher | Docs lead time **do −60%**; workload koordynatora **−10–20%**; unnamed last-mile 10k aut: **$30–35M** / capex **$2M** | Wypowiedź partnera, nie tabela badania. „Up to”. | **Niska** | Kierunek (docs + HITL) zgadza się z Forto/Qargo; liczby nie są DoD. |
| **McKinsey: Digital logistics: Into the express lane** | Ankieta **>260** shipper+provider; ~12 use-case’ów genAI | **>85%** „digital dodało wartość”; **>40%** wdrożeń **dłużej** niż plan | Survey, nie case TMS. | **Średnia** (realizm wdrożeń) | Argument **przeciw** obietnicy „AI w 4 h”. Sandbox jak u Qargo. |
| **McKinsey: Digitizing mid/last-mile handovers** | RTTVP + workflow AI + genAI komunikacja | Blind handoffs = **13–19%** kosztów logistyki US; combo rozwiązań **do −40%** waste | Analiza McKinsey + BTS, nie vendor TMS. | **Średnia** jako wielkość problemu | Problem = brak danych na styku, nie brak LLM. |

## Top 10 (liczba albo „brak liczby”)

To nie ranking jakości produktu. To **najczęściej cytowane albo najbliższe jobowi Omni**, ze statusem pomiaru.

| # | Case | Liczba | Status pomiaru |
|---|---|---|---|
| 1 | Qargo Intelligence (landing) | **−75% admin** | Slogan. Brak N, braku jobu, braku przed/po. |
| 2 | Qargo / Joda Freight | **15 min → 2 min** order entry | Named, 1 firma, 1 typ zlecenia; champion vendora. |
| 3 | Qargo / Mark Huisman | **10 h → 30 min** fakturowanie | Named przed/po; atrybucja = TMS+Exact+Shippeo, nie sam Qi. |
| 4 | Qargo / CS Ellis | **fakturowanie −75%** | Named; time-to-invoice, nie OCR. |
| 5 | Forto FlashDoc | **do 53 min/shipment**, **95%** | Wewnętrzny Forto, 6 mies.; „up to”; HITL przy niepewności. |
| 6 | Forrester TEI Alpega | **80%** czasu / **150% ROI** | N=1, min/zlecenie policzone; **nie AI**. |
| 7 | Transporeon × Anheuser-Busch | **double-digit** spot + **+24 h** | Najlepsza metoda (A/B 45 dni). Inny job (zakup). |
| 8 | project44 ETA | **+28 pp** @ 10 h ±2 h | Najlepsza metoda predykcji; N=500+ FTL. Nie extract. |
| 9 | Pfeifer / Transporeon AP | **84%** auto-assignment | Named; brak wolumenu w tekście publicznym. |
| 10 | iSPEED AI **oraz** Infios/MercuryGate native GenAI | **brak liczby** | Premiera / rebrand. Zero named KPI minut. |

Honorowe: Pass 5 min→30 s (średnia); Eskatrans 2 tyg.→2 dni (średnia, nie AI); V. Alexander 2,8 min / 2000 h (średnia, warstwa na CargoWise); Flexport 0,2% błędów celnych (primary, słaba definicja); Flexport 68% (brak liczby w primary — **nie liczyć**).

## Atrybucja: co naprawdę tnie czas

Z 44 case’ów Qargo ten sam wzorzec wraca niezależnie od Qi:

1. **Przepisanie mail/PDF** — jedyny job, gdzie cytaty klientów są spójne (rząd **2–5 min → ~1 min** albo 15→2 na trudnym zleceniu). To jest M-20.
2. **Time-to-invoice** (Huisman −95%, Ellis −75%, Eskatrans −86%, FCE tydzień→1–2 dni) — pęka, gdy **CMR/POD wraca z kabiny** i **FK się syncuje**. Qi matching pomaga; bez ePOD liczba nie powstaje.
3. **Check-calls / „gdzie ładunek”** — portal, tracking link, Transporeon Visibility, project44. **Nie LLM.** W Omni: quote engagement **bez modelu** (`008-quote-engagement.md`).
4. **Puste kilometry / routing** (Anglia −6–8%) — silnik map/opt, nie extract.
5. **90% auto-assign** (Kekkilä) — reguły zasobów.

Wniosek metodologiczny: jeśli Omni zmierzy „AI”, musi **rozbić KPI**. Inaczej powtórzy grzech Qargo (jeden % na cały back-office).

## Mapowanie na powierzchnie już w planie Omni

| Powierzchnia Omni | Co bierze z rynku | Czego nie bierze |
|---|---|---|
| **M-20 extraction HITL** (stawki, FV, RFQ) | Szkic z maila/PDF; pole + pewność; review; Joda/Pass/Portex jako **rząd wielkości minut**. Forto: flaga uncertainty + korekta uczy. KSeF = XML, nie LLM (`benchmark` §13m). | Auto-zapis `rate_line` / `charge`. Auto-link FV. Qi self-billing „generate automatically”. |
| **Photo POD quality** | RAG Qargo (zła czytelność → wyjątek); Forto flag. Pipeline Omni: ramka na żywo + OpenCV deskew (`010-scan-enhance-hitl.md`). | **GAN / inpainting tekstu.** „FULL” enhance na FV. Upscale jako dowód podpisu. |
| **Document Intelligence diff** | Qargo: match POD→trip, conflict na polach. Omni: diff waga/sztuki/data vs zlecenie, recenzja, nie overwrite (§13n X6). | Cichy overwrite. Auto-akceptacja przy pewności modelu. |
| **Quote engagement (nie LLM)** | Nikt z vendorów nie dowiódł, że LLM skraca lejek oferty. Qargo/Transporeon tną telefony **portalem**. | Piksel bez zgody. Scoring osoby. „AI przewiduje, że otworzy maila”. |
| **Prediction Ledger ETA** | project44: okno, horyzont, pp accuracy, retrening, explain „+3 h bo dwell”. McKinsey handoffs: problem danych, nie czatu. | LLM liczący ETA. Obietnica marketingowa „AI przewiduje przyszłość” (rejestr odrzuceń). |
| **Zakaz auto-charge** | Żaden case nie pokazuje bezpiecznego auto-charge. Marża = `charge` (HC). | Qi / Flash agent wystawiający sprzedaż. |
| **Zakaz auto-link FV** | Qi i Alpega sugerują auto-reconcile. Omni: drabina SQL + accept. | 1-klik bez progu i bez człowieka przy remisie. |
| **Zakaz GAN upscale** | Brak case’u TMS, który by to zmierzył jako KPI jakości prawnej skanu. | Forto/Qargo enhance ≠ generowanie pikseli podpisu. |
| **Zakaz auto-credit score** | Qargo „company summaries” (obrót, skala z danych publicznych) jest **o jeden krok** od scoringu. AI Act + art. 22. | Auto-ocena JDG/osób. Qargo summaries tylko jako szkic faktów + HITL (M-10 lookup). |

## Rekomendacja dla operatora (projektant OmniRoute)

### Gdzie AI skraca **budowę** produktu (instructor + testy, nie nowy silnik)

1. **Instructor / structured extract** na istniejącym M-20: pola + `amount_text` + pewność; testy na corpusie FV/RFQ/cennik — zamiast „silnika Document Intelligence”.
2. **Testy regresji extractu** (waga z przecinkiem — Joda to przyznał): fixture PDF, nie demo.
3. **Eval zestawu** jak project44: zdefiniuj okno (np. % pól bez poprawki operatora, czas accept, overlap bbox). To jest Prediction Ledger dla dokumentów, nie nowy BC.
4. **Generowanie testów i mapperów** (KSeF FA(3) jest deterministyczny — AI może pisać testy, nie parser).
5. **Nie buduj** agenta slotów terminala, auto-procurement, chat-TMS, GAN, scoringu. Gartner nazywa to „baseline 2026”; publicznie **nie ma** zmierzonego ROI, a Forto Flash agent i Flexport 40% to narracja, nie protokół.

### Gdzie AI w **produkcie** skraca job spedytora

Kolejność wg dowodów, nie wg slajdów:

1. **Mail/PDF → szkic zlecenia/RFQ/stawki** (HITL Create). Jedyne miejsce, gdzie named case’y powtarzają minuty. Cel produktowy: **połowa czasu wpisu**, nie −75% FTE.
2. **Skan POD/CMR/FV → kandydat + diff.** Czas do faktury spada, gdy dokument **wraca** (apka) i **nie wymaga przepisywania**. Matching = SQL; model wypełnia pola.
3. **Jakość zdjęcia przed OCR** (odrzut „zrób jeszcze raz”) — taniej niż GAN i zgodne z zakazem.
4. **ETA / wieża** — ML z ledgerem, telematyka BYO, bez LLM.
5. **Lejek oferty** — token PDF + zgoda na piksel. Zero modelu.

Nie skracaj jobu spedytora przez: auto-charge, auto-link FV, autonarrację marży, auto-kredyt, agentic booking, „75% mniej adminu” na stronie. To są liczby, których vendorzy **nie zmierzyli** albo zmierzyli na **innym** jobie (spot, dock, visibility, wymiana TMS).

### Jak mierzyć u pierwszego tenanta (żeby nie kłamać jak landing)

Na jednym jobie, 4 tygodnie przed / 4 po, ten sam zespół:

| KPI | Definicja | Co odrzucić |
|---|---|---|
| Order entry | mediana minut od otwarcia maila do `accept` szkicu | „% adminu” |
| Time-to-invoice | godziny od POD (status delivered) do wystawienia FV | OCR accuracy marketingowa |
| POD processing | % skanów reject quality vs accept; minuty HITL | GAN „wygląda ostro” |
| FV match | % 1-kandydat / lista / nieprzypisane; zero auto-link | „65% mniej FV” bez N |
| ETA | MAE w oknie ±2 h na horyzoncie N h | „AI przewiduje” |

N klientów w pitchu Omni = **ten tenant**, dopóki nie ma drugiej próby. N=44 case’ów Qargo to **marketing corpus**, nie meta-analiza.

## Źródła (URL)

### Qargo

- https://www.qargo.com/platform/qargo-intelligence/
- https://www.qargo.com/post/introducing-qargo-intelligence-ai-powered-features/
- https://www.qargo.com/post/ai-powered-tms-automation/
- https://www.qargo.com/post/introducing-qargo-email-intelligence/
- https://www.qargo.com/post/qargo-vs-legacy-systems/
- https://www.qargo.com/cases/joda-freight/
- https://www.qargo.com/cases/cs-ellis-logistics/
- https://www.qargo.com/cases/case-study-mark-huisman/
- https://www.qargo.com/cases/eskatrans/
- https://www.qargo.com/cases/pass-logistics/
- https://www.qargo.com/cases/kekkila-bvb/
- https://www.qargo.com/cases/case-study-portex-logistics/
- https://www.qargo.com/cases/fce-transport-b-v/
- https://www.qargo.com/cases/kees-int-veen/
- Lokalnie: `C:\Users\sebas\.cursor\projects\d-OMNIROUTE\benchmark\qargo-cases.md`, `qargo-news.md`

### interLAN

- https://www.interlan.pl/produkty/ispeed/
- https://www.interlan.pl/premiera-ispeed-na-translogistica-poland-2025/
- https://ispeed.eu/
- Lokalnie: `benchmark\speed-dossier.md`

### Transporeon / Alpega / MercuryGate

- https://www.transporeon.com/en_US/artificial-intelligence/solutions
- https://www.transporeon.com/en_US/artificial-intelligence/ai-in-transportation
- https://www.transporeon.com/website/pdf/case_study/Transporeon_CaseStudy_Anheuser-Busch_US.pdf
- https://www.transporeon.com/en/community/case-studies/pfeifer-group
- https://www.transporeon.com/en/community/events/journey-to-ai-powered-transportation-with-james-hardie
- https://www.alpegagroup.com/en-en/transport-management-system/
- https://www.alpegagroup.com/en-en/community/library/forrester-tei-study/
- https://tei.forrester.com/go/alpega/tms/
- https://telematik-markt.de/sites/default/files/news/attachments/Forrester_TEI_The_Total_Economic_Impact_Of_Alpega_TMS.pdf
- https://www.infios.com/en/supply-chain-solutions/transportation-management

### Forto / Flexport / warstwy na CargoWise

- https://forto.com/en/press-releases/flashdoc-by-forto-ai-based-document-processing-in-seconds/
- https://forto.com/en/press-releases/forto-launches-flash-by-forto-to-transform-global-freight-operations/
- https://www.flexport.com/technology/product-release/winter-2026/
- https://www.businesswire.com/news/home/20260226536552/en/Flexport-Launches-Technology-to-Automate-Tariff-Refunds
- https://deepcognition.ai/v-alexander-co-case-study/
- Wtórne, **nie używać jako primary:** https://ecommerce-times.com/flexport-in-2026-the-digital-freight-broker-grows-up/

### Predykcja / analityka

- https://www.project44.com/blog/eta-reimagined-transforming-project-44s-prediction-engine/
- https://www.project44.com/customer-stories/family-leisure-saves-money-and-improves-the-customer-experience-with-project44/
- https://blogs.oracle.com/scm/oracle-leader-2026-gartner-tms-magic-quadrant
- https://www.manh.com/our-insights/resources/research-reports/gartner-tms-magic-quadrant-report
- https://news.sap.com/2026/04/sap-a-leader-2026-gartner-magic-quadrant-tms/

### McKinsey

- https://www.mckinsey.com/industries/metals-and-mining/our-insights/succeeding-in-the-ai-supply-chain-revolution
- https://www.mckinsey.com/capabilities/operations/our-insights/beyond-automation-how-gen-ai-is-reshaping-supply-chains
- https://www.mckinsey.com/capabilities/operations/our-insights/digital-logistics-into-the-express-lane
- https://www.mckinsey.com/industries/logistics/our-insights/digitizing-mid-and-last-mile-logistics-handovers-to-reduce-waste
- https://www.mckinsey.com/industries/industrials-and-electronics/our-insights/distribution-blog/harnessing-the-power-of-ai-in-distribution-operations

### Omni (plan, nie źródło rynku)

- `docs/analysis/benchmark-tms-2026.md` §10 AI, §13i–§13o, rejestr odrzuceń
- `docs/_knowledge/market/008-quote-engagement.md`
- `docs/_knowledge/market/010-scan-enhance-hitl.md`
- `docs/_knowledge/market/006-telematics-hub.md`
