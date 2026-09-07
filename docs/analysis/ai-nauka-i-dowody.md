# AI w TMS/spedycji: co jest zmierzone, a co jest bias / brak dowodu

**Audyt faktów.** Zero marketingu. Data: 2026-09-07.  
Nie commituje. Nie zmienia CURRENT/PLAN. Nie jest specyfikacją produktu.

**Kontrakt OmniRoute (nie negocjowany tu — mapowany do literatury):** LLM wyciąga, kod liczy; HITL przed zapisem; `charge` = jedyny wiersz buy+sell (marża); LLM nie scoruje JDG/osób; etykieta Art. 50 na szkicu.

**Skala pewności:** *wysoka* = RCT albo recenzja (czasopismo / konferencja z programem); *średnia* = warsztat, ICDAR, MDPI, arXiv z jawną metodą i n; *niska* = ankieta branżowa, blog, preprint bez recenzji.  
DOI i URL tylko jeśli otwarto źródło. Brak paperu = **BRAK ŹRÓDŁA**, nie zgadywany tytuł.

**Co nie jest dowodem:** „99% accuracy” na stronie vendora; case study bez protokołu i ground truth; self-report produktywności bez stopera; MAE bez kalibracji jako „AI przewiduje”.

---

## 1. Tabela — obszary OmniRoute

| Obszar Omni | Wniosek | Źródło (autor, rok, URL) | Co zmierzono | Pewność |
|---|---|---|---|---|
| Ekstrakcja FV/cennika/dokumentu do **szkicu** (pola z layoutu), nie do księgi | **TAK AI** jako OCR/KIE; **TYLKO HITL** przed zapisem | Šimsa et al., 2023, DocILE (ICDAR). https://arxiv.org/abs/2302.05658 | 6,7k anotowanych dokumentów biznesowych, 55 klas. Baseline LayoutLMv3: KILE F1 **0,698**, LIR F1 **0,721**. Górne ograniczenie NER na danym OCR: F1 **0,946** / **0,961** — reszta to mismatch tokenów OCR vs pole. Autonomiczny extractor zostawia systematyczny błąd pól, w tym linii tabeli. | wysoka (benchmark ICDAR; nie RCT HITL vs auto) |
| Autonomiczny zapis extractu do TMS/FK (zero recenzji) | **NIE AI** | Goddard, Roudsari, Wyatt, 2012, *JAMIA*. https://doi.org/10.1136/amiajnl-2011-000089 | Przegląd systematyczny 74 prac. Meta-analiza 4 homogenicznych badań CDSS: risk ratio **1,26** (95% CI 1,11–1,44) — błędna rada systemu częściej prowadzona niż w grupie bez DSS. „Negative consultations” (zmiana dobrej decyzji na złą po radzie): **6–11%** przypadków. DSS 80–90% exact nie eliminuje overreliance. | wysoka |
| Operator „sprawdza” extract, ale klika Accept przy złym polu (automation bias) | **TYLKO HITL** z weryfikacją względem źródła; sama pętla recenzji nie wystarczy | Skitka, Mosier, Burdick, 1999, *Int. J. Human-Computer Studies*. https://doi.org/10.1006/ijhc.1999.0252 | Symulacja lotu, aid 94% reliable vs wskaźniki 100% true. Omission: dokładność **59%** z aidem vs **97%** bez (*p*<0,05). Commission: średnio **3,92/6** błędnych dyrektyw przyjętych (dokładność **35%**); **23,1%** osób przyjęło **wszystkie 6**. Mosier et al. 1998 (piloci): omission **55%**, commission przy fałszywym fire **100%**. | wysoka |
| Ten sam bias nazwany w prawie (nadzór człowieka) | **TYLKO HITL** — wymóg projektowy, nie „feature AI” | Rozporządzenie (UE) 2024/1689, art. 14 ust. 4 lit. b. Tekst skonsolidowany: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02024R1689-20260727 | High-risk: osoby nadzorujące mają być świadome tendencji do automatycznego polegania na wyjściu (**automation bias**). To nie pomiar dokładności — to norma, że HITL bez de-biasingu jest niewystarczający. | wysoka (akt prawny) |
| LLM **liczy** VAT, sumy, marżę, kurs, `chargeable_weight` | **NIE AI** | Gao et al., 2023, PAL, ICML. https://proceedings.mlr.press/v202/gao23f.html | Codex+CoT GSM8K **65,6%**; ten sam model z offloadem do interpretera Pythona **72,0%**. GSM-HARD (duże liczby): CoT **20,1%**, PAL **61,2%** (Δ ok. **40 pp**). Ablacja: LLM „wykonuje” wygenerowany kod bez interpretera → **23,2%** na GSM8K vs PAL **72,0%**. 16/25 par CoT: ten sam tok rozumowania, zła arytmetyka. | wysoka |
| LLM **wyciąga** kwoty jako tekst; walidacja/arytmetyka w kodzie | **TAK AI** (ekstrakcja) + **NIE AI** (liczenie) | Shu et al., 2025, LAVA, ACL FinNLP. https://doi.org/10.18653/v1/2025.finnlp-2.7 | Dokumenty finansowe, reguły C1–C5. Numerical infidelity C5: LAVA **0,00** vs baseline LLM+OCR **0,10–0,25**. Usunięcie Arithmetic Processor (liczenie w LLM): błąd C4/C5 **0,10 / 0,56**. Wniosek empiryczny zbieżny z PAL: model nie jest kalkulatorem. | średnia (warsztat ACL, jawna ablacja) |
| Deskew / prostowanie skanu przed OCR (geometria, nie generowanie treści) | **TAK** klasyczne/learned **rectify**; nie generative SR | Markovitz et al., 2020, CREASE. https://arxiv.org/abs/2008.02231 | Rectyfikacja zdjęć dokumentów. Względem SOTA: spadek błędu OCR (edit distance) **20,2%** relatywnie (**4,5 pp** absolutnie), błąd geometryczny **−14,1%**. Mierzy czytelność po transformacji, nie „dopisanie” glifów. | średnia (arXiv z metodą i n; nie weryfikowałem tu numeru tomu konferencji) |
| Generative super-resolution / inpainting cyfr na FV | **NIE AI** | Zyrek, Tarasiewicz, Sadel, Krzywon, Kawulok, 2025, *Appl. Sci.* https://doi.org/10.3390/app15148063 | SR dokumentów pod OCR. Autorzy: sieci GAN „occasionally hallucinate glyphs on unseen degradations”. Modele perceptualne (EDSR/SwinIR) „more likely to hallucinate image details”. Ren et al., 2025, Hallucination Score (preprint): https://arxiv.org/abs/2507.14367 — GSR (SeeSR, PASD) produkuje detale niezgodne z LR; PSNR/SSIM/LPIPS tego nie łapią. | średnia / niska (MDPI + preprint HS; mechanizm spójny, brak RCT na FV spedycyjnych) |
| Predykcja ETA statku z AIS vs ETA agenta | **TAK AI** (ML tabelaryczny/AIS), **nie LLM**; tylko ze scorecardem | Evmides et al., 2024, *J. Mar. Sci. Eng.* https://doi.org/10.3390/jmse12081362 | AIS wschodni Med. Random Forest MAE **99,9 min**, RMSE **163,3**; ETA od agentów MAE **178,4**, RMSE **305,2**. To ML na telemetry, nie „chat przewiduje przybycie”. Kalibracja rozkładu w tej pracy **nie** jest główną metryką. | średnia (MDPI, hold-out MAE; bez CRPS) |
| „AI przewiduje opóźnienie/disrupt” bez MAE/CRPS/kalibracji | **NIE AI** (bezwartościowe jako decyzja) | Gneiting, Raftery, 2007, *JASA*. https://doi.org/10.1198/016214506000001437 PDF: https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf | Cel prognozy probabilistycznej: **ostrość pod warunkiem kalibracji**. CRPS uogólnia błąd bezwzględny. Niewłaściwa scoring rule nagradza kłamstwo o pewności. Punktowe „AI mówi że spóźni się o 2 h” bez reliability diagramu nie jest ewaluacją. | wysoka (teoria; nie TMS) |
| Mail → pola RFQ / chartering (email-to-order) | **TYLKO HITL**; **BRAK** RCT na prawdziwej skrzynce spedycyjnej | Bründler, Clematide, 2026, MaritimEmails, LREC. http://www.lrec-conf.org/proceedings/lrec2026/pdf/2026.lrec2026-1.599.pdf | **19 817 syntetycznych** wątków (nie produkcja). IE: GLiNER do **0,86** macro-F1; Incoterms 20–30 pp gorzej niż inne encje. Autorzy: nie ma publicznego korpusu prawdziwych maili brokerskich (poufność). Vendor „97–99%” — odrzucone (sekcja 4). | średnia (LREC, syntetyk) / **BRAK ŹRÓDŁA** na czas/koszt w freight live |
| Scoring kredytowy **osób** i JDG (natural person) | **NIE AI** | Rozporządzenie (UE) 2024/1689, załącznik III pkt 5 lit. b + motyw 58. https://artificialintelligenceact.eu/annex/3/ https://ai-act-service-desk.ec.europa.eu/en/ai-act/recital-58 | High-risk: systemy „to evaluate the creditworthiness of **natural persons** or establish their credit score”; wyjątek: wykrywanie oszustwa finansowego. Motyw 58: dostęp do finansów, mieszkania, prądu, telekomu; ryzyko dyskryminacji. JDG = osoba fizyczna w działalności — w zakresie 5(b). Scoring **osoby prawnej** (sp. z o.o. po bilansie) **nie** jest tym punktem. Nie jest to zakaz — to reżim high-risk (art. 8–27), którego OmniRoute świadomie nie wdraża dla osób. | wysoka (lex lata) |
| Etykieta „propozycja AI” na szkicu extractu / maila | obowiązek transparentności, nie zysk dokładności | Art. 50 ust. 1–2 i 5. https://artificialintelligenceact.eu/article/50/ | Od 2.08.2026: informacja, że osoba wchodzi w interakcję z systemem AI (chyba że oczywiste); wyjścia syntetyczne — znacznik maszynowo czytelny. Ust. 4 (tekst publiczny) dotyczy publikacji w interesie publicznym, nie każdej oferty spedycyjnej. Mapowanie kontraktu: label na draftcie operatora. | wysoka (lex lata) |
| Copilot dla **budowniczego** oprogramowania (plastry, nie operator TMS) | **TAK AI** na zadaniach izolowanych i u juniorów; **nie gwarancja** na dojrzałym repo | Peng et al., 2023 (lab Copilot). https://arxiv.org/abs/2302.06590 — n=95, HTTP server JS: **55,8%** szybciej (p=0,0017; 95% CI **21–89%**); ukończenie 78% vs 70%. Cui et al., *Management Science*, 3 RCT, n=**4867** (Microsoft, Accenture, Fortune 100). https://doi.org/10.1287/mnsc.2025.00535 — **+26,08%** ukończonych zadań/PR (SE **10,3%**); większy zysk u mniej doświadczonych. Becker et al. / METR, 2025, RCT Cursor Pro na własnym OSS. https://arxiv.org/abs/2507.09089 https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — 16 deweloperów, 246 issue: **+19% czasu** z AI; przed: oczekiwano **−24%**; po: nadal szacowali **−20%**. | wysoka (dwa RCT + jeden RCT Cursor). **BRAK ŹRÓDŁA**, że Copilot redukuje leftover plastrów albo liczbę testów w tym repo. |

---

## 2. Pięć odrzuceń — „AI tu nie”

1. **LLM jako kalkulator VAT/marży/kursu/`charge`.** PAL: CoT spada z 65,6% do 20,1% na dużych liczbach; LAVA: bez silnika arytmetycznego błąd C5 = 0,56. Marża zostaje w kodzie/SQL na jednym wierszu buy+sell.

2. **Zapis ekstrakcji bez HITL (straight-through do bazy).** DocILE zostawia ~30% błędu pól na mocnym baseline. Goddard: błędna rada zwiększa błąd człowieka (RR 1,26). Skitka: commission mimo 100% prawdziwych wskaźników obok. Art. 14 wprost nazywa automation bias.

3. **Generative SR / inpainting / „dopisz brakującą cyfrę” na skanie FV.** Zyrek et al. 2025: halucynacja glifów. Ren et al. 2025: metryki percepcyjne chwalą obraz, który kłamie. Rectify/deskew (CREASE) jest inną klasą: geometria, nie synteza znaku.

4. **Scoring kredytowy osób i JDG.** Zał. III 5(b) + motyw 58. Nie moralizowanie: to klasyfikacja high-risk. Fraud-detection jest wyłączony z 5(b); scoring sp. z o.o. po sprawozdaniu — poza tym punktem. LLM-score osoby na karcie kontrahenta = ten use-case.

5. **ETA/disrupt i routing jako „LLM przewidzi / ułoży trasę” bez scorecardu i bez solvera.** ETA z AIS ma MAE w literaturze (Evmides 2024) — to nie LLM. Bez kalibracji/CRPS (Gneiting & Raftery 2007) punktowa wróżba nie jest decyzją. LLM jako end-to-end solver VRP: przegląd arXiv:2607.00604 (2026, preprint) pokazuje duże luki feasibility vs heurystyki OR; **nie** zastępuje solvera. Pewność tego przeglądu: niska–średnia (brak recenzji w momencie audytu).

---

## 3. Co to daje użytkownikowi spedycji vs projektantowi

Tylko tam, gdzie jest liczba w źródle. Reszta = **BRAK ŹRÓDŁA**.

### Operator / AP / spedycja

| Twierdzenie | Źródło | Limit |
|---|---|---|
| Koszt pracy na FV spada przy automatyzacji obiegu (e-faktura jako proxy), nie przy „magicznym LLM” | IOFM, World Class AP (~2021), kopia: https://www.ashconversions.com/wp-content/uploads/2023/05/IOFM-World-Class-AP-Performance-Efficiency-Benchmarking-Metrics.pdf — **6,30 USD**/FV (brak automatyzacji, desk-level) vs **1,45 USD**/FV (end-to-end, department-level). Metoda: suma płac AP / liczba FV; n rzędu 200+ działów. | Ankieta, nie RCT, **nie** ekstrakcja LLM. Mierzy dojrzałość workflow, nie F1 pól. |
| Extractor nie zdejmuje recenzji linii i VAT | DocILE: LIR F1 baseline **0,72**; górne OCR **0,96** | HITL na kwotach i liniach jest kosztem stałym, nie „edge case”. |
| Mail chartering da się parsować encjami | MaritimEmails: F1 do **0,86** na **syntetyku** | **BRAK ŹRÓDŁA** na minuty/FV albo błąd stawki na żywej skrzynce PL/DE. Case Fr. Meyer’s Sohn (theblue.ai) nie podaje F1 ani czasu. |

### Projektant oprogramowania (szybsze plastry?)

| Twierdzenie | Źródło | Limit |
|---|---|---|
| Na **jednym** zadaniu lab (HTTP server) Copilot skraca czas o ~56% | Peng et al. 2023, n=95 | Zadanie greenfield, nie dojrzały monolit z RLS/testami izolacji. CI szeroki (21–89%). |
| W firmie, na tygodniowych PR, +26% zadań | Cui et al., *Management Science*, n=4867 | SE 10,3 pp — efekt realny, mniejszy niż lab. Większy u mniej doświadczonych. Nie mierzy jakości recenzji ani leftover. |
| Na **własnym**, dużym OSS, z Cursor Pro (wczesny 2025): wolniej o 19%, przy przekonaniu że jest szybciej o 20% | METR / Becker et al. 2025, n=16×246 | RCT produktu Cursor-like. Autorzy zastrzegają: nie generalizować na juniorów i nieznane repo. Self-report produktywności jest **antykalibracją**. |
| Mniej leftover / mniej testów / szybszy plaster w tym repo | — | **BRAK ŹRÓDŁA.** |

Wniosek dla budowniczego OmniRoute (nie dla operatora TMS): narzędzie kodujące ma **dowód na zysk w labie i umiarkowany zysk w korporacyjnym RCT Copilota**, oraz **dowód na spowolnienie doświadczonych autorów dojrzałego repo w RCT Cursor 2025**. Nie ma paperu, który mierzy „mniej leftover”. Ślepe zaufanie do Copilota u autora to ten sam automation bias co u operatora FV (Skitka; METR: 20% „czuję że szybciej” przy +19% czasu).

---

## 4. Źródła świadomie odrzucone (nie w tabeli)

| URL / typ | Dlaczego nie |
|---|---|
| factura.ai, fasterquotes.io, airparser.com, keelway, freightmynd | Vendor claims 95–99%, brak protokołu, brak hold-out, brak n. |
| GitHub Blog o Copilocie | Ten sam eksperyment co Peng 2023; blog nie dodaje metody. |
| WPS „HITL vs autonomous cost” | Felieton, liczby z palca ($35–50/h). |
| MADP, arXiv:2605.17159 (2026) | Preprint; accuracy 98,5% na **100** dokumentach; FTE 70% to ekstrapolacja 100k FV. Nie recenzja. |
| „C.H. Robinson 99,2% quote accuracy” na case-studies.ai | **BRAK ŹRÓDŁA** pierwotnego paperu. |
| GLM 5.2 VAT blog (developersdigest) | N=59 transakcji, nie recenzja, myli klasyfikację z arytmetyką. |

---

## 5. Luki (uczciwy BRAK)

- RCT HITL vs fully-autonomous **na FV spedycyjnych** z kosztem błędu (marża, KSeF, duplikat płatności): **BRAK ŹRÓDŁA**.
- Czas operatora (minuty) na recenzję extractu vs ręczne wpisanie, w freight: **BRAK ŹRÓDŁA**.
- Produkcyjny korpus maili RFQ PL/DE z F1 i kosztem złej wagi/UN/LOCODE: **BRAK ŹRÓDŁA** (MaritimEmails = syntetyk).
- Kalibracja ETA **w TMS lądowym** (nie AIS morze, nie DoorDash blog): **BRAK ŹRÓDŁA** peer-review w tym audycie.
- Independent RCT Cursora po modelach późnego 2025 z CI poza zerem: METR zapowiedziało update 02.2026; **nie cytuję liczb**, których nie zweryfikowałem w paperze.

---

## 6. Mapowanie 1:1 na kontrakt

| Zasada OmniRoute | Co mówi pomiar / norma |
|---|---|
| LLM wyciąga, kod liczy | PAL 2023; LAVA 2025 C5 |
| HITL przed zapisem | DocILE residual error; Skitka commission; Goddard RR 1,26; art. 14 |
| `charge` = marża (jeden wiersz) | Brak paperu o tabeli `charge`; wniosek z PAL: model nie liczy spreadu |
| LLM nie scoruje JDG | Zał. III 5(b), motyw 58; JDG = natural person |
| Art. 50 label | Art. 50 ust. 1–2, 5; nie zastępuje HITL |

Koniec audytu.
