---
name: omniroute-investor-business
description: >-
  Model pięciu strumieni, GTM HHL/KSH, zakaz liczb skali dla inwestora
  (VISION Q12), luki konkurencji ze statusem. Używaj przy pitchu,
  GTM, Trade-Tech, Watch Tower vs TSL, gdy pada inwestor, wycena, HHL, KSH.
---

# Biznes tylko z kanonu

Źródło nadrzędne: `docs/VISION.md` A.4–A.6, A.2, E.3. Surowiec: badania `01`, `02`, `03`, `04`, `04b` — cytuj ze statusem, nie zgaduj vendorów spoza tych plików i VISION.

## Pięć strumieni (`CONFIRMED` treść, `01` §16.3)

1. Licencja SaaS — dwie skóry: TSL i Watch Tower.
2. Telematyka (OmniTelematics) — `tracking_event` **nie jest** GPS; pozycja = `position_event`.
3. Trade-Tech — PO Financing, Inventory Release, zastaw w magazynie Zbrudzewo; partner osi: SMEO. WMS jest warunkiem zastawu. Dump `04b` (Manhattan / Infios / SAP EWM) **nie** otwiera live yard / T8.
4. Dane i benchmark — przełącznik zakresu uczenia; ryzyko prawne D.2.
5. Wdrożenia i partnerzy — studium `11` (HubSpot / Salesforce).

Liczby w A.4 to **symulacja właściciela, nie prognoza zwalidowana**. Tak je podpisuj.

## Q12 — inwestorowi zero liczb skali

`docs/VISION.md` E.3 pkt 4: [WYCOFANE 2026-09-13: Q11 dwa horyzonty; **Q12 — inwestorowi dziś zero liczb skali**].

W materiale dla inwestora **nie podawaj** 29,2 mln PLN, 147 mln PLN, „setek milionów EUR” jako obietnicy. Wolno cytować, że kanon **wycofał** te liczby ze slajdu inwestorskieego i zostawił rozbieżność jako historię decyzji.

## GTM HHL / KSH (`CONFIRMED`, decyzja 10, dokument `02`)

H&H Logistics (Zbrudzewo) = pierwszy klient, skóra TSL → telematyka dla podwykonawców HHL → dane korytarzy → KSH Steel = pierwszy Watch Tower → SMEO.

Ryzyko `TO_VERIFY`: „LOGMAR i HHL to klient zero, nie referencja”. Grupa ≠ dowód rynkowy.

Konflikt GTM Uber Freight: `REQUIREMENT`, `04b` §8.H — ta sama oś „kto jeździ gdzie i za ile”; u nas katalog HITL, nie live CT/GPS.

## Konkurencja — tylko 03 / 04 / 04b / VISION

Każda luka: vendor + zdanie z pliku + `CONFIRMED` / `TO_VERIFY` / `REJECTED` / **NIE POTWIERDZONE**.

Stałe z A.2 / A.6 (nie rozszerzaj listy): dwie skóry vs p44/LSP44; Qargo bez załadowcy; CargoWise ≠ control tower; e2open ≠ CargoWise; Navisphere nie ISV; drugi magazyn marży `REJECTED`; klon Oracle TM `REJECTED`; sieć 94 tys. Infor Nexus `REJECTED`.

Schemat bliźniaka FourKites w publicznym API: **NIE POTWIERDZONE** (VISION / `03`). Nie obiecywać.

## Zakaz

97% ekstrakcji, runtime Temporal/Hatchet jako fakt, live T8/WMS, druga marża, liczby skali na slajdzie inwestora.
