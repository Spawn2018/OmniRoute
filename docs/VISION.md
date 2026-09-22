# Wizja OmniRoute — dokument kanoniczny, żywy

```
status:        roboczy kanon
wersja:        0.7
ostatnia zmiana: 2026-09-16 01:00
```

## Jak czytać

Pięć części oryginalnego planu „Domknięcie badań i wizji”:

| Część | Plik |
|---|---|
| A — czym jest i dla kogo | ten plik, część A (kopia robocza: badania `08a`) |
| B — architektura i substrat | ten plik, część B (kopia robocza: badania `08b`) |
| C — inwentarz zakresu | ten plik, część C (kopia robocza: badania `08c`) |
| D — zakazy i granice AI | ten plik, część D (kopia robocza: badania `08d`) |
| E — roadmapa fal | ten plik, część E (kopia robocza: badania `08e`) |

Pełny tekst A–E zostaje też poniżej (jedno miejsce na czytanie ciągłe).
Egzekucja zapisu: `.cursor/rules/wizja-zywa.mdc` (alwaysApply).
Zrzuty obiektów Control Tower: badania `03-BENCHMARK-CONTROL-TOWER.md`
(B.1–B.10; skrót FourKites / Blue Yonder / Kinaxis w A.2). Benchmark TMS
top-10 (`04b`) — dump 2026-09-13 (A–H × 10; CargoWise / Qargo / interLAN
zostają w badaniach `04`).

## Dziennik zmian

| Data | Co |
|---|---|
| 2026-09-23 | **631.0** leftover 528 clone U1 carry HITL zamknięty: tabela `clone_carry_mark` z `carry_kind` carry|held|skip|other (`CONFIRMED`). Auto-copy U1, similar SQL i F2b Decimal nadal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-23 | **631.0** leftover 528 clone U1 carry HITL: tabela `clone_carry_mark` z `carry_kind` carry|held|skip|other (`REQUIREMENT`). Auto-copy U1, similar SQL i F2b Decimal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **630.0** D7c leftover synchro stance HITL zamknięty: tabela `pallet_synchro_mark` z `synchro_kind` aligned|drift|held|other (`CONFIRMED`). Auto-UPDATE salda, giełda live, FK UUID i kwota nadal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **630.0** D7c leftover synchro stance HITL: tabela `pallet_synchro_mark` z `synchro_kind` aligned|drift|held|other (`REQUIREMENT`). Auto-UPDATE salda, giełda live, FK UUID i kwota `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **629.0** D7c leftover ledger ruchu palet HITL zamknięty: tabela `pallet_ledger` z `delta_count` integer ze znakiem (`CONFIRMED`). Auto-UPDATE salda, giełda live i kwota nadal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **629.0** D7c leftover ledger ruchu palet HITL: tabela `pallet_ledger` z `delta_count` integer ze znakiem (`REQUIREMENT`). Auto-UPDATE salda, giełda live i kwota `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **628.0** T7 leftover daty bazowe HITL na `shipment` zamknięty: opcjonalne `etd` / `loading_date` / `unloading_date` / `invoice_date` (`CONFIRMED`). fx×FV SQL i mnożenie przy FV nadal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **628.0** T7 leftover daty bazowe HITL na `shipment`: opcjonalne `etd` / `loading_date` / `unloading_date` / `invoice_date` (`REQUIREMENT`). fx×FV SQL i mnożenie przy FV `REJECTED` w tym plasterze. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **627.0** D9f leftover `branding_ref` HITL na `document_template` zamknięty: opcjonalny snake wskazania marki (`CONFIRMED`). `output_kind` `pdf`/`zpl`, bajty i upload nadal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **627.0** D9f leftover `branding_ref` HITL na `document_template`: opcjonalny snake wskazania marki (`REQUIREMENT`). `output_kind` `pdf`/`zpl`, bajty i upload `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **626.0** D9c leftover katalog `network_print_requirement` zamknięty: kod + etykieta sieci + `source_ref` (`CONFIRMED`). HTTP 409, PDF i QR nadal `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **625.0** D5b leftover objętość na cenniku drobnicy: opcjonalne `volume_m3` Decimal, nie zmienia `chargeable_weight` ani `amount` (`REQUIREMENT`). Paleta i FSC `REJECTED` w tym plasterze. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **624.0** D4b leftover rodzaj dokumentu: `document_kind` `rod` obok `noted`|`attached`|`other` (`REQUIREMENT`). Token `pod` `REJECTED` — POD w słowniku to port wyładunku. Skan i bajty `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **623.0** D7d leftover saldo palet: `pallet_kind` `epal` obok `chep`|`lpr` (`REQUIREMENT`). Giełda, ledger ujemny i kind `euro` `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **622.0** U3 leftover cyfra kontrolna IATA: wklejony `mawb_no` w kształcie 3+8 cyfr, ostatnia = seria 7 cyfr modulo 7 (`REQUIREMENT`, IATA Resolution 600a). Token spoza kształtu, HAWB, pula M-03 i live IATA `REJECTED` w tym plasterze. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **621.0** D6c leftover pule HBL/MBL: `hbl_number_prefix`/`mbl_number_prefix` w M-03; `ocean_bill.bill_no` nullable; nadanie SQL `MAX`+1 (`REQUIREMENT`). D6b konsolidacja / PDF / live booking `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-22 | **620.0** U3 leftover e-rates air: `channel_quote.transport_mode` `air`\|`other`; przy `air` oba porty z `airport` (`REQUIREMENT`). Live IATA / cyfra kontrolna / druga tabela e-rate `REJECTED`. Marża zostaje na `charge` (`CONFIRMED`). |
| 2026-09-13 | Utworzenie 0.1 |
| 2026-09-13 | Rozbicie na 08a–e; Q1–Q13 wiążące (HC-04 L0–2/L3–5; FK plan_snapshot; nauka per tenant + SuperAdmin na całości; start HHL BR3.0/BR6.0/BR2.0; inwestorowi zero liczb skali) |
| 2026-09-13 | Scalenie do `docs/VISION.md`; AI0 = już w kodzie (072); `/noc` stop |
| 2026-09-13 | Reguła `.cursor/rules/wizja-zywa.mdc`: decyzje produktowe w tej samej turze do tego pliku |
| 2026-09-13 | Dump CT badania `03` B.1–B.3, B.7–B.10: Oracle buy/sell = antywzorzec; p44/LSP44 = dwa GTM, jeden OpenAPI; GTT+o9+Shippeo+e2open+Infor; auto-approve zakaz; luka `charge`/`benefit_ledger`. [WYCOFANE 2026-09-13: „B.4–B.6 nietknięte” — skrót w A.2]. [WYCOFANE 2026-09-13: „TMS `04b` nietknięte” — dump `04b` jest w kanonie]. |
| 2026-09-13 | Dump TMS top-10 badania `04b` (A–H × 10): druga marża REJECTED; Decimal CONFIRMED; AI-write MQ REJECTED; Oracle LML 95% jedyna publiczna metoda przedziału; WMS+BR6.2 evidenced; e2open≠CargoWise; Uber konflikt danych; CHR nie ISV; luka dwóch skór+RLS; KSeF/JPK/SENT nasze; leftover silniki HITL. 431.0 nie wynika z dziesiątki. |
| 2026-09-13 | [WYCOFANE] zdania „TMS `04b` w toku / nietknięte” — dump jest w kanonie |
| 2026-09-13 | Bramka publikacji: Cloudflare jako warstwa bezpieczeństwa przed ruchem publicznym (B.8). Nie plaster, nie `/noc`, nie AI0. [WYCOFANE 2026-09-13: „431.0 zostaje” jako next-ID — **431.0** jest w kodzie]. |
| 2026-09-13 | **433.0** `outcome_ledger` w kodzie. Następny = AI1.2 `counterfactual_run`. CRPS liczone = AI2. |
| 2026-09-13 | AI1.2 plan (**434.0**): HITL `counterfactual_run` etykiety. Silnik = AI4.1. |
| 2026-09-13 | **434.0** `counterfactual_run` w kodzie. Następny = AI1.3 `benefit_ledger`. |
| 2026-09-13 | AI1.3 plan (**435.0**): HITL `benefit_ledger` z metodą punktu odniesienia. Druga marża = zakaz. |
| 2026-09-13 | **435.0** `benefit_ledger` w kodzie. Następny = AI1.4 słowniki otwarte. |
| 2026-09-13 | AI1.4 plan (**436.0**): pierwszy słownik = HITL `suggestion_kind` bez CHECK. |
| 2026-09-13 | **436.0** `suggestion_kind` w kodzie. Następny = leftover `twin_kind`. |
| 2026-09-13 | AI1.4 plan (**437.0**): HITL `twin_kind` bez CHECK. twin_mark CHECK zostaje. |
| 2026-09-13 | **437.0** `twin_kind` w kodzie. Następny = leftover `autonomy_level`. `data_source` = AI5. |
| 2026-09-13 | AI1.4 plan (**438.0**): HITL `autonomy_level` bez CHECK i bez FK klienta. |
| 2026-09-13 | **438.0** `autonomy_level` w kodzie. Następny = leftover FK `suggestion_ledger`. |
| 2026-09-13 | AI1.4 plan (**439.0**): FK `suggestion_ledger` → `suggestion_kind`. twin_mark CHECK zostaje. |
| 2026-09-13 | **439.0** FK ledgeru w kodzie. Następny = leftover FK `twin_mark`. |
| 2026-09-13 | AI1.4 plan (**440.0**): FK `twin_mark` → `twin_kind`. outcome_kind CHECK zostaje. |
| 2026-09-13 | **440.0** FK `twin_mark` w kodzie. Następny = leftover `outcome_kind`. |
| 2026-09-13 | AI1.4 plan (**441.0**): HITL `outcome_kind` bez CHECK. outcome_ledger CHECK zostaje. |
| 2026-09-13 | **441.0** `outcome_kind` w kodzie. Następny = leftover FK `outcome_ledger`. |
| 2026-09-13 | AI1.4 plan (**442.0**): FK `outcome_ledger` → `outcome_kind`. CHECK listy `REJECTED`. Import `outcome_kinds` z ledgeru `REJECTED`. `data_source` = AI5. |
| 2026-09-13 | **442.0** FK `outcome_ledger` w kodzie (`CONFIRMED`, git). Następny = **AI2.0** CRPS (`REQUIREMENT`). `data_source` = AI5. |
| 2026-09-13 | AI2.0 plan (**443.0**): widok `interval_score` + funkcja SQL MAE/CRPS. Wpis `prediction_ledger` zostaje. Brier/AI2.1 = leftover. |
| 2026-09-13 | **443.0** `interval_score` w kodzie (`CONFIRMED`, git). Następny = **AI2.1** champion/dryf (`REQUIREMENT`). Brier zostaje leftover. |
| 2026-09-13 | AI2.1 plan (**444.0**): widok `version_score` średnie MAE/CRPS per `model_version`. Auto-champion i dryf = leftover. |
| 2026-09-13 | **444.0** `version_score` w kodzie (`CONFIRMED`, git). Następny = leftover dryf (**445.0**, `REQUIREMENT`). Auto-champion `REJECTED`. |
| 2026-09-13 | AI2.1 leftover plan (**445.0**): widok `version_window` średnie MAE/CRPS per `model_version` i dzień UTC z `created_at`. Detektor/próg i auto-champion = leftover. |
| 2026-09-13 | **445.0** `version_window` w kodzie (`CONFIRMED`, git). Następny = leftover wpisu metryki na `prediction_ledger` (**446.0**, `REQUIREMENT`). Detektor/próg `REJECTED`. Auto-champion `REJECTED`. |
| 2026-09-13 | AI2 leftover plan (**446.0**): `prediction_ledger` POST bez `crps`/`mae`; kolumny nullable. Metryka liczona = `interval_score`. Drop kolumn i kopia widoku `REJECTED`. |
| 2026-09-13 | **446.0** `prediction_ledger` bez wpisu metryki (`CONFIRMED`, git). Warunek AI2 „nie przyjmuje wpisanej metryki” spełniony na nowym INSERT. Następny = **AI3.0** PATCH szkicu (`REQUIREMENT`). Brier leftover (brak p). |
| 2026-09-13 | AI3.0 plan (**447.0**): `PATCH` `payload.candidates` na szkicu `pending`/`rate_line`. Wersja/bbox = AI3.1. Zapis `rate_line` z serwisu `REJECTED`. |
| 2026-09-13 | **447.0** `PATCH` kandydatów w kodzie (`CONFIRMED`, git). Następny = **AI3.1** wersja/`bbox`/pewność (`REQUIREMENT`). Zapis z modelu `REJECTED`. |
| 2026-09-13 | AI3.1 plan (**448.0**): `payload.revision` + `bbox_text` / `confidence_text`. Tabela historii `REJECTED`. Float `REJECTED`. |
| 2026-09-13 | **448.0** wersja/ramka/pewność w kodzie (`CONFIRMED`, git). Następny = **AI3.2** obraz wprost (`REQUIREMENT`). Historia wierszy leftover. |
| 2026-09-13 | AI3.2 plan (**449.0**): `extract_path` text|image jako etykieta. Live vision `REJECTED`. |
| 2026-09-13 | **449.0** `extract_path` w kodzie (`CONFIRMED`, git). Następny = **AI3.3** golden (`REQUIREMENT`). Live vision `REJECTED`. |
| 2026-09-13 | AI3.3 plan (**450.0**): własny golden + pytest. 96,6% / 92,71% = `TO_VERIFY` literatura, nie fakt Omni (`REJECTED` w kodzie). |
| 2026-09-13 | **450.0** golden w kodzie (`CONFIRMED`, git). Następny = **AI3.4** Excel (`REQUIREMENT`). 96,6% zostaje `TO_VERIFY`. |
| 2026-09-15 | AI3.3 leftover plan (**509.0**): golden ≥500 vs MockExtractor (`REQUIREMENT`). DocLayNet / 2k / 5k / live vision `REJECTED`. |
| 2026-09-15 | **509.0** golden ≥500 w kodzie (`CONFIRMED`, git). Następny = pętla 2 000 (`REQUIREMENT`). DocLayNet `REJECTED`. |
| 2026-09-15 | AI3.3 leftover plan (**510.0**): golden ≥2000 vs MockExtractor (`REQUIREMENT`). 5k / DocLayNet / live vision `REJECTED`. |
| 2026-09-15 | **510.0** golden ≥2000 w kodzie (`CONFIRMED`, git). Następny = pętla 5 000 (`REQUIREMENT`). DocLayNet `REJECTED`. |
| 2026-09-15 | AI3.3 leftover plan (**511.0**): golden ≥5000 vs MockExtractor (`REQUIREMENT`). DocLayNet / live vision `REJECTED`. |
| 2026-09-15 | **511.0** golden ≥5000 w kodzie (`CONFIRMED`, git). Następny = openpyxl AI3.4 leftover (`REQUIREMENT`). DocLayNet `REJECTED`. |
| 2026-09-15 | AI3.4 leftover plan (**512.0**): openpyxl na `.xlsx` (`REQUIREMENT`). Wcześniejszy `REJECTED` z 451.0 zdjęty dla leftoveru. Live vision `REJECTED`. |
| 2026-09-15 | **512.0** openpyxl w kodzie (`CONFIRMED`, git). Następny = Instructor CI leftover (`REQUIREMENT`). Live vision `REJECTED`. |
| 2026-09-15 | AI3 leftover plan (**513.0**): Instructor×golden stub bez sieci (`REQUIREMENT`). Żywy OpenAI / DocLayNet `REJECTED`. |
| 2026-09-15 | **513.0** Instructor×golden w kodzie (`CONFIRMED`, git). Następny = formuły bez cache (`REQUIREMENT`). Żywy OpenAI `REJECTED`. |
| 2026-09-15 | AI3.4 leftover plan (**514.0**): formuła bez cache jako tekst (`REQUIREMENT`). Ewaluacja `REJECTED`. |
| 2026-09-15 | **514.0** formuły bez cache w kodzie (`CONFIRMED`, git). Następny = undo historii (`REQUIREMENT`). Live vision `REJECTED`. |
| 2026-09-15 | AI3.1 leftover plan (**515.0**): undo ostatniego `payload.history` (`REQUIREMENT`). Undo do dowolnej rewizji `REJECTED`. |
| 2026-09-15 | **515.0** undo w kodzie (`CONFIRMED`, git). Następny = **AI7.0** (`REQUIREMENT`). Instructor wiring park. |
| 2026-09-15 | AI7.0 plan (**516.0**): HITL `allocation_key` (`REQUIREMENT`). SQL / TCM / druga marża / live ERP `REJECTED`. |
| 2026-09-15 | **516.0** `allocation_key` w kodzie (`CONFIRMED`, git). Następny = 6 kategorii leftover (`REQUIREMENT`). SQL/TCM park. |
| 2026-09-15 | AI7.0 leftover plan (**517.0**): HITL `cost_category_mark` 6 kategorii PDF (`REQUIREMENT`). SQL/TCM `REJECTED`. |
| 2026-09-15 | **517.0** `cost_category_mark` w kodzie (`CONFIRMED`, git). Następny = 12 poziomów leftover (`REQUIREMENT`). |
| 2026-09-15 | AI7.0 leftover plan (**518.0**): HITL `allocation_level` otwarty słownik (`REQUIREMENT`). SQL/TCM `REJECTED`. |
| 2026-09-15 | **518.0** `allocation_level` w kodzie (`CONFIRMED`, git). AI7 HITL substrat DONE. Następny = **AI6.0** (`REQUIREMENT`). SQL/TCM/AI7.1 park. |
| 2026-09-15 | AI6.0 plan (**519.0**): HITL `impact_node_mark` 8 węzłów kaskady (`REQUIREMENT`). SQL/EBITDA/edge `REJECTED`. |
| 2026-09-15 | **519.0** `impact_node_mark` w kodzie (`CONFIRMED`, git). Następny = edge leftover (`REQUIREMENT`). SQL/EBITDA park. |
| 2026-09-15 | AI6.0 leftover plan (**520.0**): HITL `impact_edge_mark` para from/to (`REQUIREMENT`). SQL/EBITDA/FK węzeł `REJECTED`. |
| 2026-09-15 | **520.0** `impact_edge_mark` w kodzie (`CONFIRMED`, git). AI6 HITL substrat DONE. Następny = **AI9.0** (`REQUIREMENT`). SQL/EBITDA park. |
| 2026-09-15 | AI9.0 plan (**521.0**): HITL `article50_mark` etykieta art. 50 (`REQUIREMENT`). U-art50 UI / scoring `REJECTED`. |
| 2026-09-15 | **521.0** `article50_mark` w kodzie (`CONFIRMED`, git). AI9.0 HITL DONE. Następny = **AI5.0** HITL `data_source` (`REQUIREMENT`). U-art50 UI / live ingest park. |
| 2026-09-15 | AI5.0 plan (**522.0**): HITL `data_source` z `license_label` + `rights_scope` (`REQUIREMENT`). Live ingest / CHECK listy licencji `REJECTED`. |
| 2026-09-15 | **522.0** `data_source` w kodzie (`CONFIRMED`, git). AI5.0 HITL slownik DONE. Następny = leftover bramy ingest (`REQUIREMENT`). Live ingest park. |
| 2026-09-15 | AI5.0 leftover plan (**523.0**): HITL `ingest_gate_mark` truth|owner|exception (`REQUIREMENT`). Live ingest `REJECTED`. |
| 2026-09-15 | **523.0** `ingest_gate_mark` w kodzie (`CONFIRMED`, git). Brama HITL DONE. Następny = **AI5.1** HITL cechy (`REQUIREMENT`). Live ingest / train park. |
| 2026-09-15 | AI5.1 plan (**524.0**): HITL `model_feature_mark` numeric|categorical|derived (`REQUIREMENT`). Live train / feature store `REJECTED`. |
| 2026-09-15 | **524.0** `model_feature_mark` w kodzie (`CONFIRMED`, git). AI5.1 HITL DONE. Następny = **AI7.1** HITL narracja CFO (`REQUIREMENT`). Live train / TCM park. |
| 2026-09-15 | AI7.1 plan (**525.0**): HITL `cfo_narrative_mark` anomaly|story|summary (`REQUIREMENT`). Silnik narracji / druga marża `REJECTED`. |
| 2026-09-15 | **525.0** `cfo_narrative_mark` w kodzie (`CONFIRMED`, git). AI7.1 HITL DONE. Następny = leftover KPI AI5 (`REQUIREMENT`). Silnik narracji / TCM park. |
| 2026-09-15 | AI5.0 leftover plan (**526.0**): HITL `kpi_definition_mark` otd|otif|custom (`REQUIREMENT`). Wzór KPI z modelu `REJECTED`. |
| 2026-09-15 | **526.0** `kpi_definition_mark` w kodzie (`CONFIRMED`, git). AI5.0 leftover KPI DONE. Następny = **N6** `margin_floor` (`REQUIREMENT`). Live ingest / wzór KPI park. |
| 2026-09-15 | N6 plan (**527.0**): HITL `margin_floor` Decimal + para UN/LOCODE (`REQUIREMENT`). 409 na charge / S11 `REJECTED` na tym wierszu. |
| 2026-09-16 | **527.0** `margin_floor` w kodzie (`CONFIRMED`, git). N6 HITL DONE. Następny = **N9** `shipment_clone_mark` (`REQUIREMENT`). 409/S11 leftover. |
| 2026-09-16 | N9 plan (**528.0**): HITL `shipment_clone_mark` last_similar|manual_pick|other (`REQUIREMENT`). Auto-copy / drugi SoR `REJECTED`. |
| 2026-09-16 | **528.0** `shipment_clone_mark` w kodzie (`CONFIRMED`, git). N9 HITL intencja DONE. Następny = **N11** handover SBAR (`REQUIREMENT`). Copy/U1 leftover. |
| 2026-09-16 | N11 plan (**529.0**): HITL `handover_sbar_mark` situation\|background\|assessment\|recommendation (`REQUIREMENT`). Drugi czat / auto SBAR z LLM `REJECTED`. |
| 2026-09-16 | **529.0** `handover_sbar_mark` w kodzie (`CONFIRMED`, git). N11 HITL DONE. Następny = **N2** `trip_bill_mark` (`REQUIREMENT`). Notatka S/B/A/R leftover. |
| 2026-09-16 | N2 plan (**530.0**): HITL `trip_bill_mark` ready\|held\|billed (`REQUIREMENT`). SQL trips×charge / F1 live `REJECTED` na tym wierszu. |
| 2026-09-16 | **530.0** `trip_bill_mark` w kodzie (`CONFIRMED`, git po push). N2 HITL DONE. Leftover SQL `trips_to_bill` · F1 live. Następny = **O6** carrier_quote HITL (`REQUIREMENT`). |
| 2026-09-16 | Plan **531.0** O6 leftover: HITL accept `carrier_quote` → `channel_quote` + inquiry `answered` (`REQUIREMENT`). 140.0 już ma kind+quote (`CONFIRMED`). ExtractionService zapis ofert `REJECTED`. Auto-accept / live HTTP / float / fuzzy match inquiry `REJECTED`. |
| 2026-09-16 | **531.0** O6 leftover w kodzie (`CONFIRMED`, git po push). Accept → `channel_quote` + opcjonalnie inquiry `answered`. Leftover `quote_recorded` przy accept. Następny = **O7** kraj ISO (`REQUIREMENT`). |
| 2026-09-16 | Plan **532.0** O7: filtr `country_code` na `GET …/networks/{id}/members` JOIN `party` (`REQUIREMENT`). UI 141.0 już filtruje w pamięci (`CONFIRMED`). Druga kolumna kraju / scrape / live HTTP `REJECTED`. |
| 2026-09-16 | **532.0** O7 w kodzie (`CONFIRMED`, git po push). API JOIN `party.country_code` + UI param. Leftover EXPLAIN. Następny = **O8** buy-desk (`REQUIREMENT`). |
| 2026-09-16 | **533.0** O8 buy-desk group-by + `table_view` w kodzie (`CONFIRMED`, git po push). Wątek = lane POL/POD. Nowy czat / rfc822 `REJECTED` na tym wierszu. Następny = park leftover O6 `quote_recorded` · SH-R16-12…15 (`REQUIREMENT`). |
| 2026-09-16 | **536.0** O8 leftover rfc822 na `inbound_message` w kodzie (`CONFIRMED`, git po push). Message-ID / In-Reply-To HITL. Live Graph fill / group-by buy-desk po rfc822 `REJECTED` na tym wierszu. Następny = **UXCL-L1** (`REQUIREMENT`). |
| 2026-09-16 | Plan **537.0** UXCL-L1: L0 privacy + allowlista istniejących `extraction_draft_*` (`REQUIREMENT`). Job#2 charge / replay / A/B `REJECTED`. |
| 2026-09-16 | **537.0** UXCL-L1 w kodzie (`CONFIRMED`, git po push). Allowlista extract-accept. Banner zgody / Job#2 `REJECTED` na tym wierszu. Następny = leftover O8 group-by `/mail` po rfc822 (`REQUIREMENT`). |
| 2026-09-16 | Plan **538.0**: `/mail` `group_by=thread` po `in_reply_to`/`rfc822_message_id` (`REQUIREMENT`). Buy-desk lane / live Graph `REJECTED`. |
| 2026-09-16 | **538.0** `/mail` thread group_by w kodzie (`CONFIRMED`, git po push). Buy-desk rfc822 / live Graph `REJECTED` na tym wierszu. Następny = park AI3-payload / Plat-HD / G0 (`REQUIREMENT`). |
| 2026-09-16 | Plan **539.0** N6 leftover: 409 gdy marża < `margin_floor` przy opcjonalnej parze UN/LOCODE na POST charge (`REQUIREMENT`). S11 / kolumna lane na charge `REJECTED`. |
| 2026-09-16 | **539.0** N6 409 w kodzie (`CONFIRMED`, git po push). Compose w API charges. Leftover S11. Następny = **N1** leftover FTL=1 409 (`REQUIREMENT`). |
| 2026-09-16 | Plan **540.0** N1 leftover: opcjonalne `load_kind=ftl` → 409 gdy zlecenie ma już przesyłkę (`REQUIREMENT`). Unique FTL w DB / kolumna na shipment `REJECTED`. |
| 2026-09-16 | **540.0** N1 FTL=1 409 w kodzie (`CONFIRMED`, git po push). Leftover D2b / `stop`. Następny = leftover D2b FK paczki albo park AI3-payload (`REQUIREMENT`). |
| 2026-09-17 | Plan **541.0** D2b: opcjonalny `consignment_id` na `shipment_package` (`REQUIREMENT`). Required FK / WMS / auto-link `REJECTED`. |
| 2026-09-17 | **541.0** D2b FK w kodzie (`CONFIRMED`, git po push). Leftover `stop` na consignment. Następny = leftover N1 `stop` albo park AI3-payload (`REQUIREMENT`). |
| 2026-09-17 | Plan **542.0** N1 leftover: opcjonalny `stop_id` na `consignment` + złożone FK (`REQUIREMENT`). Required stop / mapa / WMS `REJECTED`. |
| 2026-09-17 | **542.0** `stop_id` na consignment w kodzie (`CONFIRMED`, git po push). Leftover auto-link / mapa. Następny = park AI3-payload / Plat-HD / G0 (`REQUIREMENT`). |
| 2026-09-17 | Plan **543.0** N11 leftover: HITL `handover_note` z polami S/B/A/R (`REQUIREMENT`). Auto T6 / LLM / FK mark `REJECTED`. |
| 2026-09-17 | **543.0** `handover_note` w kodzie (`CONFIRMED`, git po push). Leftover T6 bind · N8. Następny = park AI3-payload / Plat-HD / G0 / N6 S11 (`REQUIREMENT`). |
| 2026-09-17 | Plan **544.0** N6 S11: pending `operator_decision` (`margin_floor`) przy breach + 409 z `decision_id`; override przez accepted `floor_decision_id` (`REQUIREMENT`). Auto charge na accept / usunięcie 409 `REJECTED`. |
| 2026-09-17 | **544.0** N6 S11 w kodzie (`CONFIRMED`, git po push). Leftover UI UN / matching / auto charge. Następny = park AI3-payload / Plat-HD / G0 (`REQUIREMENT`). |
| 2026-09-17 | Plan **545.0** Plat-HD-flow: HITL `product_ticket` title+body+kind (`REQUIREMENT`). Auto-fix / FK mark / Mob `REJECTED`. |
| 2026-09-17 | **545.0** `product_ticket` w kodzie (`CONFIRMED`, git po push). Leftover S11 owner · FK mark · Mob. Następny = park AI3-payload / G0 (`REQUIREMENT`). |
| 2026-09-17 | Plan **546.0** Plat-HD S11 owner: 409+decision przy `owner_ok` (`REQUIREMENT`). Auto-fix / Mob / FK mark `REJECTED`. |
| 2026-09-17 | **546.0** S11 owner na `product_ticket` w kodzie (`CONFIRMED`, git po push). Leftover FK mark · Mob · auto-fix. Następny = park AI3-payload / G0 (`REQUIREMENT`). |
| 2026-09-17 | Plan **547.0** N6 UI UN na `/charges` (`REQUIREMENT`). Matching / auto charge `REJECTED`. |
| 2026-09-17 | **547.0** pola UN + `floor_decision_id` na UI `/charges` (`CONFIRMED`, git po push). Leftover matching / auto charge. Następny = park AI3-payload / G0 (`REQUIREMENT`). |
| 2026-09-17 | Plan **548.0** N14 HITL `self_billing_mark` (`REQUIREMENT`). Live self-billing / JPK / FK party `REJECTED`. |
| 2026-09-17 | Plan **550.0** F10 leftover HITL `invoice_match_mark` (`REQUIREMENT`). `invoice_match_candidate` / ranking SQL / allocation `REJECTED` → leftover. |
| 2026-09-17 | **550.0** `invoice_match_mark` w kodzie (`CONFIRMED`, git po push). Leftover candidate / ranking / allocation. Następny = **551.0** `invoice_alloc_mark` (`REQUIREMENT`). |
| 2026-09-17 | Plan **551.0** F10 leftover HITL `invoice_alloc_mark` (`REQUIREMENT`). `purchase_invoice_allocation` z kwotą / ranking SQL `REJECTED` → leftover. |
| 2026-09-17 | **551.0** `invoice_alloc_mark` w kodzie (`CONFIRMED`, git po push). Leftover candidate / ranking / allocation z kwotą. Następny = **552.0** F11 `postal_dispatch_mark` (`REQUIREMENT`). |
| 2026-09-17 | Plan **552.0** F11 leftover HITL `postal_dispatch_mark` (`REQUIREMENT`). Live PP / `postal_epo` / e-Doręczenia `REJECTED` → leftover. |
| 2026-09-13 | AI3.4 plan (**451.0**): parser `xlsx_sheet` stdlib. `openpyxl` `REJECTED`. `.xls` leftover. |
| 2026-09-13 | **451.0** `xlsx_sheet` w kodzie (`CONFIRMED`, git). Następny = **AI4.0** FK `plan_snapshot` (`REQUIREMENT`). `.xls` leftover. |
| 2026-09-13 | AI4.0 plan (**452.0**): FK złożone RESTRICT. CASCADE `REJECTED`. What-if `REJECTED` na tym wierszu. |
| 2026-09-13 | **452.0** FK `plan_snapshot` w kodzie (`CONFIRMED`, git). Następny = **AI4.1** what-if (`REQUIREMENT`). CASCADE `REJECTED`. |
| 2026-09-13 | AI4.1 plan (**453.0**): FK `counterfactual_run` → `plan_snapshot` + widok SQL powtórki. Solver / AI4.2 `REJECTED` na tym wierszu. |
| 2026-09-13 | **453.0** FK przebieg + widok `what_if_replay` w kodzie (`CONFIRMED`, git). Następny = **AI4.2** kółka SQL (`REQUIREMENT`). Solver liczb `REJECTED` na tym wierszu. |
| 2026-09-13 | AI4.2 plan (**454.0**): widok SQL pary uzupełniającej `circle_sim`. Generator 500k / km / VRP `REJECTED` na tym wierszu. |
| 2026-09-13 | **454.0** widok `circle_sim_pair` w kodzie (`CONFIRMED`, git). Następny = **BR3.0** start HHL (`REQUIREMENT`). Generator 500k / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR3.0 plan (**455.0**): HITL `route_plan_mark`. Valhalla / LLM-VRP `REJECTED` na tym wierszu. |
| 2026-09-13 | **455.0** `route_plan_mark` w kodzie (`CONFIRMED`, git). Następny = **BR6.0** CRM ponad leada (`REQUIREMENT`). Valhalla / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR6.0 plan (**456.0**): HITL `crm_opportunity`. Activity / pipeline silnik `REJECTED` na tym wierszu. |
| 2026-09-13 | **456.0** `crm_opportunity` w kodzie (`CONFIRMED`, git). Następny = **BR2.0** pozycja (`REQUIREMENT`). Pipeline / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR2.0 plan (**457.0**): HITL `position_event`. Live GPS / lat-lng `REJECTED` na tym wierszu. |
| 2026-09-13 | **457.0** `position_event` w kodzie (`CONFIRMED`, git). Następny = **BR2.1** urządzenie (`REQUIREMENT`). Live GPS / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR2.1 plan (**458.0**): HITL `telematics_device`. Parowanie / live GPS `REJECTED` na tym wierszu. |
| 2026-09-13 | **458.0** `telematics_device` w kodzie (`CONFIRMED`, git). Następny = **BR2.2** zgoda (`REQUIREMENT`). Parowanie / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR2.2 plan (**459.0**): HITL `tracking_consent`. Kolumna na `party_contact` / live GPS `REJECTED` na tym wierszu. |
| 2026-09-13 | **459.0** `tracking_consent` w kodzie (`CONFIRMED`, git). Następny = **BR6.1** korytarz (`REQUIREMENT`). Expo BR2.3 / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR6.1 plan (**460.0**): HITL `sales_lane`. UN/LOCODE / pipeline / HubSpot live `REJECTED` na tym wierszu. |
| 2026-09-13 | **460.0** `sales_lane` w kodzie (`CONFIRMED`, git). Następny = **BR6.2** przetarg załadowcy (`REQUIREMENT`). Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR6.2 plan (**461.0**): HITL `shipper_tender_mark`. Druga tabela `tender` / auto-award / Alpega live `REJECTED` na tym wierszu. |
| 2026-09-13 | **461.0** `shipper_tender_mark` w kodzie (`CONFIRMED`, git). Następny = **BR6.5** marketing (`REQUIREMENT`). Expo BR6.3 / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR6.5 plan (**462.0**): HITL `campaign_mark`. Atrybucja live / klej do `funnel_mark` `REJECTED` na tym wierszu. |
| 2026-09-13 | **462.0** `campaign_mark` w kodzie (`CONFIRMED`, git). Następny = **BR3.2** dyspozytor drobnicy (`REQUIREMENT`). Atrybucja live / Expo BR6.3 / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR3.2 plan (**463.0**): HITL `groupage_dispatcher_mark`. Silnik hubów / klej do `groupage_line` `REJECTED` na tym wierszu. |
| 2026-09-13 | **463.0** `groupage_dispatcher_mark` w kodzie (`CONFIRMED`, git). Następny = **BR3.1** planowanie załadunku (`REQUIREMENT`). Silnik hubów / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR3.1 plan (**464.0**): HITL `load_order_mark`. Solver / wymiary Decimal / klej do `load_plan_mark` `REJECTED` na tym wierszu. |
| 2026-09-13 | **464.0** `load_order_mark` w kodzie (`CONFIRMED`, git). Następny = **BR3.3** tacho w planie (`REQUIREMENT`). Solver / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR3.3 plan (**465.0**): HITL `tacho_plan_mark`. Live DDD / solver godzin / klej do `tacho_office_mark` `REJECTED` na tym wierszu. |
| 2026-09-13 | **465.0** `tacho_plan_mark` w kodzie (`CONFIRMED`, git). Następny = **BR4.0** promy (`REQUIREMENT`). Live DDD / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR4.0 plan (**466.0**): HITL `ferry_booking_mark`. Live rezerwacja / solver art. 9 / klej do `ferry_art9_mark` `REJECTED` na tym wierszu. |
| 2026-09-13 | **466.0** `ferry_booking_mark` w kodzie (`CONFIRMED`, git). Następny = **BR4.1** OOG (`REQUIREMENT`). Live bilet / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR4.1 plan (**467.0**): HITL `oog_permit_mark`. Wymiary Decimal / live zezwolenie / klej do `oog_mark` `REJECTED` na tym wierszu. |
| 2026-09-13 | **467.0** `oog_permit_mark` w kodzie (`CONFIRMED`, git). Następny = **BR4.2** LCL (`REQUIREMENT`). Wymiary / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR4.2 plan (**468.0**): HITL `lcl_console_mark`. Live CFS / CBM / druga tabela LCL `REJECTED` na tym wierszu. |
| 2026-09-13 | **468.0** `lcl_console_mark` w kodzie (`CONFIRMED`, git). Następny = **BR4.3** NAC (`REQUIREMENT`). Live CFS / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-13 | BR4.3 plan (**469.0**): HITL `nac_mark`. Live NAC / FK do `shipment_stakeholder` / auto-send `REJECTED` na tym wierszu. |
| 2026-09-13 | **469.0** `nac_mark` w kodzie (`CONFIRMED`, git). Następny = **BR4.4** Jedwabny Szlak (`REQUIREMENT`). Live NAC / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-14 | BR4.4 plan (**470.0**): HITL `silk_corridor_mark`. Live CR Express / FK do `shipment_leg` / para UN/LOCODE `REJECTED` na tym wierszu. |
| 2026-09-14 | **470.0** `silk_corridor_mark` w kodzie (`CONFIRMED`, git). Następny = **BR5.0** faktoring (`REQUIREMENT`). Live CR Express / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-14 | BR5.0 plan (**471.0**): HITL `factoring_connector` (SMEO|other). Live SMEO HTTP / FK do `sales_invoice` / workflow wypłaty `REJECTED` na tym wierszu. |
| 2026-09-14 | **471.0** `factoring_connector` w kodzie (`CONFIRMED`, git). Następny = **BR5.1** PO Financing (`REQUIREMENT`). Live SMEO HTTP / Expo / AI5 `REJECTED` na tym wierszu. |
| 2026-09-14 | BR5.1 plan (**472.0**): HITL `po_financing_mark`. FK do `purchase_order` / wycena zapasu BR1.2 / live partner HTTP `REJECTED` na tym wierszu. |
| 2026-09-14 | **472.0** `po_financing_mark` w kodzie (`CONFIRMED`, git). Następny = **BR5.2** giełdy transportowe (`REQUIREMENT`). Live partner HTTP / FK PO / Expo `REJECTED` na tym wierszu. |
| 2026-09-14 | BR5.2 plan (**473.0**): rozszerzenie CHECK `exchange_connector.system_kind` (timocom|teleroute|transporeon|other). Live HTTP / auto-post / nowa tabela `REJECTED` na tym wierszu. |
| 2026-09-14 | **473.0** CHECK `exchange_connector` rozszerzony (`CONFIRMED`, git). Fala BR pin do BR5.2 zamknięta. Live giełda HTTP / wymiana ofert `REJECTED` na tym wierszu. |
| 2026-09-14 | BR1.0 plan (**474.0**): HITL `wms_flow_mark` (receipt|location|pick|ship|count|other). Live WMS HTTP / RFID / qty / FK bin `REJECTED` na tym wierszu. |
| 2026-09-14 | **474.0** `wms_flow_mark` w kodzie (`CONFIRMED`, git). Następny = **BR1.1** RFID (`REQUIREMENT`). Live WMS HTTP / qty `REJECTED` na tym wierszu. |
| 2026-09-14 | BR1.1 plan (**475.0**): HITL `rfid_mark` (reader|gate|tag|other). Live RFID HTTP / EPC / FK bin `REJECTED` na tym wierszu. |
| 2026-09-14 | **475.0** `rfid_mark` w kodzie (`CONFIRMED`, git). Następny = **BR1.2** Inventory Release (`REQUIREMENT`). Live RFID poll `REJECTED` na tym wierszu. |
| 2026-09-14 | BR1.2 plan (**476.0**): HITL `inventory_finance_mark` (valuation|aging|release|other). Wycena SQL / wartość Decimal / FK position·PO / live zastaw `REJECTED` na tym wierszu. |
| 2026-09-14 | **476.0** `inventory_finance_mark` w kodzie (`CONFIRMED`, git). Następny = **BR1.3** zabezpieczenie na towarze (`REQUIREMENT`). Wycena SQL `REJECTED` na tym wierszu. |
| 2026-09-14 | BR1.3 plan (**477.0**): HITL `inventory_collateral_mark` (pledge|lien|hold|other). FK position·PO / live zastaw / wartość `REJECTED` na tym wierszu. |
| 2026-09-15 | **504.0** partial accept `candidate_indexes` w kodzie (`CONFIRMED`, git). Reszta pending. Następny = M-03 `hitl_confidence_*` (`REQUIREMENT`). Quote/RFP partial / auto-accept / Instructor / live vision `REJECTED`. |
| 2026-09-15 | Plan **504.0** AI3.0 leftover partial write przy accept (`REQUIREMENT`). Indeksy kandydatów; reszta pending. Quote/RFP partial / auto-accept / Instructor / live vision `REJECTED`. |
| 2026-09-15 | **503.0** `payload.history` w kodzie (`CONFIRMED`, git). Snapshot przy PATCH. Następny = AI3.0 leftover partial write (`REQUIREMENT`). Tabela historii / undo / Instructor / live vision `REJECTED`. |
| 2026-09-15 | Plan **503.0** AI3.1 leftover historia wierszy w `payload.history` JSONB (`REQUIREMENT`). Snapshot przy PATCH. Tabela historii / undo / Instructor / live vision `REJECTED`. |
| 2026-09-15 | **502.0** `extraction_prompt_mark` w kodzie (`CONFIRMED`, git). Prompt jako dana HITL. Następny = historia JSONB leftover (`REQUIREMENT`). Wiring LLM / tabela historii / live vision `REJECTED`. |
| 2026-09-15 | Plan **502.0** AI3.1 leftover `extraction_prompt_mark` (`REQUIREMENT`). Prompt jako dana HITL; nie wiring LLM. Tabela historii `REJECTED` (jak 448.0). Live vision `REJECTED`. |
| 2026-09-15 | **501.0** brama 70% accept zbiorczy w kodzie (`CONFIRMED`, git). Decimal na `confidence_text`; ≥2 kandydatów. Następny = AI3.1 leftover historia/prompt (`REQUIREMENT`). Auto-accept / float / partial write / live vision `REJECTED`. |
| 2026-09-15 | Plan **501.0** AI3.0 leftover brama 70% przed accept zbiorczym (`REQUIREMENT`). Decimal 0,70 w domenie na `confidence_text`; ≥2 kandydatów. Auto-accept / float / partial write / live vision `REJECTED` na tym wierszu. |
| 2026-09-15 | **500.0** PATCH `candidates` dla `carrier_quote`/`tender_rfp` w kodzie (`CONFIRMED`, git). Nazwy `quotation`/`customer_rfq` = błędny skrót planu (`REJECTED`). Następny = AI3.0 leftover próg 70% (`REQUIREMENT`). Vision live `REJECTED`. |
| 2026-09-15 | Plan **500.0** AI3.0 leftover PATCH `carrier_quote`/`tender_rfp` (`REQUIREMENT`). Próg 70% / vision `REJECTED` na tym wierszu. |
| 2026-09-15 | **499.0** `shipper_award_mark` w kodzie (`CONFIRMED`, git). Fala BR6.2 HITL domknięta; Alpega / auto-award SQL `REJECTED`. Następny = AI3.0 leftover PATCH quote/rfq (`REQUIREMENT`). |
| 2026-09-15 | Plan **499.0** BR6.2 leftover `shipper_award_mark` (`REQUIREMENT`). Stance go/hold/no_award; nie auto-award SQL. Alpega live `REJECTED`. |
| 2026-09-15 | **498.0** `shipper_bind_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.2 auto-award stance (`REQUIREMENT`). Alpega live `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **498.0** BR6.2 leftover `shipper_bind_mark` (`REQUIREMENT`). Stance tender/party; nie FK UUID. Alpega live / auto-award `REJECTED`. |
| 2026-09-15 | **497.0** `sales_bind_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.2 FK stance (`REQUIREMENT`). HubSpot / Alpega live `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **497.0** BR6.1 leftover `sales_bind_mark` (`REQUIREMENT`). Stance opportunity/party; nie FK UUID. HubSpot live `REJECTED`. |
| 2026-09-15 | **496.0** `crm_link_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.1 FK stance (`REQUIREMENT`). Cold-send / HubSpot live `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **496.0** BR6.0 leftover `crm_link_mark` (`REQUIREMENT`). Stance lead/party; nie FK UUID. Cold-send / merge `REJECTED`. |
| 2026-09-15 | **495.0** `crm_dedup_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.0 FK stance (`REQUIREMENT`). Cold-send / merge SQL `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **495.0** BR6.0 leftover `crm_dedup_mark` (`REQUIREMENT`). Stance nip/vat/email; nie merge SQL. Cold-send / FK `REJECTED`. |
| 2026-09-15 | **494.0** `shipper_like_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.0 dedup (`REQUIREMENT`). Alpega live / SQL `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **494.0** BR6.2 leftover `shipper_like_mark` (`REQUIREMENT`). Stance match/gap/bench; nie SQL. Alpega / FK `REJECTED`. |
| 2026-09-15 | **493.0** `shipper_round_mark` w kodzie (`CONFIRMED`, git). Następny = leftover like-for-like (`REQUIREMENT`). Alpega live / FK / SQL `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **493.0** BR6.2 leftover `shipper_round_mark` (`REQUIREMENT`). Runda first/second/final; nie Alpega. FK / like-for-like SQL `REJECTED`. |
| 2026-09-15 | **492.0** `volume_label` na `sales_lane` (`CONFIRMED`, git). Następny = leftover BR6.2 rundy (`REQUIREMENT`). HubSpot live / float / FK `REJECTED` na tym wierszu. |
| 2026-09-15 | **491.0** para UN/LOCODE na `sales_lane` (`CONFIRMED`, git). Następny = leftover wolumen (`REQUIREMENT`). FK port / HubSpot / km `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **491.0** BR6.1 leftover para UN/LOCODE na `sales_lane` (`REQUIREMENT`). Nie FK port. HubSpot / km `REJECTED`. |
| 2026-09-15 | **490.0** `crm_pipeline_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.1 UN/LOCODE na `sales_lane` (`REQUIREMENT`). FK lead/opportunity/activity/party `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **490.0** BR6.0 leftover `crm_pipeline_mark` (`REQUIREMENT`). Rodzaj stage/won/lost/hold; nie silnik lejka. FK lead/opportunity/activity/party `REJECTED`. |
| 2026-09-15 | **489.0** `crm_activity` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.0 etap (`REQUIREMENT`). FK lead/opportunity / cold-send `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **489.0** BR6.0 leftover `crm_activity` (`REQUIREMENT`). Rodzaj call/meeting/email/note; nie pipeline. FK lead/opportunity / cold-send `REJECTED`. |
| 2026-09-15 | **488.0** `compliance_program_mark` w kodzie (`CONFIRMED`, git). Następny = leftover BR6.0 activity (`REQUIREMENT`). PDF bytes / U-art50 `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **488.0** AI9.2 leftover `compliance_program_mark` (`REQUIREMENT`). Stancja draft/review/signed/exempt; nie PDF bytes. U-art50 / L3 write `REJECTED`. |
| 2026-09-15 | **487.0** `field_confidence_mark` w kodzie (`CONFIRMED`, git). Następny = leftover AI9.2 program PDF (`REQUIREMENT`). Przebudowa ui-04 / float auto-accept `REJECTED` na tym wierszu. |
| 2026-09-15 | Plan **487.0** AI9.1 leftover `field_confidence_mark` (`REQUIREMENT`). Pasma green/yellow/orange/hold; nie przebudowa ui-04. Float / auto-accept `REJECTED`. |
| 2026-09-14 | **486.0** `quality_descent_mark` w kodzie (`CONFIRMED`, git). Następny = leftover ui-04 pewność per pole (`REQUIREMENT`). Silnik auto-zejścia / L3 write / MAE SQL `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **486.0** leftover AI8.2 `quality_descent_mark` (`REQUIREMENT`). Powód zejścia jakości (mae/crps/brier/manual) jako HITL; nie silnik auto-zejścia. L3 write / MAE SQL / scoring osoby `REJECTED` na tym wierszu. |
| 2026-09-14 | **485.0** `style_fidelity_mark` w kodzie (`CONFIRMED`, git). Następny = leftover auto-zejście jakości L3 (`REQUIREMENT`). Score SQL/LLM / scoring osoby / auto-block mail `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **485.0** AI8.1 `style_fidelity_mark` (`REQUIREMENT`). Stancja bramki fidelity jako HITL (pass/hold/reject/exempt); nie wyliczanie 85%. Score SQL/LLM / scoring osoby / auto-block mail `REJECTED` na tym wierszu. |
| 2026-09-14 | **484.0** `style_cascade_mark` w kodzie (`CONFIRMED`, git). Następny = **AI8.1** STYLE FIDELITY leftover (`REQUIREMENT`). Scoring osoby / silnik stylu / FK party `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **484.0** AI8.0 `style_cascade_mark` (`REQUIREMENT`). Kaskada Global→…→Context jako HITL katalog poziomów; nie silnik stylu. STYLE FIDELITY / scoring osoby / FK party `REJECTED` na tym wierszu. |
| 2026-09-14 | **483.0** `l3_gate_mark` w kodzie (`CONFIRMED`, git). Następny = **AI8.0** kaskada stylu leftover (`REQUIREMENT`). L3 write / scoring Pain×Frequency / Bertha `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **483.0** AI8.2 `l3_gate_mark` (`REQUIREMENT`). Checklista bramy L3 (SoT/owner/exception/rollback/blast) jako HITL, nie silnik. L3 write / scoring Pain×Frequency / Bertha `REJECTED` na tym wierszu. SOP agenta = how-to 1 strona. |
| 2026-09-14 | **482.0** `automation_bias_mark` w kodzie (`CONFIRMED`, git). Następny = **AI8.2** brama L3 leftover (`REQUIREMENT`). ui-04 przebudowa / auto-accept `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **482.0** AI9.1 `automation_bias_mark` (`REQUIREMENT`). U-art50 / ui-04 przebudowa `REJECTED` na tym wierszu. Scoring / auto-accept `REJECTED`. |
| 2026-09-14 | **481.0** `risk_register_mark` w kodzie (`CONFIRMED`, git). Następny = **AI9.1** automation bias (`REQUIREMENT`). Scoring osoby / L3 silnik `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **481.0** AI9.2 `risk_register_mark` (`REQUIREMENT`). Mob Expo park. Scoring osoby / L3 silnik `REJECTED` na tym wierszu. U-art50 UI zostaje. |
| 2026-09-14 | **480.0** `product_ticket_mark` w kodzie (`CONFIRMED`, git). Następny = **Mob** park → **AI9.2** (`REQUIREMENT`). CAPA / auto-fix `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **480.0** Plat-HD `product_ticket_mark` (`REQUIREMENT`). CAPA / `operator_notice` / auto-fix `REJECTED` na tym wierszu. Leftover workflow naprawy · Mob. |
| 2026-09-14 | **479.0** `line_impact_layer_mark` w kodzie (`CONFIRMED`, git). Następny = **Plat-HD** (`REQUIREMENT`). SQL/EBITDA leftover. Silnik w Pythonie `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **479.0** BR7.1 `line_impact_layer_mark` (`REQUIREMENT`). `line_impact_mark` zostaje. SQL/EBITDA leftover. Silnik w Pythonie `REJECTED` na tym wierszu. |
| 2026-09-14 | **478.0** `ops_room_mark` w kodzie (`CONFIRMED`, git). Następny = **BR7.1** wpływ na linię (`REQUIREMENT`). N8 / widok sklejony / T8 live leftover. Drugi czat `REJECTED` na tym wierszu. |
| 2026-09-14 | Plan **478.0** BR7.0 `ops_room_mark` (`REQUIREMENT`). `war_room_mark` zostaje. N8 / widok sklejony / T8 live leftover. Drugi czat `REJECTED` na tym wierszu. |
| 2026-09-14 | **477.0** `inventory_collateral_mark` w kodzie (`CONFIRMED`, git). Następny = **BR7.0** sala operacyjna (`REQUIREMENT`). Live zastaw `REJECTED` na tym wierszu. |
| 2026-09-13 | C.3 **Grupa 8**: help desk produktu (ticket → agent → akceptacja właściciela) + mobile całego OmniRoute. Leftover PLAN **Plat-HD** / **Mob**. Nie 468.0. |
| 2026-09-13 | D.7 readiness (Murphy 2026 + audyt PDF/czat): Three-Bucket, Definition Gap, szwy eskalacji = leftover. Mission Control / wektor / druga warstwa semantyczna / Bertha `REJECTED`. |
| 2026-09-13 | Ciało C.3 Grupa 8 + D.7 + skrót `03` B.4–B.6 w A.2. E.3: HC-04 i FK `plan_snapshot` zamknięte. [WYCOFANE 2026-09-13: „B.4–B.6 nietknięte w dumpie” — skrót jest w kanonie]. |
| 2026-09-13 | D.7: pięć jobów z audytu GPT jako leftover (definicja KPI per strona; brama L3; SOP agenta; ulga nie sens; promień wybuchu). Nie nowy BC. Nie 468.0. |
| 2026-09-13 | D.8: badania ≠ drugi kanon. C.4 mapa leftover. AI3 leftover z `07`. C.3 Grupa 6: `crm_opportunity` jest. E.3 Q11 zamknięte. Nie 468.0. |
| 2026-09-16 | D.8: przy `/noc` busy badania = schowek pomysłów/wizji (`REQUIREMENT`). Przy idle/stop praca = repo OmniRoute + GitHub (`REQUIREMENT`). Badania nadal ≠ drugi kanon (`CONFIRMED`). Nie 527.0 z tej karty. |
| 2026-09-16 | D.8: badania = surowiec na nowe plany/kanony/agentów/kontrakty w repo — **tylko** po stopie `/noc` **i** jawnym poleceniu człowieka (`REQUIREMENT`). Sam idle ≠ promocja. [WYCOFANE 2026-09-16: „idle = przenieś pakiet SH do repo”.] |
| 2026-09-16 | **Rejestr wdrożenia 16 IX:** 20 plików badań → kanon kolejki [rejestr-wdrozenia-16-ix.md](ops/rejestr-wdrozenia-16-ix.md) + PLAN § Fala SH-R16 (`REQUIREMENT` operatora: 100% pokrycie; park z warunkiem). Pin 2026-09-08c bez zmian. Nie AI0. |
| 2026-09-16 | SH-R16 audyt braków → szablony 29/29, false DONE naprawione, materialne w PLAN (SH-R16-8…15). (`REQUIREMENT`) |

---

# Wizja OmniRoute — dokument kanoniczny, żywy

```
status:        roboczy kanon (zastępuje "Informacje z claude/vision.md" z 2026-08-29)
wersja:        0.1
utworzony:     2026-09-13
ostatnia zmiana: 2026-09-16 01:00
autor ustaleń: Sebastian Bożek (właściciel produktu)
redakcja:      agent, na podstawie dokumentów 01-07 i 09-11 w tym katalogu
lokalizacja:   docs/VISION.md (repozytorium OmniRoute)
```

---

## Jak czytać ten dokument i jak go aktualizować

Ten plik jest **żywy**. Ma być aktualizowany za każdym razem, gdy pojawi się nowe
ustalenie — nie przepisywany od zera i nie duplikowany w nowy plik z sufiksem `-v2`.

**Zasady aktualizacji, obowiązujące każdego, kto go dotknie:**

1. **Nowe ustalenie dopisujesz w odpowiedniej części i dodajesz wiersz w Dzienniku zmian.**
   Bez wiersza w dzienniku zmiana nie istnieje.
2. **Nie usuwasz starego ustalenia w ciszy.** Jeśli coś przestaje obowiązywać, zostaje
   w tekście z adnotacją `[WYCOFANE 2026-MM-DD: powód]`. To jedyny sposób, żeby nie
   powtórzyła się historia `vision.md`, który przez piętnaście dni pokazywał wizję
   unieważnioną przez właściciela, bo nikt nie odnotował korekty.
3. **Każde twierdzenie ma jeden z czterech statusów.** `CONFIRMED` — potwierdzone
   dosłownym zapisem ustalenia właściciela albo kodem w repozytorium. `REQUIREMENT` —
   wymóg właściciela, jeszcze nie zaprojektowany. `TO_VERIFY` — prawdopodobne, bez
   potwierdzenia. `REJECTED` — świadomie odrzucone, zostaje jako ostrzeżenie przed
   ponownym wracaniem do tematu.
4. **Liczby zawsze z metodą i źródłem.** Liczba bez metody pomiaru jest sloganem
   i do tego dokumentu nie wchodzi. Jeśli źródłem jest materiał marketingowy dostawcy,
   musi to być napisane wprost przy liczbie.
5. **Czego tu nie ma:** kodu, nazw kolumn wymyślonych „na przyszłość", terminów
   kalendarzowych. Terminy i kolejka zadań żyją w `docs/PLAN-REALIZACJA.md`
   w repozytorium; ten dokument mówi **co i dlaczego**, nie **kiedy**.
6. **Reguła agenta:** `.cursor/rules/wizja-zywa.mdc` (alwaysApply). Rozmowa o
   rozbudowie, funkcjach, architekturze, działaniu, UI, modułach, zakresie,
   GTM zmieniającym produkt, autonomii, bliźniakach albo zakazach AI — zapis
   w tej samej turze. Nie zrzut czatu. Nie plaster z wizji. `/noc` czyta
   CURRENT + PLAN § Kolejka, nie ten plik jako next-ID.

**Relacja do repozytorium.** Kanon jest **jeden**: `docs/VISION.md`. Nie forkuje
się trzeciej wizji. Rozbicie A–E (`08a`–`08e`) i `08-WIZJA-OMNIROUTE.md` w
`D:\OMNIROUTE-badania` to kopia robocza — ruszasz ją tylko gdy już edytujesz
badania, i wtedy synchronizujesz **z** kanonu, nie odwrotnie.
`Informacje z claude/vision.md` z 29 VIII jest zastąpiony — nie ładuj archiwum
do kontekstu.
Pełne zrzuty pól i zdarzeń Control Tower żyją w badaniach `03` (nie w tym pliku).
TMS `04b` — dump 2026-09-13 (A–H × 10; CargoWise / Qargo / interLAN w `04`).

---

## Dziennik zmian

| Data | Co się zmieniło | Źródło ustalenia |
|---|---|---|
| 2026-09-13 | Dokument utworzony. Skonsolidowano ustalenia z historii czatów (2026-08-29 → 2026-09-13), ośmiu canvasów, czterech PDF-ów, dziewięciu plików tekstowych, prezentacji handlowej i audytu kodu. | dokumenty `01`–`07`, `09`–`11` w tym katalogu |
| 2026-09-13 | Dziesięć decyzji wiążących właściciela zapisanych jako kanon (część A.3, B.4, D.2). | prompt właściciela 2026-09-13 + odpowiedzi na pytania |
| 2026-09-13 | Dodano część C.3 — brakujące moduły. Powód: właściciel wskazał wprost, że plan budowy musi objąć to, czego dziś się nie buduje. | polecenie właściciela 2026-09-13 |
| 2026-09-13 | Wskazano regułę `.cursor/rules/wizja-zywa.mdc`. Kanon = ten plik, nie trzecia kopia. | polecenie właściciela 2026-09-13 |
| 2026-09-13 | Dump Control Tower (badania `03` B.1–B.3, B.7–B.10): antypattern Oracle buy/sell; p44/LSP44 jeden OpenAPI dwa GTM; trójka PLANNED/ACTUAL/ESTIMATE; zakaz float geo; GTT model+tolerance; wzorzec benchu o9 cuOpt; Shippeo Triple SLA bez claimu liczb; Shippeo≠Overhaul; e2open=WiseTech; Infor sieć ≠ RLS; auto-approve zakaz; luka `charge`+`benefit_ledger` u siódemki. [WYCOFANE 2026-09-13: „B.4–B.6 nietknięte” — skrót w A.2]. [WYCOFANE 2026-09-13: „TMS `04b` nadal w toku” — dump `04b` jest w kanonie]. | public docs w `03`; decyzje Omni = `REQUIREMENT` / `REJECTED` / `CONFIRMED` w A–E |
| 2026-09-13 | Dump TMS top-10 (badania `04b`, A–H × 10 poza CargoWise/Qargo/interLAN): klon drugiej marży REJECTED (SAP `Profitability` na FWO; Oracle `Job.Profit` + osobne buy/sell shipments; Shipwell `customer_charge_line_items` + `vendor_charge_line_items` + `markup`); JSON `number` / integer cents ≠ Decimal HC; AI-write bo MQ ma (Shipwell Swifty/MCP, Uber 30+ agents, SAP calc on save) REJECTED; Oracle LML 95% `Prediction Low/High` = jedyna publiczna metoda przedziału, nie CRPS/MAE; Fala BR WMS evidenced (Manhattan Active TM+WMS+Yard+Labour; Infios Archer OMS/WMS/TMS; SAP EWM); BR6.2 = Alpega TenderEasy + Freight Bench (multi-round, like-for-like, spot; nie auto-award); e2open ≠ CargoWise (close 03.08.2025, „very little product overlap”); Uber Freight konflikt osi danych HHL; CHR Navisphere nie ISV; żaden z 10 nie sprzedaje dwóch skór TSL+Watch Tower + Postgres RLS; KSeF/JPK/SENT nie publiczne; leftover silniki (VSR, LML, Optimizer, Archer, what-if) zostają HITL + `suggestion_ledger` (AI1.0 po 431.0). 431.0 `quote_validity_mark` nie wynika z tej dziesiątki. | public docs w `04b`; decyzje Omni = `REQUIREMENT` / `REJECTED` / `CONFIRMED` w A–E |
| 2026-09-13 | Bramka publikacji: Cloudflare jako warstwa bezpieczeństwa (DNS + proxy, TLS Full/strict, HSTS, WAF, rate limit, Access) **zanim** SPA operatora jest publiczna. Nie marketing CDN. Nie zastępuje RLS/HITL/Auth0 I1/I2. Nie plaster `/noc`. 431.0 zostaje. | polecenie właściciela 2026-09-13; stan repo `CONFIRMED`; limity planów = public docs Cloudflare (cytowane w B.8), nie nasz cennik |
| 2026-09-13 | Leftover EXP1 katalogów quotation zamknięty: **431.0** `quote_validity_mark` w kodzie (`CONFIRMED`, git). Następny = **AI1.0** `suggestion_ledger` (`REQUIREMENT`, PLAN Fala AI). Kolumny `valid_until` / `revision_no` / `supersedes_id` na `quotation` zostają leftover (`REQUIREMENT`). | CURRENT + plaster 431.0 `/noc` |
| 2026-09-13 | AI1.0 pierwszy plaster (**432.0**) = HITL `suggestion_ledger` append-only: przedział Decimal + `reaction` + `changed_to`. Zapis z modelu na L0–2 `REJECTED` (HC-04). `outcome_ledger` / słowniki AI1.4 / trzy BC autosave = leftover fali (`REQUIREMENT`). Nie klon `prediction_ledger` ani `operator_decision`. | `/plan-modul` `/noc`; VISION B.2 + HC-04 |
| 2026-09-13 | **432.0** `suggestion_ledger` w kodzie (`CONFIRMED`, git). Następny = **AI1.1** `outcome_ledger` (`REQUIREMENT`). Zapis LLM / CRPS liczone / FK encji zostają `REJECTED` na tym wierszu. | CURRENT + plaster 432.0 `/noc` |
| 2026-09-13 | AI1.1 (**433.0**) = HITL `outcome_ledger`: `actual_value` Decimal + UUID podpowiedzi jako dana. CRPS/MAE liczone `REJECTED` (AI2). FK do `suggestion_ledger` `REJECTED`. | `/plan-modul` `/noc`; VISION B.2 |
| 2026-09-13 | **433.0** `outcome_ledger` w kodzie (`CONFIRMED`, git). Następny = **AI1.2** `counterfactual_run` (`REQUIREMENT`). CRPS liczone / FK do podpowiedzi zostają `REJECTED` na tym wierszu. | CURRENT + plaster 433.0 `/noc` |
| 2026-09-13 | AI1.2 (**434.0**) = HITL `counterfactual_run`: `run_code` + etykiety baseline / dźwigni / wyniku. Silnik what-if `REJECTED` (AI4.1). Kwota oszczędności `REJECTED` (AI1.3). Nie klon `what_if_mark` / `plan_snapshot`. | `/plan-modul` `/noc`; VISION B.2 |
| 2026-09-13 | **434.0** `counterfactual_run` w kodzie (`CONFIRMED`, git). Następny = **AI1.3** `benefit_ledger` (`REQUIREMENT`). Silnik what-if zostaje `REJECTED` na tym wierszu. | CURRENT + plaster 434.0 `/noc` |
| 2026-09-13 | AI1.3 (**435.0**) = HITL `benefit_ledger`: `method_label` + `hours_saved` + `saved_amount` Decimal. Druga marża `REJECTED`. Liczenie z `charge` `REJECTED`. | `/plan-modul` `/noc`; VISION B.2 |
| 2026-09-13 | **435.0** `benefit_ledger` w kodzie (`CONFIRMED`, git). Następny = **AI1.4** słowniki (`REQUIREMENT`). Druga marża i SQL z `charge` zostają `REJECTED` na tym wierszu. | CURRENT + plaster 435.0 `/noc` |
| 2026-09-13 | AI1.4 (**436.0**) = HITL `suggestion_kind`: `kind_code` bez CHECK/ENUM. `twin_kind` / `data_source` / `autonomy_level` leftover. FK z `suggestion_ledger` `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION B.3 |
| 2026-09-13 | **436.0** `suggestion_kind` w kodzie (`CONFIRMED`, git). Następny = **twin_kind** słownik (`REQUIREMENT`, C.2). CHECK na `suggestion_ledger` zostaje `REJECTED` na tym wierszu. | CURRENT + plaster 436.0 `/noc` |
| 2026-09-13 | AI1.4 (**437.0**) = HITL `twin_kind`: `kind_code` bez CHECK/ENUM. Zmiana `twin_mark` `REJECTED`. `data_source` / `autonomy_level` leftover. | `/plan-modul` `/noc`; VISION C.2 |
| 2026-09-13 | **437.0** `twin_kind` w kodzie (`CONFIRMED`, git). Następny = **autonomy_level** (`REQUIREMENT`, B.3). `data_source` = AI5 (`REQUIREMENT`). CHECK na `twin_mark` zostaje `REJECTED` na tym wierszu. | CURRENT + plaster 437.0 `/noc` |
| 2026-09-13 | AI1.4 (**438.0**) = HITL `autonomy_level`: `level_code` bez CHECK/ENUM. FK `party` `REJECTED`. `data_source` leftover AI5. Silnik L3+ `REJECTED`. | `/plan-modul` `/noc`; VISION B.3 · B.4 |
| 2026-09-13 | **438.0** `autonomy_level` w kodzie (`CONFIRMED`, git). Następny = FK `suggestion_ledger` (`REQUIREMENT`, B.3). `data_source` = AI5. CRPS `REJECTED` na tym wierszu. | CURRENT + plaster 438.0 `/noc` |
| 2026-09-13 | AI1.4 (**439.0**) = FK `(organization_id, suggestion_kind)` → słownik. CHECK listy `REJECTED`. Import `suggestion_kinds` z ledgeru `REJECTED`. `twin_mark` CHECK zostaje. | `/plan-modul` `/noc`; VISION B.3 |
| 2026-09-13 | **439.0** FK `suggestion_ledger` w kodzie (`CONFIRMED`, git). Następny = FK `twin_mark` (`REQUIREMENT`). `data_source` = AI5. CRPS `REJECTED` na tym wierszu. | CURRENT + plaster 439.0 `/noc` |
| 2026-09-13 | AI1.4 (**440.0**) = FK `(organization_id, twin_kind)` → słownik. CHECK ośmiu `REJECTED`. Import `twin_kinds` ze znacznika `REJECTED`. `outcome_kind` CHECK zostaje. | `/plan-modul` `/noc`; VISION C.2 |
| 2026-09-13 | **440.0** FK `twin_mark` w kodzie (`CONFIRMED`, git). Następny = HITL `outcome_kind` (`REQUIREMENT`). `data_source` = AI5. CRPS `REJECTED` na tym wierszu. | CURRENT + plaster 440.0 `/noc` |
| 2026-09-13 | AI1.4 (**441.0**) = HITL `outcome_kind`: `kind_code` bez CHECK/ENUM. Zmiana `outcome_ledger` `REJECTED`. `data_source` leftover AI5. | `/plan-modul` `/noc`; VISION B.3 |
| 2026-09-13 | **441.0** `outcome_kind` w kodzie (`CONFIRMED`, git). Następny = FK `outcome_ledger` (`REQUIREMENT`). `data_source` = AI5. CRPS `REJECTED` na tym wierszu. | CURRENT + plaster 441.0 `/noc` |
| 2026-09-13 | AI1.4 (**442.0**) = FK `(organization_id, outcome_kind)` → słownik. CHECK listy `REJECTED`. Import `outcome_kinds` z ledgeru `REJECTED`. | `/plan-modul` `/noc`; VISION B.3 |
| 2026-09-13 | **442.0** FK `outcome_ledger` w kodzie (`CONFIRMED`, git). Następny = **AI2.0** CRPS (`REQUIREMENT`). `data_source` = AI5. | CURRENT + plaster 442.0 `/noc` |
| 2026-09-13 | AI2.0 (**443.0**) = `interval_score`: MAE + CRPS jednostajne liczy Postgres. Wpis CRPS na `prediction_ledger` zostaje. Brier / champion `REJECTED`. | `/plan-modul` `/noc`; VISION B.2 |
| 2026-09-13 | **443.0** `interval_score` w kodzie (`CONFIRMED`, git). Następny = **AI2.1** champion/dryf (`REQUIREMENT`). Brier / zapis `prediction_ledger` zostają leftover. | CURRENT + plaster 443.0 `/noc` |
| 2026-09-13 | AI2.1 (**444.0**) = `version_score`: średnie MAE/CRPS per wersja modelu. Auto-champion / dryf `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION B.2 |
| 2026-09-13 | **444.0** `version_score` w kodzie (`CONFIRMED`, git). Następny = leftover dryf **445.0** (`REQUIREMENT`). Auto-champion `REJECTED`. | CURRENT + plaster 444.0 `/noc` |
| 2026-09-13 | AI2.1 leftover (**445.0**) = `version_window`: średnie per wersja i dzień. Detektor/próg `REJECTED`. Auto-champion `REJECTED`. | `/plan-modul` `/noc`; VISION B.2 |
| 2026-09-13 | **445.0** `version_window` w kodzie (`CONFIRMED`, git). Następny = zamknięcie wpisu CRPS/MAE na `prediction_ledger` (**446.0**, `REQUIREMENT`). Detektor/próg i auto-champion `REJECTED`. Brier zostaje leftover (brak p). | CURRENT + plaster 445.0 `/noc` |
| 2026-09-13 | AI2 leftover (**446.0**) = `prediction_ledger` przestaje przyjmować wpisane CRPS/MAE. Kolumny nullable. Kopia `interval_score` i drop `REJECTED`. Brier / auto-champion leftover. | `/plan-modul` `/noc`; VISION B.2 · E AI2 |
| 2026-09-13 | **446.0** w kodzie (`CONFIRMED`, git). Nowy INSERT bez `crps`/`mae`. Następny = **AI3.0** PATCH `extraction_draft` (`REQUIREMENT`). Brier leftover. | CURRENT + plaster 446.0 `/noc` |
| 2026-09-13 | AI3.0 (**447.0**) = `PATCH` kandydatów na szkicu przed accept. Wersjonowanie/bbox `REJECTED` (AI3.1). Zapis z modelu `REJECTED` (HC-04). | `/plan-modul` `/noc`; VISION E AI3 |
| 2026-09-13 | **447.0** w kodzie (`CONFIRMED`, git). PATCH `candidates` na pending/`rate_line`. Następny = **AI3.1** wersja/`bbox` (`REQUIREMENT`). Quote/rfp PATCH leftover. | CURRENT + plaster 447.0 `/noc` |
| 2026-09-13 | AI3.1 (**448.0**) = licznik `revision` + ramka/pewność jako tekst. Historia wierszy `REJECTED`. Float `REJECTED`. Zapis z modelu `REJECTED`. | `/plan-modul` `/noc`; VISION E AI3 |
| 2026-09-13 | **448.0** w kodzie (`CONFIRMED`, git). `revision` + `bbox_text`/`confidence_text`. Następny = **AI3.2** obraz wprost (`REQUIREMENT`). | CURRENT + plaster 448.0 `/noc` |
| 2026-09-13 | AI3.2 (**449.0**) = `extract_path` text|image. Live piksele `REJECTED`. Excel/golden `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E AI3 |
| 2026-09-13 | **449.0** w kodzie (`CONFIRMED`, git). `extract_path` text|image jako etykieta. Następny = **AI3.3** golden (`REQUIREMENT`). Live vision `REJECTED`. | CURRENT + plaster 449.0 `/noc` |
| 2026-09-13 | AI3.3 (**450.0**) = własny zbiór golden + bramka pytest. Liczby z preprintu `REJECTED` jako stała. Excel/vision `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E AI3 |
| 2026-09-13 | **450.0** w kodzie (`CONFIRMED`, git). Dwa przypadki THC/BAF vs `MockExtractor`. Następny = **AI3.4** Excel (`REQUIREMENT`). | CURRENT + plaster 450.0 `/noc` |
| 2026-09-15 | AI3.3 leftover (**509.0**) = pętla golden ≥500 vs MockExtractor. DocLayNet / 2k / 5k / live vision `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **509.0** w kodzie (`CONFIRMED`, git). 500 przypadków vs `MockExtractor`. Następny = **510.0** ≥2000 (`REQUIREMENT`). | CURRENT + plaster 509.0 `/noc 15` |
| 2026-09-15 | AI3.3 leftover (**510.0**) = pętla golden ≥2000 vs MockExtractor. 5k / DocLayNet / live vision `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **510.0** w kodzie (`CONFIRMED`, git). 2000 przypadków vs `MockExtractor`. Następny = **511.0** ≥5000 (`REQUIREMENT`). | CURRENT + plaster 510.0 `/noc 15` |
| 2026-09-15 | AI3.3 leftover (**511.0**) = pętla golden ≥5000 vs MockExtractor. DocLayNet / live vision `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **511.0** w kodzie (`CONFIRMED`, git). 5000 przypadków vs `MockExtractor`. Następny = **512.0** openpyxl (`REQUIREMENT`). | CURRENT + plaster 511.0 `/noc 15` |
| 2026-09-15 | AI3.4 leftover (**512.0**) = openpyxl na `.xlsx`. Live vision `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **512.0** w kodzie (`CONFIRMED`, git). `XlsxSheetParser` przez openpyxl. Następny = **513.0** Instructor CI (`REQUIREMENT`). | CURRENT + plaster 512.0 `/noc 15` |
| 2026-09-15 | AI3 leftover (**513.0**) = Instructor×golden stub w gate. Żywy OpenAI / DocLayNet `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **513.0** w kodzie (`CONFIRMED`, git). Instructor stub × golden. Następny = **514.0** formuły (`REQUIREMENT`). | CURRENT + plaster 513.0 `/noc 15` |
| 2026-09-15 | AI3.4 leftover (**514.0**) = tekst formuły bez cache Excel. Ewaluacja `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **514.0** w kodzie (`CONFIRMED`, git). Formuła bez cache. Następny = **515.0** undo (`REQUIREMENT`). | CURRENT + plaster 514.0 `/noc 15` |
| 2026-09-15 | AI3.1 leftover (**515.0**) = undo ostatniego `payload.history`. Undo do dowolnej rewizji / live vision `REJECTED`. | `/plan-modul` `/noc 15`; VISION E AI3 |
| 2026-09-15 | **515.0** w kodzie (`CONFIRMED`, git). POST undo. Następny = **516.0** AI7.0 (`REQUIREMENT`). Instructor wiring park. | CURRENT + plaster 515.0 `/noc 15` |
| 2026-09-15 | AI7.0 (**516.0**) = HITL otwarty słownik `allocation_key`. SQL alokacji / TCM / druga marża / live ERP `REJECTED` na tym wierszu. | `/plan-modul` `/noc 7`; VISION B.6 |
| 2026-09-15 | **516.0** w kodzie (`CONFIRMED`, git). `allocation_key` HITL. Następny = **517.0** 6 kategorii (`REQUIREMENT`). SQL/TCM `REJECTED`. | CURRENT + plaster 516.0 `/noc 7` |
| 2026-09-15 | AI7.0 leftover (**517.0**) = HITL `cost_category_mark` (direct|shared|allocated|overhead|capital|risk). SQL/TCM `REJECTED`. | `/plan-modul` `/noc 7`; VISION B.6 |
| 2026-09-15 | **517.0** w kodzie (`CONFIRMED`, git). 6 kategorii HITL. Następny = **518.0** 12 poziomów (`REQUIREMENT`). | CURRENT + plaster 517.0 `/noc 7` |
| 2026-09-15 | AI7.0 leftover (**518.0**) = HITL otwarty słownik `allocation_level`. SQL/TCM `REJECTED`. | `/plan-modul` `/noc 7`; VISION B.6 |
| 2026-09-15 | **518.0** w kodzie (`CONFIRMED`, git). 12 poziomów HITL. Następny = **519.0** AI6.0 (`REQUIREMENT`). SQL/TCM/AI7.1 park. | CURRENT + plaster 518.0 `/noc 7` |
| 2026-09-15 | AI6.0 (**519.0**) = HITL `impact_node_mark` (shipment|inventory|sku|line|order|revenue|margin|cash). SQL/EBITDA/edge `REJECTED`. | `/plan-modul` `/noc 7`; VISION B.6 |
| 2026-09-15 | **519.0** w kodzie (`CONFIRMED`, git). 8 węzłów HITL. Następny = **520.0** edge (`REQUIREMENT`). SQL/EBITDA park. | CURRENT + plaster 519.0 `/noc 7` |
| 2026-09-15 | AI6.0 leftover (**520.0**) = HITL `impact_edge_mark` (from_kind×to_kind). SQL/EBITDA/FK węzeł `REJECTED`. | `/plan-modul` `/noc 7`; VISION B.6 |
| 2026-09-15 | **520.0** w kodzie (`CONFIRMED`, git). Krawędź HITL. Następny = **521.0** AI9.0 (`REQUIREMENT`). SQL/EBITDA park. | CURRENT + plaster 520.0 `/noc 7` |
| 2026-09-15 | AI9.0 (**521.0**) = HITL `article50_mark` (generated|exempt|human|other). U-art50 UI / scoring `REJECTED`. | `/plan-modul` `/noc 7`; VISION B.6 |
| 2026-09-13 | AI3.4 (**451.0**) = OOXML pierwszy arkusz → tekst. Nowa zależność `REJECTED`. Vision `REJECTED`. | `/plan-modul` `/noc`; VISION E AI3 |
| 2026-09-13 | **451.0** w kodzie (`CONFIRMED`, git). `parser_name=xlsx_sheet`. Następny = **AI4.0** (`REQUIREMENT`). | CURRENT + plaster 451.0 `/noc` |
| 2026-09-13 | AI4.0 (**452.0**) = FK `plan_snapshot` → shipment/trip/resource, `ON DELETE RESTRICT`. CASCADE `REJECTED`. | `/plan-modul` `/noc`; VISION E AI4 |
| 2026-09-13 | **452.0** w kodzie (`CONFIRMED`, git). FK złożone RESTRICT. Następny = **AI4.1** (`REQUIREMENT`). | CURRENT + plaster 452.0 `/noc` |
| 2026-09-13 | AI4.1 (**453.0**) = FK przebieg → migawka + widok `what_if_replay`. Solver / kółka 500k `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E AI4 |
| 2026-09-13 | **453.0** w kodzie (`CONFIRMED`, git). FK złożone RESTRICT + widok powtórki. Następny = **AI4.2** (`REQUIREMENT`). Solver liczb `REJECTED`. | CURRENT + plaster 453.0 `/noc` |
| 2026-09-13 | AI4.2 (**454.0**) = widok `circle_sim_pair` (samozłączenie unload↔load). Generator 500k / km `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E AI4 |
| 2026-09-13 | **454.0** w kodzie (`CONFIRMED`, git). Para w SQL. Następny = **BR3.0** (`REQUIREMENT`). AI5 `data_source` zostaje park. | CURRENT + plaster 454.0 `/noc` |
| 2026-09-13 | BR3.0 (**455.0**) = HITL `route_plan_mark` (`route|stop|window|other`). Valhalla `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **455.0** w kodzie (`CONFIRMED`, git). Katalog planu trasy. Następny = **BR6.0** (`REQUIREMENT`). Valhalla leftover. | CURRENT + plaster 455.0 `/noc` |
| 2026-09-13 | BR6.0 (**456.0**) = HITL `crm_opportunity` (`open|won|lost|other`). Activity / pipeline `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **456.0** w kodzie (`CONFIRMED`, git). Katalog okazji. Następny = **BR2.0** (`REQUIREMENT`). Pipeline leftover. | CURRENT + plaster 456.0 `/noc` |
| 2026-09-13 | BR2.0 (**457.0**) = HITL `position_event` (`gps|manual|other`). Live GPS `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **457.0** w kodzie (`CONFIRMED`, git). Katalog zdarzenia pozycji. Następny = **BR2.1** (`REQUIREMENT`). Współrzędne / poll leftover. | CURRENT + plaster 457.0 `/noc` |
| 2026-09-13 | BR2.1 (**458.0**) = HITL `telematics_device` (`tracker|fault|other`). Parowanie / live GPS `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **458.0** w kodzie (`CONFIRMED`, git). Katalog urządzenia. Następny = **BR2.2** (`REQUIREMENT`). Parowanie leftover. | CURRENT + plaster 458.0 `/noc` |
| 2026-09-13 | BR2.2 (**459.0**) = HITL `tracking_consent` (`party|driver|other`). Kolumna na kontakcie / live GPS `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **459.0** w kodzie (`CONFIRMED`, git). Katalog zgody. Następny = **BR6.1** (`REQUIREMENT`). Kolumna na kontakcie leftover. Expo BR2.3 park. | CURRENT + plaster 459.0 `/noc` |
| 2026-09-13 | BR6.1 (**460.0**) = HITL `sales_lane` (`repeat|spot|other`). UN/LOCODE / pipeline / HubSpot live `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **460.0** w kodzie (`CONFIRMED`, git). Katalog korytarza sprzedaży. Następny = **BR6.2** (`REQUIREMENT`). UN/LOCODE leftover. | CURRENT + plaster 460.0 `/noc` |
| 2026-09-13 | BR6.2 (**461.0**) = HITL `shipper_tender_mark` (`round|bench|spot|other`). Druga tabela `tender` / auto-award / Alpega live `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **461.0** w kodzie (`CONFIRMED`, git). Katalog trybu załadowcy. Następny = **BR6.5** (`REQUIREMENT`). Rundy leftover. Expo BR6.3 park. | CURRENT + plaster 461.0 `/noc` |
| 2026-09-13 | BR6.5 (**462.0**) = HITL `campaign_mark` (`campaign|attribution|other`). Atrybucja live / `funnel_mark` `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **462.0** w kodzie (`CONFIRMED`, git). Katalog kampanii. Następny = **BR3.2** (`REQUIREMENT`). Atrybucja leftover. Expo BR6.3 park. | CURRENT + plaster 462.0 `/noc` |
| 2026-09-13 | BR3.2 (**463.0**) = HITL `groupage_dispatcher_mark` (`line|hub|cutoff|consol|other`). Silnik hubów / klej do `groupage_line` `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **463.0** w kodzie (`CONFIRMED`, git). Katalog stance dyspozytora. Następny = **BR3.1** (`REQUIREMENT`). Silnik hubów leftover. | CURRENT + plaster 463.0 `/noc` |
| 2026-09-13 | BR3.1 (**464.0**) = HITL `load_order_mark` (`sequence|stack|door|other`). Solver / wymiary Decimal / klej do G6 `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **464.0** w kodzie (`CONFIRMED`, git). Katalog kolejności załadunku. Następny = **BR3.3** (`REQUIREMENT`). Solver leftover. | CURRENT + plaster 464.0 `/noc` |
| 2026-09-13 | BR3.3 (**465.0**) = HITL `tacho_plan_mark` (`plan|window|rest|other`). Live DDD / solver godzin / klej do office `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **465.0** w kodzie (`CONFIRMED`, git). Katalog ograniczenia tacho w planie. Następny = **BR4.0** (`REQUIREMENT`). Live DDD leftover. | CURRENT + plaster 465.0 `/noc` |
| 2026-09-13 | BR4.0 (**466.0**) = HITL `ferry_booking_mark` (`booking|window|sailing|other`). Live rezerwacja / solver art. 9 / klej do `ferry_art9_mark` `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **466.0** w kodzie (`CONFIRMED`, git). Katalog rezerwacji promu. Następny = **BR4.1** (`REQUIREMENT`). Live bilet leftover. | CURRENT + plaster 466.0 `/noc` |
| 2026-09-13 | BR4.1 (**467.0**) = HITL `oog_permit_mark` (`permit|pilot|route|other`). Wymiary Decimal / live zezwolenie / klej do G5 `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **467.0** w kodzie (`CONFIRMED`, git). Katalog zezwolenia OOG. Następny = **BR4.2** (`REQUIREMENT`). Wymiary leftover. | CURRENT + plaster 467.0 `/noc` |
| 2026-09-13 | BR4.2 (**468.0**) = HITL `lcl_console_mark` (`console|cfs|other`). Live CFS / CBM / klej do D6 `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **468.0** w kodzie (`CONFIRMED`, git). Katalog konsoli LCL/CFS. Następny = **BR4.3** (`REQUIREMENT`). Live CFS leftover. | CURRENT + plaster 468.0 `/noc` |
| 2026-09-13 | BR4.3 (**469.0**) = HITL `nac_mark` (`nac|nominated|agent|other`). Live NAC / FK do I2 / auto-send `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-13 | **469.0** w kodzie (`CONFIRMED`, git). Katalog NAC / agenta nominowanego. Następny = **BR4.4** (`REQUIREMENT`). Live NAC leftover. | CURRENT + plaster 469.0 `/noc` |
| 2026-09-14 | BR4.4 (**470.0**) = HITL `silk_corridor_mark` (`silk|block_train|transit|other`). Live CR Express / FK do 110.0 / `lane_pattern` `REJECTED` na tym wierszu. | `/plan-modul` `/noc`; VISION E Fala BR |
| 2026-09-14 | **470.0** w kodzie (`CONFIRMED`, git). Katalog Jedwabnego Szlaku. Następny = **BR5.0** (`REQUIREMENT`). Live CR Express leftover. | CURRENT + plaster 470.0 `/noc` |

---
---

# CZĘŚĆ A — Czym jest OmniRoute i dla kogo

## A.1 Jedno zdanie

**OmniRoute to wielotenantowe oprogramowanie klasy „inteligentne zarządzanie firmą",
które obsługuje jednocześnie obie strony rynku transportu: wykonawcę usługi
(spedycja, przewoźnik, operator logistyczny) i jej zleceniodawcę (korporacja,
załadowca, właściciel łańcucha dostaw), a jego przewagą nie jest lista funkcji,
lecz to, że **każda podpowiedź systemu jest mierzona metodą naukową i rozliczana
z tego, ile realnie oszczędziła**.

Status: `CONFIRMED` — ta definicja to złożenie dwóch dosłownych ustaleń właściciela
z 2026-09-04 (rozmowa `fada5c85`, przełom wizji) i z 2026-09-13.

## A.2 Dwie strony rynku — i dlaczego to jest cały sens

Rynek dzieli oprogramowanie na dwa rozłączne światy, bo tak historycznie wyrósł.

**Świat pierwszy: systemy dla wykonawcy usługi.** TMS i ERP spedycyjne — CargoWise,
Qargo, Interlan SPEED i dziesiątki lokalnych. Umieją zlecenie, przewóz, dokument,
fakturę, marżę. Patrzą na świat z perspektywy „mam zlecenie, muszę je wykonać i na
nim zarobić".

**Świat drugi: systemy dla zleceniodawcy.** Supply Chain Control Tower, czasem
nazywany Watch Tower — Kinaxis, Blue Yonder, project44, FourKites, Shippeo, o4S,
Overhaul i pozostali. Umieją widoczność, wyjątek, ryzyko, wpływ na produkcję.
Patrzą z perspektywy „mam linię produkcyjną i zamówienie klienta, transport jest
tylko jednym z ryzyk".

**Luka, którą właściciel wskazał, realnie istnieje** (`CONFIRMED`, dokument `01` §11.1
i `04`): te dwa światy prawie się nie przecinają. Qargo — potwierdzone czterema
niezależnymi dowodami w dokumencie `04` — **nie obsługuje załadowcy ani control tower**.
CargoWise jest systemem spedytora. Z drugiej strony żaden control tower nie prowadzi
księgi opłat spedytora i nie liczy jego marży. Kto chce mieć oba widoki, kupuje dwa
systemy i płaci trzeciemu za integrację między nimi.

**Dlaczego to jest do zrobienia tylko teraz i tylko w ten sposób.** Te same dane —
przewóz, pozycja, opóźnienie, koszt — mają dla obu stron inne znaczenie. Dla
spedytora opóźnienie to ryzyko kary i pustego przebiegu. Dla korporacji to ryzyko
przestoju linii, kary wobec jej klienta i kosztu kapitału zamrożonego w zapasie.
**Jeden rekord, dwie interpretacje.** Jeśli jeden system trzyma oba modele
interpretacji na tym samym rekordzie, powstaje coś, czego nie da się złożyć
z dwóch osobnych produktów: możliwość odpowiedzenia zleceniodawcy na pytanie
„*co to opóźnienie zrobi z moją marżą*", zanim spedytor w ogóle zdąży je zgłosić.

To nie znaczy, że produkt ma być jednym monolitem sprzedawanym wszystkim. Znaczy,
że **jest to jedna baza, jeden model danych i jeden silnik wnioskowania, sprzedawany
w dwóch skórach**, z pełną izolacją tenantów (RLS wymuszany przez bazę, nie przez
kod aplikacji — patrz część B.1).

**Jedna baza, dwie skóry — nie dwa codebase'y** (`REQUIREMENT`, dump CT 2026-09-13,
badania `03` A.4 / B.1): 14.07.2026 project44 rozdzielił GTM na `project44`
(załadowca) i `LSP44` (3PL / forwarder / broker) przy **tym samym OpenAPI v4**
(`https://lsp44.ai/press-release/project44-launches-lsp44/`). OmniRoute nie
rozszczepia produktu na dwie aplikacje dla spedytora i załadowcy.

**Shippeo ≠ Overhaul** (`CONFIRMED`, `03` A.4 / B.3): Shippeo 04.05.2026 przejął
**Logward** (execution), nie Overhaul. Overhaul to vendor ryzyka ładunku
(FreightVerify, 18–19.08.2025) — nie analog RTTV. Nie mieszać `cargo_claim` /
fraud z kartą Shippeo. Źródła: PR Shippeo/Logward; PRNewswire Overhaul/FreightVerify.

**e2open w grupie WiseTech** (`CONFIRMED`, close 03–04.08.2025, ASX + SEC 8-K
`000119312525172643`; `03` A.4 / B.9): INTTRA + Harmony + CargoWise pod jednym
holdingiem. Nie obiecywać Harmony Agent bez HITL. Nie dublować pary
CargoWise+Harmony jako „nasz control tower".

**e2open ≠ CargoWise** (`CONFIRMED`, dump TMS `04b` §5.0): WiseTech zamknął
zakup 03.08.2025; cytat CEO „very little product overlap globally”
(wisetechglobal.com/news). Holding ma nogę LSP (CargoWise, badania `04`)
i nogę shipper/network (e2open TMS). Nie obiecywać jednego produktu,
który jest jednocześnie Harmony i CargoWise.

**Dwie skóry TSL + Watch Tower + Postgres RLS** (`CONFIRMED` luka, `04b`
„Czego nie robić” pkt 10): żaden z dziesięciu TMS z krajobrazu MQ nie
sprzedaje tego pakietu. Luka z A.2 stoi.

**CHR Navisphere nie jest ISV** (`CONFIRMED`, `04b` §10): platforma
C.H. Robinson (+ TMC / Managed Solutions). Argument sprzedaży:
„nie siedzisz na platformie konkurencyjnego 3PL”.

**FourKites / Blue Yonder / Kinaxis** (`CONFIRMED` publicznie w `03` B.4–B.6;
skrót do kanonu 2026-09-13, bez zgadywania liczb klientów):
FourKites nazywa pięć bliźniaków (`Order`, `Shipment`, `Inventory`, `Asset`,
`Facility`) plus `Loft™` jako środowisko agentów. To analogia do **naszej
taksonomii** C.2, nie nowa tabela-twin i nie obiekt API — schemat bliźniaka
w publicznym API **NIE POTWIERDZONE**. GraphQL z repo third-party
**NIE POTWIERDZONE** jako publiczne API FourKites — nie obiecywać.
Blue Yonder `Supply Chain Command Center` = przebrandowane One Network
(`CONFIRMED` przypis first-party). `docs.onenetwork.com` jest publiczna;
część pól nowszego BY bywa za logowaniem — w kanonie tylko to, co `03`
ma jako POTWIERDZONE. Kinaxis `Maestro®` (dawniej `RapidResponse®`) jest
wzorcem what-if / concurrent planning. Mechanizm kopii planu jest
publicznie opisany jako scenariusz; analog `plan_snapshot` +
`counterfactual_run` **już jest w kodzie jako HITL** (265.0 / 434.0 /
452.0 / 453.0). Solver what-if zostaje leftover AI4.1, nie runtime.

## A.3 Co niniejszym unieważniamy

To jest najważniejszy fragment tej części, bo bez niego wracamy do punktu wyjścia.

Plik `Informacje z claude/vision.md` nosił nagłówek `status: aktualny`,
`last_review: 2026-08-29`. Opisywał produkt **wąski**: narzędzie dla spedytora do
ekstrakcji stawek i wyceny. Ten opis **przestał być prawdziwy 2026-09-04 o 01:19**,
gdy właściciel w rozmowie `fada5c85` rozszerzył zakres na zarządzanie całą firmą
po obu stronach rynku. Korekta nigdy nie trafiła do pliku — trafiła do rozmowy,
która się skończyła.

Dowód, że to nie jest moja interpretacja, jest w dokumencie `01` §2.2: agent
trzykrotnie zawężał zakres do wersji z `vision.md`, a właściciel trzykrotnie go
przywracał, ostatnim razem słowami „**dalej przekręcasz. Źle.**". Wzorzec jest
jednoznaczny i powtarzalny: **agenci systematycznie zawężali wizję do tego, co
było zapisane, a właściciel ją systematycznie przywracał.** Dlatego ten dokument
istnieje i dlatego ma dziennik zmian.

**Unieważnione wprost** (`CONFIRMED`, decyzje właściciela 2026-09-13):

1. **Zakres wąski „produkt dla spedytora".** Segment obejmuje korporacje jako
   pełnoprawnego odbiorcę, nie jako dodatek. `vision.md` do przepisania w całości.
2. **Wykluczenie benchmarku na danych klientów.** Wcześniej traktowane jako
   niedopuszczalne; teraz dopuszczone, z przełącznikiem zakresu uczenia obsługiwanym
   wyłącznie przez SuperAdmina (część D.2, punkt 3).
3. **Gwarancja z 2026-09-08, że treść umów jest niewidoczna nawet dla SuperAdmina.**
   **Wycofana.** SuperAdmin ma pełny dostęp do wszystkiego. Ryzyko prawne tej decyzji
   jest odnotowane w części D.2 i pozostaje otwarte jako świadomie przyjęte.
4. **„Nie robimy WMS i księgowości".** Rozstrzygnięte na rzecz pełnego zakresu —
   z WMS i księgowością włącznie. Uzasadnienie biznesowe jest realne: magazyn
   w Zbrudzewie jest fizycznym aktywem w modelu Trade-Tech (część A.4).
5. **„Nie robimy auto-wysyłki" jako zasada absolutna.** Zastąpione przez pięć
   poziomów autonomii z bramkami (część B.4). Wymaga przepisania `HC-04`
   w `GROUNDING.md`, nie tylko ustalenia w rozmowie — to zostaje jako zadanie,
   nie jako fakt.

## A.4 Model biznesowy — pięć strumieni i wymiar Trade-Tech

Wizja z 2026-09-04 i materiały handlowe z 2026-09-08 opisują coś więcej niż
licencję na oprogramowanie. Poniższy model jest `CONFIRMED` co do treści
(dokument `01` §16.3), natomiast **liczby są symulacją właściciela, nie prognozą
zwalidowaną rynkowo** — i tak muszą być prezentowane.

**Strumień 1 — licencja SaaS.** Klasyczny abonament za tenanta i za użytkownika.
Dwie skóry: TSL i Watch Tower.

**Strumień 2 — telematyka (OmniTelematics).** Własna warstwa pozycji, sprzedawana
albo **dawana darmowo jako koło zamachowe danych** (część A.5). Kluczowe rozróżnienie
techniczne, które już zostało ustalone: `tracking_event` **nie jest** GPS; do pozycji
służy osobny `position_event`.

**Strumień 3 — Trade-Tech: finansowanie obrotu.** To najmniej oczywisty i najbardziej
wyróżniający element. Model łączy finansowanie zamówienia (PO Financing), zwolnienie
towaru z zapasu (Inventory Release) i **fizyczne zabezpieczenie w magazynie
w Zbrudzewie**. Dlatego WMS nie jest kaprysem — bez ewidencji magazynowej
o jakości pozwalającej na zastaw nie ma tego strumienia. Partnerem faktoringowym
w osi wejścia jest SMEO.

**WMS nie jest ozdobą** (`REQUIREMENT`, już rozstrzygnięte; dump `04b`
evidenced): Manhattan Active TM + WMS + Yard + Labour na tym samym
ActivePlatform; Infios Archer Fabric sync OMS/WMS/TMS; SAP EWM obok TM.
To wzmacnia Fala BR (Zbrudzewo / Trade-Tech), nie otwiera live yard / T8.

**Strumień 4 — dane i benchmark.** Zagregowane stawki, korytarze i czasy jako
produkt informacyjny. Wymaga przełącznika zakresu uczenia i jest źródłem ryzyka
prawnego opisanego w D.2.

**Strumień 5 — wdrożenia i partnerzy.** Studium HubSpot i Salesforce (dokument `11`)
pokazuje, że u obu ekosystem partnerów wdrożeniowych jest osobnym, dużym strumieniem.

**Rozbieżność skali, którą trzeba rozstrzygnąć** (`TO_VERIFY`, nierozstrzygnięte):
z 2026-09-04 pochodzi ambicja „setek milionów EUR", z symulacji Trade-Tech
— 29,2 mln PLN przychodu i około 147 mln PLN wyceny w roku trzecim. To albo dwa
różne horyzonty, albo dwie różne definicje. Do uzgodnienia z właścicielem.

## A.5 Oś wejścia na rynek — koło zamachowe danych

To decyzja wiążąca numer 10 z 2026-09-13, `CONFIRMED`. Pełne mapowanie właścicielskie
jest w dokumencie `02`.

```
H&H Logistics (Zbrudzewo)  ─── pierwszy klient, skóra TSL
        │
        │  HHL ma bazę podwykonawców
        ▼
darmowa albo dotowana telematyka dla podwykonawców HHL
        │
        │  HHL łatwiej pozyskuje podwykonawców (ma im co dać)
        │  OmniRoute dostaje dane: kto jeździ, gdzie, za ile
        ▼
nasycenie silnika stawki spotowej i kontraktowej
        │
        ├─> przewoźnik widzi, gdzie ma puste przebiegi, za które nikt nie płaci
        └─> silnik Watch Tower też się nasyca (te same dane, druga interpretacja)
        ▼
KSH Steel i pozostałe spółki grupy ─── pierwszy Watch Tower
        │
        ▼
SMEO ─── partner faktoringowy dla strumienia Trade-Tech
```

**Dlaczego ta oś jest mocna:** rozwiązuje problem zimnego startu silnika
predykcyjnego. Model stawki spotowej bez danych o tym, kto realnie jeździ którym
korytarzem i za ile, jest bezużyteczny. Darmowa telematyka kupuje te dane taniej
niż jakikolwiek zakup zewnętrznego indeksu — i kupuje dane **własne**, czyli takie,
których konkurencja nie ma.

**Konflikt GTM z Uber Freight** (`REQUIREMENT`, `04b` §8.H): Uber Freight
konkuruje o „kto jeździ gdzie i za ile”. To jest ta sama oś danych co
darmowa telematyka + baza podwykonawców HHL. Nie kopiować live CT/GPS
z Uber / Alpega Shippeo-p44 / Oracle `trackingEvents` — u nas katalog HITL.

**Ryzyko tej osi, zapisane uczciwie** (`TO_VERIFY`, nierozstrzygnięte): cała oś
opiera się na jednej grupie kapitałowej. Własny materiał `produkt-na-sprzedaz.md`
§4 ostrzega wprost, że „LOGMAR i HHL to klient zero, nie referencja", i zaleca
2–3 partnerów spoza własnego kręgu. Grupa daje wolumen i szybkość, ale **nie daje
dowodu rynkowego** — a dowód rynkowy jest tym, co się sprzedaje kolejnemu klientowi.

## A.6 Czym OmniRoute nie jest

Ta lista jest równie ważna jak definicja, bo chroni przed rozpłynięciem produktu.

- **Nie jest ERP-em sprzedawanym jako ERP.** Własny materiał handlowy otwiera się
  zasadą „nie sprzedawaj ERP". Sprzedaje się wynik, nie kategoria.
- **Nie jest asystentem AI dopiętym do TMS-a.** AI jest w środku każdego przepływu
  albo nie ma go wcale; nie jest okienkiem czatu w narożniku.
- **Nie jest systemem, w którym model językowy liczy pieniądze.** To zakaz twardy,
  nie preferencja (część D.1).
- **Nie jest narzędziem oceniającym ludzi.** Scoring osoby i jednoosobowej
  działalności jest zakazany nie z uprzejmości, lecz z mocy prawa — AI Act
  załącznik III pkt 5(b) i art. 22 RODO. „To nie nasza decyzja, to prawo."
- **Nie jest fabryką kodu.** Pomysł na moduł generujący moduły został skierowany
  na osobny tor i **nie jest częścią produktu** (decyzja wiążąca numer 7).
- **Nie jest klonem Oracle TM/OTM** (`REJECTED` jako wzorzec, `03` B.8): buy i sell
  na osobnych zasobach / akcjach „calculate" — u nas jeden `charge` i `margin()`.
- **Nie jest dwoma produktami p44 / LSP44.** Dwa ruchy GTM, jedna baza
  (`REQUIREMENT`, `03` B.1).
- **Nie jest siecią 94 tys. organizacji Infor Nexus** jako modelem tenancy
  (`REJECTED`, `03` B.10). Control Center ≠ ION; izolacja = Postgres RLS.
- **Nie jest drugim magazynem marży** (`REJECTED` klon, `04b` §1.D / §2.D /
  §9.D): SAP `Profitability` na `forwarding order`; Oracle `Job.Profit` =
  Revenue − Cost + osobne buy/sell shipments; Shipwell
  `customer_charge_line_items` + `vendor_charge_line_items` + `markup`.
  Zostaje jeden `charge` + `margin()`.
- **Nie jest Navisphere.** CHR nie sprzedaje ISV konkurencyjnym 3PL
  (`CONFIRMED`, `04b` §10).
- **Nie jest e2open jako „drugi CargoWise".** Inny produkt, inna noga holdingu
  (`CONFIRMED`, `04b` §5.0).

---
---

# CZĘŚĆ B — Architektura i substrat rozszerzalności

## B.1 Fundament, który już działa — i którego nie ruszamy

Audyt kodu z 2026-09-13 (dokument `01` §5) ustalił stan faktyczny. To nie jest
projekt na zielonym polu; to projekt z dojrzałym fundamentem i płaską warstwą
funkcjonalną.

**Co jest solidne i sprawdzone w praktyce na ponad czterystu plastrach:**

- **Izolacja tenantów wymuszana przez bazę.** `organization_id` w każdej tabeli
  biznesowej, `FORCE ROW LEVEL SECURITY`, polityka oparta na
  `current_setting('app.current_org')::uuid`. Do każdej nowej tabeli powstaje
  **test izolacji dowodzący**, że wiersz obcego tenanta jest niewidoczny.
  To jest najcenniejszy zasób architektoniczny w tym projekcie i **żadna decyzja
  z tej wizji go nie osłabia**.
  **Odrzucamy sieć Infor jako model tenancy** (`REJECTED`, `03` B.10): Infor
  Control Center **nie jest** Infor ION (osobny `developer.infor.com`); claim
  „94 000+ organizacji" (datasheet INF-2411284, bez metody izolacji) **nie**
  zastępuje `FORCE ROW LEVEL SECURITY`. Zero zapytań cross-tenant. Nie budować
  „CT na ION Gateway".
- **Granice modułów egzekwowane maszynowo.** `import-linter` pilnuje, że bounded
  context nie importuje serwisu innego bounded contextu. Każdy BC ma własny plik
  `AGENTS.md` z listą dozwolonych zależności i listą zakazów.
- **Pieniądz jako `Decimal` nierozerwalnie z walutą.** Nigdy `float`. Marża liczona
  w jednym miejscu — funkcja `margin()` w `backend/app/domain/charge.py` — a `charge`
  jest jedynym wierszem trzymającym równocześnie kupno i sprzedaż.
  **Odrzucamy klon Oracle TM/OTM** (`REJECTED` jako wzorzec, `03` B.8, docs 26a
  `otmra`): Oracle rozdziela kupno i sprzedaż (`perspective`, zasób `sellShipments`,
  akcje `calculateDirectCostBuy` / `calculateDirectCostSell`). Nie klonujemy
  silników „calculate margin".
  Dump TMS `04b` **dopina** ten sam zakaz poza OTM (`REJECTED` klon):
  SAP zakładka `Profitability` / `Profitability Analysis` na FWO
  (źródła kosztu FO/FB/FSD, przychodu FWO/FWSD; PDF TM 9.0 GA);
  Oracle obiekt `Job`: `Total Job Revenue` − `Total Job Cost` = `Profit`
  plus osobne buy/sell shipments (otmol `job_workspace`);
  Shipwell dwa stosy `customer_charge_line_items` /
  `vendor_charge_line_items` + `markup` / `customer_markup`
  (OpenAPI v2 Core). Nikt z dziesiątki nie publikuje Decimal jako HC —
  Oracle `currencyType.value` i Shipwell `Quote.total` to JSON `number`;
  Uber Instant Quote `price.amount` = integer cents
  (`CONFIRMED` luka, `04b` §2.B / §8.B / §9.B). Zostaje Decimal.
  **Odrzucamy float na współrzędnych** (`REJECTED`, `03` B.1.2): p44 publikuje
  `TrackedShipmentPosition.latitude` / `longitude` jako float WGS84. Do geography
  OmniRoute nie kopiujemy tego typu — HC Decimal, zero float na geo.
- **HITL jako wzorzec, nie jako wyjątek.** `extraction_draft` → akceptacja
  człowieka → dopiero zapis. Model nie zapisuje do bazy.
- **Niemutowalność stawek.** `rate_line` z `source_ref`; zmiana to nowy rekord
  i `superseded_by`, nie `UPDATE`.

**Czego nie ma i co jest sedno problemu:** warstwa funkcjonalna jest bardzo szeroka
i bardzo płaska. Dwadzieścia siedem bounded contextów, które w nazwie mają bliźniaka,
predykcję albo pomiar, to **w całości katalogi CRUD** — tabela `mark_code` +
`*_kind` + `source_ref`, endpoint, test izolacji, lista na froncie. Żaden z nich
nic nie liczy. `twin_mark` przechowuje *rodzaj* bliźniaka, nie bliźniaka.
`prediction_ledger` przechowuje wpisaną wartość CRPS, nie policzoną.

To nie jest zarzut wobec tej pracy — to był świadomy tryb „jeden pionowy plaster
naraz", który dał sprawdzony fundament i sto procent pokrycia testami izolacji.
Ale to znaczy, że **wizja z tego dokumentu nie jest kontynuacją dotychczasowego
tempa, lecz zmianą rodzaju pracy**: z dokładania katalogów na dobudowywanie
silników pod katalogi, które już stoją.

**Jedna luka o statusie P0, potwierdzona w kodzie** (`CONFIRMED`, dokument `01` §5.6):
`charge` **nie ma `source_ref`**. Stawka kupna ma pochodzenie, opłata — nie.
Bez tego nie da się udowodnić, skąd wzięła się kwota, a więc nie da się policzyć
oszczędności względem punktu odniesienia. **To musi być pierwsza pozycja fali**,
przed jakimkolwiek elementem AI.

[WYCOFANE 2026-09-13: `charge.source_ref` **jest** w kodzie — plaster 129.0,
migracja 072. Nie otwierać plastra AI0. Akapit powyżej zostaje jako ostrzeżenie
przed ponownym zgłoszeniem „brak pochodzenia".]

## B.2 Cztery tabele substratu — zamiast 232 bliźniaków

To jest centralna decyzja architektoniczna tej wizji i odpowiedź na pytanie, które
przez kilka rozmów wracało bez rozstrzygnięcia: jak zrobić bliźniaka, ciągłe uczenie,
podpowiedzi, pomiar naukowy i pomiar oszczędności **dla każdego elementu programu**,
skoro elementów jest ponad dwieście.

**Odpowiedź: to nie jest pięć wymagań na dwustu obiektach. To jedno zjawisko.**
Podpowiedź, reakcja człowieka na podpowiedź, to co się naprawdę stało, i różnica
między jednym a drugim — to ten sam strumień danych, oglądany z czterech stron.
Budowanie tego osobno dla każdego BC dałoby około dziewięciuset wycinków kodu
robiących to samo. Budowane raz, jako substrat, do którego każdy BC się podłącza,
daje cztery tabele.

**`suggestion_ledger`** — każda podpowiedź, jaką system kiedykolwiek wydał.
Gdzie (bounded context + identyfikator encji), co zaproponowano, z jakim przedziałem
albo poziomem pewności, która wersja modelu i którego promptu to wygenerowała,
co zrobił człowiek (`accept` / `modify` / `reject`) i — krytyczne — **na co zmienił**.
Ta jedna tabela jest równocześnie: sygnałem uczenia, strumieniem obserwacji dla
bliźniaka i podstawą całego pomiaru. Bez pola „na co zmienił" nie ma uczenia
z korekty człowieka, a to jest najcenniejszy sygnał, jaki ten produkt będzie miał.

**`outcome_ledger`** — co się naprawdę stało. Złączenie z `suggestion_ledger`
daje CRPS, Brier i MAE **policzone z danych**, a nie wpisane w pole. Tu jest cała
różnica między obecnym `prediction_ledger` a tym, czego wymaga wizja.

**443.0 (`CONFIRMED`, git `/noc`):** pierwszy plaster AI2.0 to widok `interval_score`
plus funkcja SQL `IMMUTABLE`. MAE = odległość od środka przedziału. CRPS = wzór
zamknięty dla rozkładu jednostajnego na `[low, high]`. Brier (`REJECTED` na 443.0)
wymaga prawdopodobieństwa, którego ledger nie ma. Champion/dryf = AI2.1
(`REQUIREMENT`). **444.0 (`CONFIRMED`, git `/noc`):** widok `version_score`
pokazuje średnie, nie przełącza modelu. **445.0 (`CONFIRMED`, git `/noc`):**
widok `version_window` pokazuje średnie per dzień UTC z `created_at`, nie stawia
flagi dryfu. Detektor/próg `REJECTED`. Auto-champion `REJECTED`.
**446.0 (`CONFIRMED`, git `/noc`):** `prediction_ledger` nie przyjmuje wpisanej
metryki. POST bez `crps`/`mae`, kolumny nullable, historia wpisu zostaje.
Kopia `interval_score` do wiersza `REJECTED`. Drop kolumn `REJECTED`.
Brier leftover (brak p). Auto-champion `REJECTED`. Warunek zakończenia AI2
w tabeli E: nowy INSERT nie niesie wpisanej metryki; metryka liczy się
z `interval_score`. Stare wiersze z wpisem zostają do odczytu.

**`counterfactual_run`** — bliźniak w sensie operacyjnym: nazwany scenariusz,
punkt odniesienia, lista przestawionych dźwigni, wynik. Niemutowalny i odtwarzalny,
bo odpowiedź na pytanie „co by było gdyby" bez możliwości powtórzenia przebiegu
nie jest analizą, tylko anegdotą.

**`benefit_ledger`** — zaoszczędzony czas i zaoszczędzone pieniądze,
**z jawnie zapisaną metodą wyznaczenia punktu odniesienia**. To wymaganie właściciela
„każdy element liczy, ile zaoszczędził" — ale realizowane w jedyny uczciwy sposób.
Bez zapisanej metody punktu odniesienia liczba oszczędności jest nieweryfikowalna,
a produkt sprzedawany na nieweryfikowalnej liczbie oszczędności jest produktem,
który się kiedyś przewróci na pierwszym audycie u klienta.

**Dlaczego to od razu odpowiada na wymagania 2, 3, 4, 5 i 6 z promptu właściciela:**
bliźniak każdego elementu to `suggestion_ledger` + `outcome_ledger` zawężone do
tego elementu. Pytanie „co by było gdyby" to `counterfactual_run`. Ciągłe uczenie
to pętla po korektach człowieka w `suggestion_ledger`. Naukowy pomiar to metryki
ze złączenia dwóch pierwszych tabel. Pomiar oszczędności to `benefit_ledger`.
Jedna konstrukcja, pięć wymagań.

**Trójka plan / fakt / estymata** (`REQUIREMENT`, `03` B.1): project44 publikuje
`TrackedShipmentDateTime.type` = `PLANNED` | `ACTUAL` | `ESTIMATE` oraz długi
enum `TrackedShipmentEvent.type`. To jest bliżej `entity_event` /
`prediction_ledger` niż marketingowych „twins" FourKites (karta `03` B.4; skrót w A.2).
p44 **nie** publikuje CRPS/MAE — nasze AI2
nadal liczy metryki z danych.

**Oracle LML** (`CONFIRMED`, `04b` §2.E, otmol `ml_perform_prediction`):
jedyna publiczna metoda AI z przedziałem w dziesiątce — 95% prediction
interval, pola `Prediction Low Value` / `Prediction High Value`. To **nie**
jest CRPS/MAE ani niezależny audyt. `prediction_ledger` zostaje daną HITL
aż AI2 policzy ze złączenia `suggestion_ledger` × `outcome_ledger`.

**Shippeo Triple SLA** (`REQUIREMENT` + zakaz claimu, `03` B.3.4): vendor nazywa
kontrakt ETA + onboarding + tracking i cytuje money-back; **progi liczbowe są
ZA LOGOWANIEM**. Nasz `prediction_ledger` trzyma miarę **jako daną**, nie jako
aneks kontraktu, który wymyślamy. Nie cytujemy ich liczb SLA.

**Luka `CONFIRMED`** (dump CT 2026-09-13, `03` B.11): żaden z siódemki (p44/LSP44,
o9, Shippeo, SAP GTT, Oracle OTM, e2open, Infor Nexus) nie ma `charge` buy+sell
ani `benefit_ledger`. Najbliższe — i **złe** — analogie: Oracle split buy/sell
oraz p44 `costs[]` / e2open `/{loadid}/rates` (tylko koszt). To wzmacnia AI1.3
i już istniejące pochodzenie `charge.source_ref` (129.0 / 072) — nie nowy plaster
AI0.

**Wzorce do cytowania, nie silniki do kopiowania** (`REQUIREMENT`, `04b`
„Co skopiować”): Oracle język BUY/SELL (nie dwa wiersze shipment);
Manhattan `Quick Rate Lookup` — quote bez tworzenia shipment;
e2open `carrierRateReference` (EDI 204 L11 QUT) jako analog `source_ref`;
katalogi zdarzeń Shipwell / Navisphere jako inspiracja nazw
`tracking_event` / `entity_event`, nie live silnik.

## B.3 Otwarte słowniki — warunek rozszerzalności

Decyzja wiążąca numer 6 z 2026-09-13, `CONFIRMED`. Właściciel postawił wymóg,
żeby architektura pozwalała dodać nową tabelę, moduł, pole, silnik i sekcję
**bez przebudowy**. Konsekwencja jest konkretna i dotyczy sposobu pisania migracji.

**Rodzaj bytu nigdy nie jest ograniczeniem `CHECK` ani typem `ENUM`. Jest wierszem
w tabeli słownikowej.**

- **`twin_kind`** — nowy rodzaj bliźniaka to `INSERT`, nie migracja i nie wydanie (`CONFIRMED`, 437.0).
- **`data_source`** — słownik źródeł zewnętrznych, z licencją i zakresem praw
  przy każdym wierszu. To jest miejsce, w którym mieszka katalog z dokumentu `10`.
- **`autonomy_level`** — poziom autonomii jako **dana per tenant** (`CONFIRMED`,
  438.0). Per klient (FK) zostaje leftover. Nie stała w kodzie (część B.4).
- **`suggestion_kind`** — nowy rodzaj podpowiedzi to wiersz (`CONFIRMED`, 436.0).
- **`outcome_kind`** — nowy rodzaj wyniku to wiersz (`CONFIRMED`, 441.0). FK z `outcome_ledger` (`CONFIRMED`, 442.0). CHECK listy na ledgerze `REJECTED`.

**Model zdarzeń SAP GTT** (`REQUIREMENT`, `03` B.7, PDF LBN 2.0 z 19.04.2025):
planned event + **okno tolerancji**, unplanned, adres XRI
(`xri://sap.com/id:LBN#…`); interfejsy `GTT_V2_*` powstają **po** wdrożeniu
modelu (standard `gttft1` i własne). Nie hardcodować zamkniętej listy milestone
w kodzie — otwarty słownik / dane, jak `suggestion_kind`.

Cena tej decyzji, powiedziana wprost: tracimy część gwarancji, które dawał
`CHECK` na poziomie bazy. Rekompensata to walidacja wobec słownika w warstwie
serwisu plus klucz obcy do tabeli słownikowej. **To jest świadomy kompromis
na rzecz rozszerzalności**, a nie przeoczenie.

## B.4 Pięć poziomów autonomii AI

Decyzja wiążąca numer 5, `CONFIRMED`. Domyślnie **LEVEL 1**. Wyżej tylko przez
bramkę, z zapisem w audit logu, jako dana per tenant i per klient.

| Poziom | Nazwa | Co AI robi | Warunek wejścia |
|---|---|---|---|
| 0 | Observer | tylko patrzy i zapisuje do `suggestion_ledger`, nic nie pokazuje | — |
| 1 | Asystent | pokazuje podpowiedź, człowiek decyduje o wszystkim | domyślny |
| 2 | Recenzent | pokazuje **różnicę** wobec stanu i proponuje korektę | zmierzona jakość na własnym zbiorze golden |
| 3 | Wykonawca w limitach | działa sam w jawnie zapisanych granicach, człowiek widzi po fakcie | bramka jakości + limity zapisane jako dana + audit log |
| 4 | Negocjator | prowadzi wymianę w granicach mandatu | bramka + mandat jako dana + pełny zapis |
| 5 | Agent sprzedaży | prowadzi proces sprzedażowy | bramka + zgoda właściciela per tenant |

**Bramka jakości nie jest ozdobą.** Wejście na poziom wyżej wymaga zmierzonego
wyniku na **własnym** zbiorze golden — nie na benchmarku z literatury i nie na
liczbie od dostawcy. Poniżej progu poziom się nie włącza, a jeśli wynik spadnie,
poziom schodzi automatycznie.

**Konflikt HC-04** — [WYCOFANE 2026-09-13: Q1–Q2 + przepisanie
`GROUNDING.md`]. HC-04 mówi: L0–2 bez zapisu AI; L3–5 tylko w zapisanych
granicach + audit; auto-zejście jakości przed L3. LLM nadal nie liczy.

## B.5 Hierarchia stylu — dlaczego bliźniak człowieka jest legalny

Tu rozstrzygamy sprzeczność, która wyglądała na nieusuwalną: właściciel chce
bliźniaków imitujących relacje między konkretnymi ludźmi, a jednocześnie
obowiązuje bezwzględny zakaz oceniania osób.

**Rozstrzygnięcie, potwierdzone w `Rozwiązanie_Relacji_AI.pdf`** (`CONFIRMED`):
bliźniak osoby jest **bliźniakiem stylu i relacji**, nie oceną wyników.
Modeluje, *jak* ten człowiek pisze i czego zwykle oczekuje w rozmowie z tym
konkretnym kontrahentem — nigdy tego, *jak dobrze* pracuje. Pierwsze jest
narzędziem pomocy. Drugie jest zakazane prawem.

Kaskada stylu, od najbardziej ogólnego do najbardziej szczegółowego:

```
Global AI → Company Style → Department Style → User Style
          → Customer Style → Person-to-Person Style → Current Context
```

Każdy niższy poziom nadpisuje wyższy tylko w tym, co ma ustalone. Do tego
**`STYLE FIDELITY SCORE` jako bramka na poziomie 85%** — szkic, który nie brzmi
jak ten użytkownik w rozmowie z tym kontrahentem, nie jest mu proponowany.

## B.6 Silniki, które trzeba dobudować pod istniejące katalogi

Dla każdego z poniższych katalog HITL **już istnieje w kodzie**. Brakuje warstwy,
która liczy. To jest treść fali opisanej w części E.

1. **Silnik ekstrakcji z pomiarem** — ścieżka „obraz wprost" jako challenger dla
   obecnej ścieżki przez tekst, `PATCH` na `extraction_draft`, edycja w interfejsie
   przed akceptacją, wersjonowanie, obsługa Excela, bramka progowa.
2. **Silnik stawki spotowej i kontraktowej** — nasycany danymi z telematyki.
3. **Silnik ETA i opóźnienia** — z przedziałem, nie wróżbą punktową.
   Wzorzec publikacji benchu (`REQUIREMENT`, `03` B.2.4): o9, 23.07.2026,
   first-party NVIDIA cuOpt — zbiór ~**30 mln** zmiennych, **15,7 mln**
   ograniczeń; GPU B200 **57,4 s** vs CPU **661,7 s**; delta objective
   **0,008%**; oba status optimal. Źródło: o9solutions.com news cuOpt.
   Ten sam rygor metody przy benchach AI1 / `suggestion_ledger` i przy BR3.0
   (Valhalla / solver). **Liczy solver, nie model językowy.**
4. **Silnik what-if** na `counterfactual_run` — symulacja kółek w SQL, nie w Pythonie.
5. **Silnik kosztu obsługi** — Cost Allocation Engine: dwanaście poziomów alokacji,
   sześć kategorii kosztu, dwadzieścia trzy klucze podziału, wynik jako
   **`TRUE CONTRIBUTION MARGIN`**. To odpowiedź na pytanie „ile realnie zarabiamy
   na tym kliencie", którego dzisiejszy `charge` nie potrafi udzielić.
6. **Graf skutku biznesowego** (Business Impact Graph) — kaskada
   `Shipment → Inventory → SKU → Production Line → Customer Order → Revenue → Margin → Cash`.
   To jest technicznie **cały Watch Tower**: tłumaczenie zdarzenia transportowego
   na język zarządu korporacji.
7. **Silnik danych zewnętrznych** — ingest, cechy modelu, kaskada skutku.
8. **Silnik podpowiedzi i pomiaru** — substrat z części B.2, wspólny dla wszystkich.
9. **Silnik stylu** — kaskada z części B.5 z bramką wierności.
10. **Silnik zgodności** — AI Act, RODO, etykieta art. 50, rejestr ryzyka.
11. **Silnik CRM i sprzedaży** — własny model, konektor per tenant (część C.3).
12. **Cyfrowy CFO** — dla wszystkich typów podmiotów, decyzja wiążąca numer 8.
    Narracja **po** zapytaniu SQL, nigdy zamiast niego; anomalia nie jest dowodem.

## B.7 Jak dodać tabelę, moduł, pole i silnik — wzorce z kodu

Właściciel wymaga, żeby ta wizja odpowiadała na pytanie „jak to rozszerzyć".
Odpowiedź nie jest teoretyczna — wzorce są potwierdzone w repozytorium i wystarczy
je kopiować (`CONFIRMED`, dokument `07` §14).

| Element | Wzorzec do skopiowania 1:1 |
|---|---|
| migracja z RLS | `backend/alembic/versions/235_crm_lead.py` |
| test izolacji tenantów | `backend/tests/crm_leads/test_crm_lead_isolation.py` |
| deklaracja uprawnienia | `require_permission("can_manage_crm_leads", "organization")` w `backend/app/api/crm_leads.py` |
| lista na froncie | `frontend/src/features/crm-lead/catalog-page.tsx` |
| granica modułu | plik `AGENTS.md` w katalogu bounded contextu |

**Nowy rodzaj bytu** (bliźniak, źródło danych, rodzaj podpowiedzi) — `INSERT`
do słownika, bez migracji.
**Nowy silnik** — podłączenie do substratu z B.2, bez własnych tabel na podpowiedzi
i pomiar.
**Nowe pole** — migracja + rozszerzenie modelu + typ na froncie; bez zmian
w zastosowanych migracjach, zawsze nowa.

## B.8 Bramka publikacji — Cloudflare jako warstwa bezpieczeństwa

Właściciel (2026-09-13): **wdrożyć Cloudflare jako warstwę bezpieczeństwa zanim
aplikacja będzie publiczna.** To jest bramka **publikacji HTTP**, nie plaster
produktu i nie marketingowy CDN. Nie zmienia kolejki `/noc`. Następny plaster
zostaje **431.0**. `charge.source_ref` już jest — nie otwierać AI0.

**Stan repo (`CONFIRMED`, audyt 2026-09-13):** nie ma Traefik / Caddy / nginx
w drzewie. `docker-compose.yml` wystawia tylko PostgreSQL 16 i OpenFGA
(playground). FastAPI (`backend/app/main.py`) ma `RequestIdMiddleware`;
**brak** CORS, HSTS, TrustedHost i rate limitu w aplikacji. SPA Vite
proxy `/api` i `/health` na `127.0.0.1:8000` — to jest deweloperka, nie edge.
C4 w `docs/ARCHITECTURE.md` rysuje operator → HTTPS SPA → JSON API; origin
produkcyjny **nie** jest nazwany. Jedyna wzmianka „Cloudflare” w docs to e-mail
Palletforce za ich proxy (`docs/analysis/dostepy-do-zdobycia.md`) — nie nasza
strefa. Auth produkcyjny = leftover **S53** Auth0 I1/I2 (HITL `idp_connector`
270.0; live parked). Sekrety: GitHub Encrypted Secrets. **Zakaz Infisical.**
Hetzner jako host originu pojawia się tylko w historycznym planie fabryki
(`.cursor/plans/omniroute-realizacja.plan.md`) — **nie** jest wybranym
hostingiem (`TO_VERIFY`).

Cloudflare **nie zastępuje** RLS, OpenFGA, HITL ani `charge` = marża.
Model nadal nie liczy. Access przed SPA **nie** jest IdP tenanta.

### Co jest REQUIREMENT przed ruchem publicznym (konto + domena + origin)

Fakty planów poniżej są z **publicznej dokumentacji Cloudflare**, nie z naszego
cennika. Kwot planu nie zapisujemy.

| Warstwa | Status | Źródło publiczne / uwaga Omni |
|---|---|---|
| DNS strefy + **proxy (orange cloud)** na hoście SPA/API | `REQUIREMENT` | [Proxy status](https://developers.cloudflare.com/dns/proxy-status/). Bez proxy nie ma WAF/HSTS/Access na tym hoście. |
| TLS na krawędzi; do originu **Full** albo **Full (strict)**, nie Flexible | `REQUIREMENT` | [Encryption modes](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/) (aktualizacja 2026-04-16): Cloudflare zaleca Full / Full (strict); Full (strict) wymaga certyfikatu originu (publiczne CA albo Cloudflare Origin CA). Flexible = HTTP do originu — `REJECTED` na publikację. |
| HSTS po działającym HTTPS | `REQUIREMENT` | [HSTS](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/http-strict-transport-security/) (2026-08-14): dostępne na planie Free. Preload / `includeSubDomains` dopiero gdy wszystkie hosty mają HTTPS (`TO_VERIFY` przy konfiguracji). |
| WAF **Cloudflare Free Managed Ruleset** | `REQUIREMENT` | [Managed Rules — Availability](https://developers.cloudflare.com/waf/managed-rules/) (2026-09-08): Free Managed Ruleset na **wszystkich** planach (wysokoudarowe, szeroko eksploatowane luki). |
| WAF **Cloudflare Managed Ruleset** + **OWASP Core Ruleset** | `REQUIREMENT` na publikację z otwartym Internetem; **nie** na planie Free | Ta sama tabela: Managed + OWASP = **Pro i wyżej**. To nie jest „później, bo nie chcemy” — to limit planu dostawcy. Kupno Pro **nie** jest plastrem. |
| Jedna reguła **rate limiting** na `/api` (IP, okno 10 s) | `REQUIREMENT` na Free | [Rate limiting — Availability](https://developers.cloudflare.com/waf/rate-limiting-rules/) (2026-08-25): Free = 1 reguła, charakterystyka IP, okres 10 s, mitigacja 10 s. Więcej reguł / dłuższe okna = Pro+ (limit dostawcy, nie nasza cena). |
| **Cloudflare Access** (Zero Trust) przed SPA operatora i `/api` | `REQUIREMENT` *zanim* publiczni tenantci | [Access policies](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/) (2026-09-04): Access jest **deny by default**; Allow po e-mailu / końcówce domeny / IdP. To zamek przed publikacją, nie login tenanta. **Nie** zdejmuje leftover S53 Auth0 I1/I2. |
| DDoS L3/L7 na ruchu proxowanym | `REQUIREMENT` (wchodzi z orange cloud) | Kolejność faz WAF: HTTP DDoS (`ddos_l7`) przed custom/rate/managed ([Managed Rules — execution order](https://developers.cloudflare.com/waf/managed-rules/), 2026-09-08). |

### Co jest później albo ostrożnie

| Warstwa | Status | Dlaczego |
|---|---|---|
| **Bot Fight Mode** na całej strefie | `TO_VERIFY` przed włączeniem na `/api` | [Bot Fight Mode](https://developers.cloudflare.com/bots/get-started/bot-fight-mode/) (2026-08-03): darmowy; **chroni całą domenę bez ograniczenia ścieżki**; może challenge'ować API; **nie da się** pominąć regułą WAF Skip. Na pre-publish Access + 1 rate limit na `/api` wystarcza. Super Bot Fight Mode (Skip na Ruleset Engine) = później, płatny. |
| Challenge tylko na nadużycie `/api` | `REQUIREMENT` = rate limit (wyżej); Bot Fight ≠ ten sam mechanizm | Rate limit na Free jest ścieżkowy. Bot Fight — nie. |
| Workers / cache HTML / image CDN / marketing | `REJECTED` jako cel tej bramki | To nie jest warstwa bezpieczeństwa publikacji. |
| Cloudflare jako magazyn sekretów tenanta / kluczy LLM / Postgres | `REJECTED` | HC-05: sekrety tenanta szyfrowane kluczem tenanta; GitHub Encrypted Secrets; zakaz Infisical. Baza i OpenFGA **nie** idą przez publiczny proxy jako porty 5432/8080. |

### Czego nie kłaść na Cloudflare

- `POSTGRES_*`, JWT, `OPENAI_API_KEY`, klucze tenantów, wrapped DEK / KEK.
- Playground OpenFGA (`3000`) i port bazy — zostają w sieci prywatnej originu.
- Treść umów / `blob_ciphertext` — Access nie jest unwrap.
- Live Auth0 / Graph / portale — leftover S53 / S55; Access ich nie zastępuje.

### Kroki właściciela (konto, nie kod)

1. Czy jest już konto Cloudflare i jaka jest domena produkcyjna — `TO_VERIFY`.
2. Dodać strefę, wskazać nameservery, poczekać na active.
3. Rekord A/AAAA/CNAME hosta aplikacji: **Proxied**.
4. Certyfikat originu + tryb **Full (strict)**.
5. HSTS po pierwszym czystym HTTPS.
6. Włączyć Free Managed Ruleset.
7. Jedna reguła rate limit na `http.request.uri.path` zaczynające się od `/api`.
8. Zero Trust: aplikacja Access na ten host; Allow dla e-maili operatora
   (albo końcówka domeny firmy); **nie** Include Everyone.
9. Origin: tylko ruch z Cloudflare (po Access). Porty PG/OpenFGA niepubliczne.
10. Plan Pro — gdy trzeba Managed + OWASP na otwarty Internet. Kwota = cennik
    dostawcy w dashboardzie, nie liczba w tym pliku.

Dopóki Access zamyka host, aplikacja **nie jest publiczna** w sensie tej bramki,
nawet jeśli DNS już wskazuje na Cloudflare.

---
---

# CZĘŚĆ C — Pełny inwentarz zakresu

## C.1 Stan faktyczny na 2026-09-13

Liczby z audytów 7–8 września, przeniesione tu, bo bez nich nie da się ocenić,
ile z wizji jest zrobione (`CONFIRMED`, dokument `01` §14):

| Miara | Wartość |
|---|---|
| funkcje zaplanowane w 100% | **47** |
| funkcje **niezaplanowane** | **25** |
| funkcje wymagające weryfikacji | **37** |
| funkcje świadomie odrzucone | **35** |
| pola w projektowanych obiektach | **324** (50 już w kodzie, **274** proponowane) |
| nowe tabele do dołożenia | **32** |
| silniki nazwane w materiałach źródłowych | **42** → 36 wierszy w matrycy + 10 odrzuceń |
| tematy z rozmów bez własnego wiersza w planie | **75** |
| nazwy z PDF-ów bez wiersza w planie | **136** (z czego 28 to aliasy) |
| dostępy do zdobycia | **49** pozycji, z tego **22** o statusie P0 |

Ostatni ukończony plaster: **477.0** (HITL `inventory_collateral_mark`).
Następny = wskazanie Q z pin **2026-09-08c** — nie zgaduj (`REQUIREMENT`).
AI1.0–AI1.4 oraz 443.0–477.0 są w kodzie (`CONFIRMED`); `data_source`
zostaje w AI5 (`REQUIREMENT`). Teza B.1 zostaje: szerokość katalogów nie zastępuje pomiaru.

## C.2 Bliźniaki — scalona taksonomia

Źródła podawały **cztery różne listy bliźniaków: 12, 23, 8 i 8 pozycji**
(`CONFIRMED`, dokument `01` §6.5). Tabela słownikowa `twin_kind` jest otwarta
(`CONFIRMED`, 437.0). `twin_mark.twin_kind` ma FK do słownika
(`CONFIRMED`, 440.0) — CHECK ośmiu wartości zdjęty. Nowy rodzaj = `INSERT`.

**Rozstrzygnięcie:** jedna taksonomia, pięć osi, `twin_kind` jest tabelą
słownikową, więc rozszerzanie nie wymaga migracji ani zmiany `CHECK`.

| Oś | Co modeluje | Przykłady |
|---|---|---|
| **obiekt operacyjny** | rzecz, która fizycznie istnieje i ma stan | zlecenie, przejazd, kontener, pojazd, naczepa, przesyłka, magazyn |
| **osoba i relacja** | **styl i oczekiwania w relacji, nigdy ocena wyników** | użytkownik, kontrahent, para „nasz człowiek ↔ ich człowiek" |
| **proces** | powtarzalny przepływ z wariantami | ekstrakcja, wycena, przetarg, awizacja, windykacja, reklamacja |
| **rynek** | zachowanie zewnętrzne, na które nie mamy wpływu | korytarz, stawka spot, stawka kontraktowa, paliwo, kurs, port, kółko |
| **organizacja** | firma jako całość i jej wynik | tenant, oddział, klient korporacyjny, łańcuch dostaw |

Dwa bliźniaki, których brak wykryto później i które trzeba mieć na liście:
**bliźniak przetargu** i **bliźniak kółka na korytarzu** (dopisane jako `G2.20`).

**Granica prawna wpisana w taksonomię:** oś „osoba i relacja" modeluje wyłącznie
styl komunikacji i oczekiwania w relacji. **Nie modeluje wydajności, jakości pracy
ani wiarygodności człowieka.** Uzasadnienie w części D.5.

## C.3 Brakujące moduły — czego dziś się nie buduje, a wizja tego wymaga

To jest część dopisana na wprost sformułowane polecenie właściciela: *„w planie
budowy aplikacji chcę także brakujące moduły i wszystko inne, bo nowa zaktualizowana
wizja OmniRoute przecież uwzględnia dużo więcej niż obecnie się buduje"*.

Poniższe pozycje **albo nie mają kodu, albo mają wyłącznie katalog HITL**
bez warstwy operacyjnej. Każda ma wiersz w PLAN (Fala BR / Plat-HD / Mob /
AI5–AI7). Podział na grupy odpowiada temu, co blokuje co.

**Grupa 1 — magazyn i fizyczny towar.** Warunek konieczny dla strumienia Trade-Tech,
bo bez ewidencji magazynowej nie ma zastawu na towarze.
- **WMS w pełnym zakresie** — przyjęcie, lokalizacja, kompletacja, wydanie, inwentaryzacja
  (`REQUIREMENT` evidenced `04b` §3.H / §6.H / §1: Manhattan Active
  TM+WMS+Yard+Labour; Infios Archer OMS/WMS/TMS; SAP EWM — WMS nie jest
  dekoracją liderów MQ)
- **RFID i identyfikacja automatyczna** — czytniki, bramki, znakowanie
- **Zapas jako obiekt finansowy** — wycena, wiekowanie, zwolnienie towaru (Inventory Release)
- **Zabezpieczenie na towarze** — powiązanie pozycji magazynowej z finansowaniem

**Grupa 2 — własna telematyka (OmniTelematics).** Koło zamachowe danych z części A.5.
- **Pozycja jako osobny byt** — katalog HITL `position_event` jest (`CONFIRMED`, 457.0);
  wyraźnie oddzielony od `tracking_event`. Leftover współrzędne / poll (`REQUIREMENT`).
  Live GPS `REJECTED` na katalogu.
- **Urządzenia i ich cykl życia** — katalog HITL `telematics_device` jest
  (`CONFIRMED`, 458.0); leftover parowanie z pojazdem / silnik awarii
  (`REQUIREMENT`). Live poll `REJECTED` na katalogu.
- **Zgoda na śledzenie** — katalog HITL `tracking_consent` jest (`CONFIRMED`, 459.0);
  leftover kolumna na `party_contact` (`REQUIREMENT`). Live poll `REJECTED` na katalogu.
- **Aplikacja kierowcy** — zlecenie, POD, skan, status, komunikacja, tryb offline

**Grupa 3 — planowanie i optymalizacja.** Najbardziej „silnikowa" grupa, dziś nieobecna.
- **Planowanie tras** — katalog HITL `route_plan_mark` jest (`CONFIRMED`, 455.0);
  leftover solver Valhalla / VRP / km (`REQUIREMENT`, patrz D.3). Nie model językowy.
- **Planowanie załadunku** — katalog HITL `load_order_mark` jest
  (`CONFIRMED`, 464.0); leftover solver / wymiary Decimal (`REQUIREMENT`).
  Klej do G6 `REJECTED` na katalogu. G6 `load_plan_mark` zostaje osiami/tunelem.
- **Dyspozytor drobnicy** — katalog HITL `groupage_dispatcher_mark` jest
  (`CONFIRMED`, 463.0); leftover silnik hubów / konsolidacja (`REQUIREMENT`).
  Klej do `groupage_line` `REJECTED` na katalogu.
- **Tacho w planowaniu** — katalog HITL `tacho_plan_mark` jest
  (`CONFIRMED`, 465.0); leftover live DDD / solver godzin (`REQUIREMENT`).
  `tacho_office_mark` zostaje office/card/ddd. Klej do office `REJECTED`
  na katalogu.
- **Symulacja kółek** — do 500 tysięcy wariantów, liczona w SQL

**Grupa 4 — gałęzie transportu bez pokrycia.**
- **Promy** — katalog HITL `ferry_booking_mark` jest (`CONFIRMED`, 466.0);
  leftover live rezerwacja / bilet HTTP / solver art. 9 (`REQUIREMENT`).
  `ferry_art9_mark` zostaje rest/watchdog/crossing. Klej do art. 9
  `REJECTED` na katalogu.
- **Ładunki ponadnormatywne** — katalog HITL `oog_permit_mark` jest
  (`CONFIRMED`, 467.0); leftover wymiary Decimal / live zezwolenie
  (`REQUIREMENT`). `oog_mark` zostaje oog/lashing/escort. Klej do G5
  `REJECTED` na katalogu.
- **Konsolidacja morska LCL** — katalog HITL `lcl_console_mark` jest
  (`CONFIRMED`, 468.0); leftover live CFS / kalkulacja CBM (`REQUIREMENT`).
  Druga tabela LCL `REJECTED`. `ocean_bill` zostaje HBL/MBL. Odcinek
  `ocean_lcl` zostaje na `shipment_leg`. Klej do D6 `REJECTED` na katalogu.
- **NAC i agent nominowany** — rola w przepływie dokumentowym
- **Jedwabny Szlak / kolej Chiny–Europa** — katalog HITL `silk_corridor_mark`
  (`CONFIRMED`, 470.0); odcinek `china_rail` zostaje (110.0); leftover
  live CR Express / para UN/LOCODE (`REQUIREMENT`)

**Grupa 5 — finanse i pieniądz.**
- **Faktoring** — katalog HITL `factoring_connector` jest
  (`CONFIRMED`, 471.0); partner SMEO w osi wejścia (`CONFIRMED`, A.5);
  leftover live SMEO HTTP / workflow wypłaty F7 (`REQUIREMENT`)
- **Finansowanie zamówienia** (PO Financing) — katalog HITL `po_financing_mark` jest
  (`CONFIRMED`, 472.0); leftover FK `purchase_order` / wycena zapasu BR1.2 (`REQUIREMENT`)
- **Giełdy transportowe** — katalog HITL `exchange_connector` rozszerzony
  (`CONFIRMED`, 473.0); kind P0 trans_eu|timocom|teleroute|transporeon|other;
  leftover live HTTP / auto-post / wymiana ofert (`REQUIREMENT`)
- **Cyfrowy CFO w pełnym zakresie** — dla wszystkich typów podmiotów, decyzja wiążąca nr 8
- **Cost Allocation Engine** — dwanaście poziomów, `TRUE CONTRIBUTION MARGIN`

**Grupa 6 — sprzedaż, klient i marketing.** Szczegóły w dokumencie `11`.
- **CRM ponad leada** — katalog HITL `crm_opportunity` jest
  (`CONFIRMED`, 456.0); `crm_activity` (`CONFIRMED`, 489.0);
  `crm_pipeline_mark` (`CONFIRMED`, 490.0); `crm_dedup_mark` (`CONFIRMED`, 495.0);
  `crm_link_mark` (`CONFIRMED`, 496.0); `crm_lead` zostaje.
  Leftover cold-send park (`REQUIREMENT`). Cold auto-send `REJECTED`.
- **Korytarz jako obiekt sprzedażowy** — katalog HITL `sales_lane` jest
  (`CONFIRMED`, 460.0); para UN/LOCODE (`CONFIRMED`, 491.0); `volume_label`
  tekst (`CONFIRMED`, 492.0). Leftover HubSpot live / FK (`REQUIREMENT`).
  HubSpot/Salesforce live `REJECTED` na tym wierszu. W TSL decyduje powtarzalny
  wolumen na korytarzu, nie jednorazowy deal.
- **Przetargi korporacyjne po stronie załadowcy** — katalog HITL
  `shipper_tender_mark` jest (`CONFIRMED`, 461.0); `shipper_round_mark`
  (`CONFIRMED`, 493.0); `shipper_like_mark` (`CONFIRMED`, 494.0).
  Leftover Alpega live / FK (`REQUIREMENT`).
  Druga tabela `tender` i auto-award `REJECTED`
  na tym wierszu. Alpega TenderEasy + Freight Bench = kanon EU, nie live.
- **Aplikacja mobilna dla sprzedaży** — iOS i Android
- **Portale** — klienta, przewoźnika, podwykonawcy
- **Marketing i automatyzacja** — katalog HITL `campaign_mark` jest
  (`CONFIRMED`, 462.0); leftover atrybucja live (`REQUIREMENT`).
  Klej do `funnel_mark` `REJECTED` na tym wierszu.

**Grupa 7 — Watch Tower jako produkt.**
- **Graf skutku biznesowego** — kaskada do marży i gotówki (część B.6, punkt 6)
- **Sala operacyjna (war room)** — katalog rodzaju incydentu `war_room_mark`
  jest (`CONFIRMED`, 200.0). Katalog HITL warstwy działającej `ops_room_mark`
  jest (`CONFIRMED`, 478.0). Leftover N8 / widok sklejony / T8 live
  (`REQUIREMENT`). Drugi czat `REJECTED` na tym wierszu.
- **Wpływ na linię produkcyjną** — katalog znacznika skutku `line_impact_mark`
  jest (`CONFIRMED`, 409.0). Katalog HITL warstwy liczonej
  `line_impact_layer_mark` jest (`CONFIRMED`, 479.0). Leftover SQL / EBITDA /
  plant feed (`REQUIREMENT`). Silnik liczący w Pythonie `REJECTED` na tym wierszu.

**Grupa 8 — help desk produktu i sterowanie z telefonu.**
Wymóg właściciela z 2026-09-13 oraz workflow z rozmowy blueprinting / matrycy
7 IX (`IT Support Agent`). Leftover PLAN: **Plat-HD** i dopisek **Mob**.
Nie 468.0. Nie Expo live. Nie nowy BC w tej nocy.
- **Ticket / help desk / customer support produktu OmniRoute** (`REQUIREMENT`) —
  użytkownik zgłasza **błąd programu**, nie pytanie operacyjne o zlecenie.
  Agent przegląda zgłoszenie i proponuje naprawę. Wdrożenie naprawy tylko po
  akceptacji właściciela (HITL). Źródło nazwy w analizie:
  `docs/analysis/benchmark-tms-2026.md` — „ticket → analiza → propozycja
  naprawy → człowiek zatwierdza”, status BRAK, fala HZ.
  To **nie** jest: Operational Service Agent, Customer Chat, CI8
  `repair_playbook`, `capa_mark`, `operator_notice`.
- **Aplikacja mobilna do sterowania całym OmniRoute** (`REQUIREMENT`) — iOS i
  Android; z telefonu widać i zatwierdza się m.in. naprawy ze zgłoszeń powyżej.
  To **nie** jest: BR6.3 (apka sprzedaży), BR2.3 (apka kierowcy), X1–X5
  (portale), pusty wiersz `Mob` (Expo po S53+X bez tego zakresu).
  `mobile_client_mark` to katalog znaczników HITL, nie ta aplikacja.

**Uwaga metodyczna o tej liście.** Nie jest to lista życzeń. Każda pozycja ma
pokrycie w materiałach źródłowych z okresu 29 VIII – 11 IX i jest częścią tych
**25 funkcji niezaplanowanych** oraz **75 tematów bez własnego wiersza w planie**
z tabeli w części C.1. Kolejność realizacji i to, co naprawdę jest potrzebne
u pierwszego klienta, rozstrzyga część E.

## C.4 Trzydzieści dwie nowe tabele

Lista dosłowna z rozmowy „blueprinting" (`CONFIRMED`, dokument `01` §14.1):

`relation_document_requirement` · `resource` · `trip` · `stop` · `position_event` ·
`telematics_connector` · `resource_telematics_link` · `exchange_message` ·
`entity_event` · `weather_observation` · `party_document` · `party_exchange_snapshot` ·
`monitoring_scheme` · `shipment_monitoring_filing` · `map_basemap` · `user_map_prefs` ·
`tenant_map_provider` · `erp_connector` · `erp_series_map` · `erp_export` ·
`scan_enhance_run` · `invoice_match_candidate` · `network_print_requirement` ·
`document_template` · `shipment_package` · `postal_dispatch` · `postal_tracking_event` ·
`postal_epo` · `purchase_invoice` · `purchase_invoice_allocation` · `quote_engagement` ·
`quote_view_token`

**Mapa 2026-09-13 (Alembic + leftover istniejącego ID — nie nowe Q):**

| Nazwa z blueprinting | Stan |
|---|---|
| `resource` · `trip` · `stop` · `telematics_connector` · `entity_event` · `weather_observation` · `party_document` · `monitoring_scheme` · `document_template` · `shipment_package` · `erp_connector` · `position_event` | **jest** (HITL / katalog) |
| `relation_document_requirement` | leftover **C8** |
| `resource_telematics_link` | leftover **V5** |
| `exchange_message` | leftover **V5b** |
| `party_exchange_snapshot` | leftover **C9** |
| `shipment_monitoring_filing` | leftover **C1** |
| `map_basemap` · `user_map_prefs` · `tenant_map_provider` | leftover **X8** |
| `erp_series_map` · `erp_export` | leftover **F9** |
| `scan_enhance_run` | leftover **X9** |
| `invoice_match_candidate` | leftover **F10** po 550.0 |
| `invoice_match_mark` | **550.0** HITL katalog stancji (`CONFIRMED`) |
| `purchase_invoice_allocation` | leftover **F10** (kwota) — mark **551.0** `invoice_alloc_mark` (`CONFIRMED`) |
| `network_print_requirement` | leftover **D9** |
| `postal_dispatch` · `postal_tracking_event` · `postal_epo` | leftover **F11** |
| `purchase_invoice` · `purchase_invoice_allocation` | leftover **F9** / **F10** |
| `quote_engagement` · `quote_view_token` | leftover **X7** |

Nowa tabela = INSERT przy wskazanym ID, gdy CURRENT tam wskaże. Nie 32 plastry
z tej listy. Nie zgadywać kolumn.

Do tego cztery tabele substratu z części B.2 (`suggestion_ledger`, `outcome_ledger`,
`counterfactual_run`, `benefit_ledger`) i cztery słowniki z B.3 (`twin_kind`,
`data_source`, `autonomy_level`, `suggestion_kind`, `outcome_kind`).

## C.5 Rozszerzenia istniejących obiektów

- **`charge.source_ref`** — [WYCOFANE 2026-09-13 jako luka P0 do zrobienia:
  jest w kodzie, plaster 129.0 / 072]. Warunek `benefit_ledger` pozostaje
  (część B.1 / B.2).
- `shipment.shipment_ref` — leftover pinu, nie 468.0
- `sales_invoice.delivery_channel` — leftover **F1** / kanał e-faktury
- `extraction_draft.draft_kind` + `bbox` / pewność w JSONB — **448.0**
  (`CONFIRMED`); **503.0** `payload.history` (`CONFIRMED`); **515.0** undo
  (`CONFIRMED`); leftover Instructor (`07`)
- `party_contact.tracking_consent` — leftover kolumny; katalog
  `tracking_consent` jest (`CONFIRMED`, 459.0)

---
---

# CZĘŚĆ D — Zakazy, granice AI i zgodność

## D.1 Co nie zmienia się nigdy

Te zasady są stałe we **wszystkich** źródłach od 29 sierpnia do dziś i nie ruszamy
ich bez świadomej, zapisanej decyzji właściciela (`CONFIRMED`, dokument `01` §12.3).

1. **`organization_id` w każdej tabeli biznesowej, RLS wymuszany przez bazę,
   test izolacji do każdej nowej tabeli.** Żadne zapytanie nie sięga po dane
   więcej niż jednego tenanta.
2. **Model językowy nie liczy.** Sumy, marża, VAT, kursy — nigdy w modelu.
   Dowód nie jest ideologiczny: w badaniu **PAL** łańcuch myśli dał 20,1%
   poprawnych odpowiedzi tam, gdzie przekazanie obliczenia interpreterowi dało 61%
   (zbiór GSM-HARD).
3. **Kwoty jako `Decimal`, waluta nierozerwalnie z kwotą, nigdy `float`.**
   To samo dla współrzędnych: **odrzucamy** kopiowanie p44 `latitude` /
   `longitude` jako `float` do geography (`REJECTED`, `03` B.1.2).
   Oracle / Shipwell JSON `number` i Uber integer cents (`04b`) **nie**
   zastępują Decimal (`CONFIRMED` luka).
4. **`charge` jest jedynym miejscem prawdy o marży.** Kupno i sprzedaż na jednym
   rekordzie, marża liczona funkcją w domenie. Oracle `perspective` /
   `sellShipments` / `calculateDirectCostBuy`|`Sell` jest **odrzucalnym klonem**
   (`REJECTED`, `03` B.8). SAP `Profitability` na FWO, Oracle `Job.Profit` +
   dwa shipmenty, Shipwell dwa stosy + `markup` — ten sam antywzorzec
   (`REJECTED`, `04b`).
5. **Każda stawka ma `source_ref`.** Bez pochodzenia rekord nie wchodzi.
6. **Stawki są niemutowalne.** Zmiana to nowy rekord i `superseded_by`.
7. **Nic z ekstrakcji nie trafia do bazy bez akceptacji człowieka.**
8. **Poświadczenia zewnętrzne należą do tenanta i są szyfrowane jego kluczem.**
9. **Nie liczymy w Pythonie tego, co Postgres policzy z indeksem.**
10. **Każde wywołanie zewnętrzne jest idempotentne.**

## D.2 Co zmieniamy świadomie — i jakim kosztem

Pięć zmian wobec dotychczasowego kanonu. Każda ma zapisany koszt, bo zmiana bez
zapisanego kosztu wraca po miesiącach jako niespodzianka.

**Zmiana 1 — zakres produktu obejmuje korporacje.**
Koszt: `vision.md` do przepisania, druga skóra produktu, drugi model interpretacji
tych samych danych.

**Zmiana 2 — SuperAdmin ma pełny dostęp do wszystkiego.**
Gwarancja z 2026-09-08 o umowach niewidocznych nawet dla SuperAdmina jest wycofana.
Zysk: ekstrakcja z umów wraca, wdrożenie klienta korporacyjnego realnie przyspiesza.
Koszt, zapisany wprost: przestaje obowiązywać zdanie ze slajdu 9 prezentacji
handlowej („zero AI na umowach i taryfach jako źródle prawdy") oraz zasada
„nie robimy wspólnego benchmarku z danych klientów". Wymaga zmiany `GROUNDING.md`
i `backend/app/services/customer_contracts/AGENTS.md`.
**Ryzyko odnotowane, nie zignorowane:** własny materiał `produkt-na-sprzedaz.md`
§2.3 mówi, że pierwsze pytanie na każdym spotkaniu handlowym to „a kto jeszcze
to widzi", a §6.1 ostrzega, że klient, który dowie się po fakcie, „ma podstawę
do rozwiązania umowy i do zgłoszenia naruszenia". Uczenie na danych tenanta bez
jego wiedzy zmienia OmniRoute z podmiotu przetwarzającego w administratora dla
tego celu, co wymaga własnej podstawy prawnej. **Do potwierdzenia z prawnikiem
przed pierwszym płacącym tenantem.**

**Zmiana 3 — przełącznik zakresu uczenia obsługuje wyłącznie SuperAdmin**,
tenant nie musi o nim wiedzieć.
Koszt: patrz ryzyko przy zmianie 2. Dodatkowo problem techniczny niezależny
od zapisu w umowie — **memoryzacja modelu**: model dostrojony na danych wielu
tenantów może odtworzyć fragment danych jednego z nich w odpowiedzi dla drugiego.
To ryzyko nie znika przez zapis w umowie. `TO_VERIFY`, nierozstrzygnięte.

**Zmiana 4 — pełny zakres, z WMS i księgowością.**
Koszt: duży. Uzasadnienie biznesowe realne (część A.4).

**Zmiana 5 — pięć poziomów autonomii zamiast absolutnego zakazu auto-wysyłki.**
Koszt: `HC-04` do przepisania z jawnym opisem, co wolno na którym poziomie.

## D.3 Granice AI — dwanaście na tak, dwanaście na nie, dwanaście szarych

Ta matryca jest `CONFIRMED` (dokument `01` §10) i przenosi się do wizji bez zmian,
bo każda pozycja ma dowód, nie opinię.

**AI robi, zawsze przez akceptację człowieka:** cennik → pole tekstowe z kwotą →
akceptacja → `rate_line` · wiadomość przychodząca przez ten sam szkic · mail →
szkic zapytania ofertowego (nie silnik wyceny) · faktura kosztowa → szkic
`purchase_invoice` · CMR i POD bez kodu Omni → rodzaj i pola · jeden mechanizm
podziału dla zapytania, faktury, cennika i CMR przez rodzaj szkicu · ramka
na dokumencie z poziomem pewności i edycją przed akceptacją · klasyfikacja rodzaju
dokumentu, gdy brak kodu QR · różnica dokumentu wobec zlecenia **jako recenzja,
nigdy jako nadpisanie** · szkic maila „podaj numer zlecenia" · etykieta z art. 50 ·
guard przed wejściem do modelu.

**AI nie robi — zakazy twarde z dowodem:**
- sumy, marża, VAT, kursy — dowód **PAL** (20,1% vs 61%)
- automatyczny zapis ekstraktu, `rate_line` i `charge` — dowód
  **Goddard, Roudsari, Wyatt 2012 (JAMIA)**: automation bias z ryzykiem względnym
  **1,26 (95% CI 1,11–1,44)**
- **auto-akceptacja korekt i „auto-resolve"** (`REJECTED`, `03` B.11) — LSP44
  „80%+ auto-resolution" (PR 14.07.2026, „internal company data", **bez metody**),
  Infor „without manual intervention", Oracle `autoApproveAdjustedCosts`.
  Odwrotność `operator_decision`. Agenci tylko za Akceptuj / Zmień / Odrzuć.
- **AI-write bo MQ ma** (`REJECTED`, `04b` §1.D / §8.E / §9.E): Shipwell
  Swifty / MCP write / `auto-book`; Uber 30+ agents „take actions on your
  behalf” (PR 21.05.2025); SAP charge calc on save FWO. HC-04: L0–2 bez
  zapisu AI. Obecność w Magic Quadrant nie zdejmuje HITL.
- cena sprzedaży i marża z modelu; automatyczne podpięcie faktury pod zlecenie;
  wynik dopasowania i suma linii zbiorczej w modelu — to zapytanie SQL
- parser KSeF FA(3) przez model — schemat jest sztywny, idzie przez XSD
- model zamiast skanera, gdy na papierze jest kod Omni
- **automatyczny scoring osoby i jednoosobowej działalności** — AI Act załącznik III
  pkt 5(b) i art. 22 RODO
- **GAN i inpainting na fakturze** — „taki model dopowiada piksele; na fakturze
  to nowa cyfra"
- akceptacja wyłącznie na podstawie „pewności"; **poniżej 70% pewności pozycja nie
  wchodzi do akceptacji zbiorczej**
- **RAG na wycenie, schemacie bazy i VAT** (`HC-08`) — RAG tylko na procedurach
- numer nadania, imię z potwierdzenia odbioru i znaczek z OCR albo modelu

**Szare — dopuszczalne, ale nie jako P0 i tylko z rejestrem predykcji, etykietą
z art. 50 i akceptacją człowieka:** czas przybycia i slot · streszczenia maili ·
reguły z tekstu · asystent przy rekordzie · ranking zakupowy · narracja CFO
**po** zapytaniu SQL (anomalia nie jest dowodem) · wczesne ostrzeganie ·
analiza umów · negocjacje w limitach · SQL z modelu przepuszczony przez `sqlglot` ·
prognoza i bliźniak.

**Potwierdzenie z rynku, nie z naszych przekonań** (`CONFIRMED`, dokument `01` §11.3):
przegląd ogłoszeń o pracę u czołówki control tower pokazał, że **nikt z liderów
nie liczy w modelach językowych**. Kinaxis wymaga programowania
całkowitoliczbowego i komercyjnych solverów (Gurobi, Xpress, CPLEX). o9 buduje
graf wiedzy na neuro-symbolice z **deterministycznymi solverami ograniczeń** obok
sieci neuronowych, a na stanowisko prowadzącego ML wymaga „3+ lata w C, C++ albo
Rust, Python tylko do prototypów". project44 stoi na Javie, Kafce i PostgreSQL.
Blue Yonder używa uczenia ze wzmocnieniem na modelach językowych, ale w warstwie
agentowej, nie obliczeniowej. **Zasada „model nigdy nie liczy" jest zgodna
z praktyką liderów, a nie naszym ograniczeniem.**

## D.4 Dowody, które podważają oś sprzedażową — i dlaczego zostają w wizji

Ten podrozdział istnieje, bo obowiązuje zasada mówienia prawdy także wtedy,
gdy prawda jest niewygodna. Poniższe wyniki **osłabiają** najprostszą wersję
narracji sprzedażowej.

- **Metaanaliza w Nature Human Behaviour**: zespół „człowiek + AI" bywa **gorszy
  niż lepsze z dwojga osobno**. Samo dołożenie AI do pracy człowieka nie gwarantuje
  poprawy.
- **Zawody M5**: w prognozowaniu szeregów czasowych metody proste i zespołowe
  wygrywały z rozbudowanymi. Złożoność nie kupuje trafności.
- **Dokładność czasu przybycia u dostawców jest ważona pokryciem** — liczba
  „X procent trafności" bez podania pokrycia jest nieinterpretowalna.
- **Cyfrowe bliźniaki w logistyce są w fazie pilotaży**, nie produkcji.
  Przeglądy literatury same stwierdzają brak walidacji empirycznej.
- **Dwanaście twierdzeń, których nie wolno używać w materiałach** — bo nie mają
  pokrycia w badaniu. Twierdzenia dostawców o 97–99% dokładności ekstrakcji
  zostały odrzucone jako niepoparte metodą.
- **Shippeo Triple SLA** — istnienie kontraktu `CONFIRMED` (`03` B.3.4);
  liczb SLA nie wolno cytować (progi ZA LOGOWANIEM). Money-back jest claimem
  vendora, nie naszą gwarancją.
- **Cursor na dojrzałym projekcie open-source: −19% w badaniu z grupą kontrolną**,
  przy +56% w laboratorium i +26% w badaniu firmowym. Ten sam rodzaj narzędzia,
  trzy różne wyniki zależnie od rygoru pomiaru.
- **Brak recenzowanego badania na przepływie „mail → zlecenie" w spedycji.**
  `MaritimEmails` osiąga F1 0,86, ale **na danych syntetycznych**.
- **Nie znalazłem ani jednego niezależnie zaudytowanego wyniku wdrożenia
  u żadnego dostawcy control tower.** Wszystkie liczby z case studies to materiały
  własne dostawców, bez metodologii i grupy kontrolnej.
- **KSeF / JPK / SENT** nie występują publicznie u żadnego z dziesięciu TMS
  (`CONFIRMED` luka, `04b` porównanie przekrojowe). Leftovery fiskalne PL
  zostają nasze (F1, C1), nie „już jest u lidera MQ”.

**Wniosek, który z tego wynika, jest odwrotny do intuicyjnego.** Te dowody
nie podkopują produktu — **czynią jego oś wartościowszą**. Na rynku, na którym
nikt nie ma niezależnie zaudytowanego wyniku, a wszyscy mają broszury,
**pierwszy rzetelny pomiar sam jest przewagą konkurencyjną**. Dlatego cztery
tabele substratu z części B.2 nie są infrastrukturą pomocniczą — są produktem.
Zdanie sprzedażowe nie brzmi „nasze AI ma 97% dokładności", bo tego nie da się
obronić. Brzmi: **„pokazujemy, ile dokładnie zaoszczędziliśmy, i pokazujemy,
jak to policzyliśmy"** — a tego dziś nie robi nikt.

**Liczby, które wolno używać, bo mają metodę** (`CONFIRMED`, dokument `01` §10.6):
Transporeon z Anheuser-Busch — test A/B przez 45 dni, dwucyfrowa poprawa na rynku
spot, +24 godziny wyprzedzenia. project44 — poprawa czasu przybycia o 28 punktów
procentowych przy oknie 10 godzin ±2 h na ponad 500 przewozach całopojazdowych.
Badania recenzowane o czasie przybycia ze statku: MAE 16,01 h wobec 22,15 h dla
czasu podawanego przez kapitana; stacking LightGBM z XGBoost i lasem losowym —
MAE 3,30 h, czyli −74,7% wobec średniej historycznej.

## D.5 AI Act i RODO

**Klasyfikacja, którą trzeba przyjąć jako fakt, nie jako ryzyko do oszacowania:**
scoring osób i jednoosobowych działalności wpada pod **AI Act załącznik III
pkt 5(b)** jako zastosowanie wysokiego ryzyka, a decyzja podejmowana wyłącznie
automatycznie wobec osoby jest ograniczona **art. 22 RODO**. Sformułowanie
właściciela jest tu najtrafniejsze: „**to nie nasza decyzja, to prawo**".

Z tego wynikają trzy obowiązki wpisane w produkt, nie w politykę:
- **etykieta z art. 50** przy każdej treści wygenerowanej przez model
- **nadzór człowieka z jawnym przeciwdziałaniem automation bias** (art. 14 ust. 4
  lit. b) — dowód konieczności: badanie **Skitka, Mosier, Burdick 1999**, w którym
  badani przyjęli średnio **3,92 z 6** błędnych wskazań systemu (dokładność 35%),
  a **23,1% osób przyjęło wszystkie sześć**
- **program zgodności jako osobny etap planu**, nie jako zadanie poboczne
  (decyzja wiążąca nr 8)

## D.6 Licencje — trzy pułapki wykryte w audycie

Pełna analiza w dokumencie `05` §0. Tu trzy, które realnie zmieniają decyzje
techniczne w produkcie komercyjnym:

1. **AGPL i klauzula użycia sieciowego (sekcja 13).** Biblioteka na AGPL użyta
   w usłudze dostępnej przez sieć pociąga obowiązek udostępnienia kodu.
   **Stan sprawdzony:** PyMuPDF **nie jest** w zależnościach OmniRoute — jedyny
   manifest to `pyproject.toml` i nie ma tam ani `pymupdf`, ani `fitz`, ani
   `pdfplumber`, ani `pypdfium`, ani `pikepdf`. Wyjaśnia to, dlaczego
   `PdfStringsParser` w `backend/app/integrations/docling/parser.py` wyciąga tekst
   z PDF **własnym kodem**. **Pozostaje otwarte:** zależności przechodnie `docling`
   nie zostały sprawdzone. `TO_VERIFY`.
2. **Licencje niekomercyjne i share-alike przy danych** — CC BY-NC-SA wyklucza
   użycie komercyjne, ODbL wymaga udostępnienia bazy pochodnej. Dotyczy części
   zbiorów z dokumentu `10`; dlatego `data_source` ma kolumnę z licencją.
3. **Copyleft w solverach.** Dla planowania tras: **Valhalla na MIT wygrywa
   z openrouteservice i VROOM**, które mają licencje copyleft niewygodne
   w produkcie zamkniętym.

Dodatkowo ustalenie o statusie usterki w kanonie: **`llm-guard` jest projektem
zarchiwizowanym**, a `GROUNDING.md` wskazuje go jako cel twardego wymagania.
To martwy cel i trzeba go zastąpić.

## D.7 Filtr Murphy / GPT / Gemini — brać i nie brać

Źródło książki: badania `18` (Murphy 2026, `[C]` field report). Audyt PDF-ów
ChatGPT / Gemini: `18` §11. „90 % projektów AI pada” = slogan `[C]`, nie fakt.

**Już jest (`CONFIRMED`) — nie otwierać plastra:** HITL + `operator_decision`;
`charge` + `source_ref` = SSoT marży; `GLOSSARY` = Definition Gap; RLS;
`customer_sop` / `task_template`; WIP=1 / jeden plaster; AI9.1 (automation bias).

**Leftover / proces, nie nowy BC:** Grupa 8 (**Plat-HD**, **Mob**);
Love/Hate i Three-Bucket = playbook HHL (`02`), nie tabela; Shadow AI =
proces onboardingu; Closet sprint = `/refaktor` + jeden obszar danych —
**nie** wycinanie 60 % planu.

Pięć jobów z audytu GPT (`REQUIREMENT`, leftover, nie nowy BC, nie 468.0):

1. **Definicja KPI per strona rynku** — ten sam skrót (OTD / OTIF) może mieć
   inną formułę u HHL, klienta, przewoźnika i wieży. `GLOSSARY` pilnuje *naszych*
   nazw. Leftover: słownik definicji z właścicielem i źródłem prawdy; AI nie
   wymyśla wzoru. Nie pasek „72 % readiness”. W PLAN: AI5.0 + wiersz `otif_mark`.
2. **Brama przed L3** — zanim `autonomy_level` wejdzie na 3: jest źródło prawdy,
   właściciel danych, kto łapie wyjątek, rollback, audit. Checklist produktu,
   nie silnik. W PLAN: **AI8.2** (+ AI5.0 przy pierwszym ingestcie).
3. **SOP agenta — jedna strona** — po co jest, jakie dane, read/write, kiedy
   woła człowieka, log, rollback, kto jest właścicielem. `customer_sop` to SOP
   klienta, nie kontrakt agenta. W PLAN: **AI8.2**.
4. **Najpierw ulga, nie sens pracy** — priorytet automatyzacji: to, czego
   operator nienawidzi, nie to, czym jest jego rzemiosło. Zasada kolejki BR/AI,
   nie scoring `Pain × Frequency` w bazie.
5. **Promień wybuchu przed zapisem** — co najgorszego zrobi agent, zanim
   dostanie write. Runbook przy L3. W PLAN: **AI8.2**. Nie Ten-Decisions jako
   silnik.

**`REJECTED`:** Mission Control jako produkt; 40 agentów; Bertha / CoS tenanta;
OMNI READINESS ENGINE jako osobny BC; warstwa semantyczna jako osobny BC;
pgvector na przetargach; Next.js / Astro; Cloudflare AI Gateway jako Q;
RLHF jako silnik; LLM na kwotach / marży; auto-send; drugi SSoT marży.
Cloudflare = bramka publikacji (B.8). Access ≠ Auth0 S53.

## D.8 Badania na `D:\` a kanon w repo

Folder `D:\OMNIROUTE-badania` jest **dowodem** i **surowcem**: pomysły, szkice
wizji, plany, kontrakty, skille, agenci. Nie jest drugim CURRENT.

- **`/noc` busy (`REQUIREMENT`):** pętla plastra, commit, push, CI = to
  repozytorium + GitHub (jak `docs/ops/nocna-zmiana.md`). Nowe notatki
  (plany, wizja, SH, „ulepsz elite”) → tylko badania. Zero promocji do
  kanonu / `.cursor` / `docs/ops`. Nie ładuj `22`–`24` do cyklu.
- **`/noc` idle albo stop (`REQUIREMENT`):** praca produktu (kolejka
  CURRENT, plaster, gate, push) = OmniRoute + GitHub. Badania **nie**
  wlewają się same. Nowy plan, kanon, agent, skill, kontrakt, PROC z
  badań → **tylko** po jawnym poleceniu człowieka („przenieś / zainstaluj
  / zrób kanon z badań”). Sam stop nocy ≠ zgoda. Bez tego zdania: zero
  kopii z badań do repo.

Do `docs/VISION.md` i `docs/PLAN-REALIZACJA.md` wchodzi: `REQUIREMENT` /
`CONFIRMED` / leftover na **istniejącym** ID / świadome `REJECTED`. Nie
wchodzi: zrzut czatu (`99`), eseje vendorów (`03`/`04`/`04b` — zostaje
skrót w A.2), playbook sprzedaży (`02`), metodyka modeli (`05`/`06`),
szkice CURRENT (`14`), kolejka `12-FALA-AI-KOLEJKA.md` (SUPERSEDED),
książka Murphy jako BC (`18`).

**Wyjątek 2026-09-16 (jawne polecenie):** pakiet SH z badań (20 plików
16 IX) → kanon kolejki fabryki [ops/rejestr-wdrozenia-16-ix.md](../ops/rejestr-wdrozenia-16-ix.md)
+ PLAN § Fala SH-R16. Eseje `*-OS.md` / `22`–`24` **nie** są drugim CURRENT;
są **zmapowane** (DONE/NOW/PARK/REJECT). `/noc` nie wczytuje surowca — czyta rejestr + CURRENT.

**22 dostępy P0** z C.1 = katalog `09`/`10`, pierwszy ingest = **AI5.0**,
nie 22 plastry. Zero live HTTP, dopóki CURRENT nie wskaże AI5.

---
---

# CZĘŚĆ E — Roadmapa: kolejność, zależności, bramki

## E.1 Zasada kolejności

Właściciel postawił wymóg: „*każdy kolejny krok ma wynikać z poprzedniego*".
Poniższy łańcuch jest odpowiedzią i **nie jest dowolny** — każda strzałka oznacza
twardą zależność, nie preferencję.

```
charge.source_ref (P0)   [2026-09-13: ogniwo jest w kodzie — 129.0 / 072]
  └─> benefit_ledger — bez pochodzenia kwoty nie ma dowodu oszczędności

entity_event rozszerzony na wszystkie podmioty
  ├─> bliźniak (strumień obserwacji)
  ├─> lane_pattern z każdego zlecenia
  └─> aktywność CRM

suggestion_ledger + outcome_ledger
  ├─> metryki liczone (CRPS, Brier, MAE), nie wpisywane
  ├─> champion/challenger i wykrywanie dryfu
  ├─> benefit_ledger (co uratowano)
  └─> dowód sprzedażowy

PATCH na extraction_draft + edycja w interfejsie
  └─> sygnał uczenia ekstrakcji
        └─> ścieżka "obraz wprost" jako challenger
              └─> pomiar na własnym zbiorze golden
                    └─> bramka wydaniowa na progach

plan_snapshot ze spójnością
  └─> silnik what-if
        └─> symulacja kółek (500k+ w SQL)
              └─> odpowiedź na pytanie typu Gdańsk-Oslo

warstwa ingest danych zewnętrznych
  └─> cechy modelu predykcyjnego
        └─> kaskada skutku dla korporacji (Watch Tower)

telematyka u podwykonawców HHL
  └─> dane kto / gdzie / za ile
        └─> nasycenie silnika stawek spot i kontraktowych
              └─> redukcja pustych przebiegów
                    └─> Watch Tower dla KSH Steel
```

## E.2 Fale — co wchodzi, kiedy się kończy

Fala AI **nie staje obok** istniejących fal V, W, CT i CI. **Podnosi je** —
te fale mają dziś zamknięte katalogi HITL i jawnie wpisane w planie pozycje
„leftover silnik…". Fala AI jest właśnie tym leftoverem, dociągniętym do końca.

Dump CT 2026-09-13 (`03` B.1–B.10; skrót B.4–B.6 w A.2) **potwierdza leftover silników** —
nie otwiera nowych katalogów HITL. Oracle buy/sell jest antywzorcem. p44
`PLANNED` / `ACTUAL` / `ESTIMATE` zasila analog AI1/AI2. Luka `charge` +
`benefit_ledger` u siódemki wzmacnia AI1.3. `charge.source_ref` już jest —
AI0 nie wraca do kolejki.

Dump TMS 2026-09-13 (badania `04b` A–H × 10; CargoWise/Qargo/interLAN w `04`)
**potwierdza leftover silników jako HITL**, nie runtime. VSR / LML /
Optimizer / Archer / what-if u konkurencji to silniki; u nas katalog HITL
+ `suggestion_ledger` (AI1.0 po 431.0). 431.0 `quote_validity_mark` **nie**
wynika z tej dziesiątki. AI-write MQ = zakaz. Druga marża = zakaz.
`charge.source_ref` już jest — AI0 nie wraca.

| Fala | Treść | Warunek wejścia | Warunek zakończenia |
|---|---|---|---|
| **AI0 — pochodzenie** | `charge.source_ref` | [WYCOFANE 2026-09-13 jako „brak, to jest P0": jest w kodzie 129.0 / 072] | **DONE** — nowy INSERT wymaga `source_ref` |
| **AI1 — substrat** | `suggestion_ledger`, `outcome_ledger`, `counterfactual_run`, `benefit_ledger` + cztery słowniki | AI0 | trzy istniejące BC pisze do substratu; test izolacji dla każdej tabeli |
| **AI2 — pomiar** | CRPS, Brier, MAE **liczone** ze złączenia; champion/challenger; dryf | AI1 | `prediction_ledger` przestaje przyjmować wpisaną metrykę; metryka liczy się z danych |
| **AI3 — ekstrakcja** | `PATCH` na szkicu, edycja w UI, wersjonowanie, Excel, ścieżka „obraz wprost" jako challenger, bramka progowa | AI2 (bo bez pomiaru nie ma bramki) | wynik na **własnym** zbiorze golden raportowany; wydanie poniżej progu zablokowane |
| **AI4 — bliźniak i what-if** | `plan_snapshot` spójny, silnik what-if, symulacja kółek w SQL | AI1 | pytanie typu Gdańsk-Oslo dostaje odpowiedź odtwarzalną |
| **AI5 — dane zewnętrzne** | ingest, `data_source` z licencją, cechy modelu | AI1 | pierwsze źródło produkcyjne z zapisaną licencją |
| **AI6 — Watch Tower** | graf skutku biznesowego do marży i gotówki | AI5 + CI (klauzule SLA) | zdarzenie transportowe daje skutek w języku zarządu |
| **AI7 — koszt i CFO** | Cost Allocation Engine, `TRUE CONTRIBUTION MARGIN`, Cyfrowy CFO | AI0 | koszt obsługi klienta policzony, narracja **po** SQL |
| **AI8 — styl i autonomia** | kaskada stylu, `STYLE FIDELITY SCORE`, poziomy 0-5 | AI2 | poziom 2 włączony dla jednego tenanta za bramką |
| **AI9 — zgodność** | etykieta art. 50, rejestr ryzyka, przeciwdziałanie automation bias | równolegle od AI3 | program zgodności zamknięty przed poziomem 3 |

**Brakujące moduły z części C.3** wchodzą **równolegle**, a nie po Fali AI —
bo WMS, telematyka i planowanie nie zależą od substratu pomiarowego, tylko od
osi wejścia na rynek. Kolejność wewnątrz nich wynika z części A.5: telematyka
przed silnikiem stawek, WMS przed strumieniem Trade-Tech.

## E.3 Co pozostaje nierozstrzygnięte

Lista jest krótka, ale każda pozycja blokuje konkretną decyzję projektową.
**Żadnej z nich nie rozstrzygam samodzielnie.**

1. **`HC-04` wobec poziomów autonomii.** [WYCOFANE 2026-09-13: Q1–Q2 —
   `GROUNDING.md` przepisane. L0–2 bez zapisu AI; L3–5 w zapisanych granicach
   + audit; auto-zejście jakości przed L3.]
2. **Klucz obcy w `plan_snapshot`.** [WYCOFANE 2026-09-13: Q3 + 452.0 —
   FK złożone `(organization_id, id)` + `ON DELETE RESTRICT`. CASCADE `REJECTED`.]
3. **Memoryzacja modelu** przy uczeniu międzytenantowym — problem techniczny,
   którego nie rozwiązuje zapis w umowie.
4. **Rozbieżność skali.** [WYCOFANE 2026-09-13: Q11 — dwa horyzonty
   tej samej ścieżki. Q12 — inwestorowi dziś zero liczb skali.]
5. **Koncentracja na jednej grupie kapitałowej** — wolumen kontra dowód rynkowy.
6. **Zależności przechodnie `docling`** — niesprawdzone pod kątem AGPL.
7. **Dwa prompty referencyjne.** [WYCOFANE 2026-09-13: Q13 — pełne wersje
   w badaniach `01b-PROMPTY-REFERENCYJNE.md`.]
8. **Domena produkcyjna** hosta SPA/API pod Cloudflare — nie zapisana
   (`TO_VERIFY`). Bez niej nie ma strefy ani Access.
9. **Czy właściciel ma już konto Cloudflare** — nie potwierdzone
   (`TO_VERIFY`).
10. **Origin produkcyjny** (gdzie granian + SPA + PG) — Hetzner jest tylko
    w historycznym planie fabryki, nie w kanonie (`TO_VERIFY`).
11. **Limit miejsc Zero Trust / Access** na planie, który wybierze właściciel —
    tabela [account limits](https://developers.cloudflare.com/cloudflare-one/account-limits/)
    (2026-09-04) nie podaje liczby miejsc Free; nie zgadywać (`TO_VERIFY`
    w dashboardzie Cloudflare One).
12. **Umowa powierzenia (DPA) z Cloudflare** przed danymi osobowymi tenantów
    na krawędzi — `TO_VERIFY` z prawnikiem; pre-publish Access na e-mailach
    operatora jest węższy niż ruch płacących tenantów.

---

**Koniec wizji, wersja 0.1.** Dokument jest żywy — przy każdym nowym ustaleniu
dopisz treść i wiersz w Dzienniku zmian na początku pliku.

