# Inwentarz funkcjonalny freight forwarding ERP — wsad do budowy

Źródło: publiczna dokumentacja i strony produktowe Shipthis. Dokument opisuje **wymagania funkcjonalne** (funkcje nie podlegają prawu autorskiemu). Nie zawiera i nie może zawierać: ich kodu, layoutu UI, przeklejonych tekstów dokumentacji.

---

## 1. Mapa modułów

### 1.1 Shipments (operacje) — rdzeń
- Dashboard: liczniki zleceń wg okresu, tabela statusów filtrowana po operatorze/kliencie
- Reports: ground freight, taski (pending/due/completed), aktywne zlecenia, raporty klienckie
- Accepted Quotes: zaakceptowane oferty czekające na utworzenie joba
- My Shipments / All Shipments: widok user-specific vs. organizacyjny, edycja danych
- Podział modalny: Air / Sea / Land (osobne widoki, zapisywane filtry)
- Documentation: joby dokumentacyjne powiązane ze zleceniem
- Taski i milestone'y per zlecenie, deadline'y, przypisanie do osób

### 1.2 Quotation (ofertowanie)
- Dashboard: open / sent / lost quotes, zaakceptowane oczekujące na job
- All Quotations: pełna lista zapytań i odpowiedzi
- Quote Tariff Sheet (Group): grupy stawek per klient
- Reports: statystyki ofert, oferty wg handlowca / klienta
- Website quotes (zapytania z formularza WWW)
- Konwersja Quotation → Booking (wybór shipment class + operator)
- Preview oferty, download PDF / XLS, wysyłka mailem
- Import ofert z pliku, audit history oferty

### 1.3 Rate / Tariff Manager
- Freight Rate Manager: stawki morskie FCL/LCL, stawki lotnicze
- Port / Local Rate Manager: opłaty lokalne morskie i lotnicze/portowe
- Transport Rate Manager: cartage / dowóz-odwóz
- Import arkuszy Excel z całymi cennikami
- Macierz stawek per port/lotnisko, pre-leg i post-leg charges
- Charge manager settings (konfiguracja typów opłat)
- Customer-specific charges: stawki dedykowane, auto-podstawiane przy ofercie

### 1.4 Customer / CRM
- Dashboard: klienci po przekroczeniu limitu kredytowego, segmentacja wg performance
- All Customers: CRUD, kontakty, adresy
- Reports: performance, shipments by customer, invoice/payment
- Audit history klienta (cała aktywność od dodania)
- Enable Portal Access dla kontaktu + wysyłka danych logowania
- Customer Performance Measurement / grading rentowności klienta
- Repozytorium dokumentów klienta, historia maili, historia ofert i faktur

### 1.5 Vendors / Agents
- Dashboard z zapisywanymi filtrami
- CRUD vendora, import/eksport
- Costing bills (bille kosztowe vendora)
- Vendor account statement

### 1.6 Sales
- Dashboard: sprzedaż w ujęciu rok/kwartał/miesiąc/tydzień/dzień
- Reports: wg typu klienta, handlowca, marży
- Pipeline: etapy, opportunities, forecast, follow-upy
- Aktywność handlowców w terenie: wizyty, spotkania, wyniki, trasy

### 1.7 Accounting
- Dashboard: pending approvals, aging AR / AP
- Chart of Accounts (aktywa bieżące, trwałe, podatkowe, custom)
- Receivable: faktury, wpłaty klientów, noty kredytowe
- Payable: koszty, costing, płatności vendorów, noty debetowe
- Banking: konta bankowe, wyciągi, transakcje, feed z banku
- Reports: sprzedaż, płatności, fakturowanie, marże
- Settings: waluty, terminy płatności, zapisy księgowe, stawki podatkowe
- Multi-currency, automatyczne przeliczanie kursów

### 1.8 Documents
- Auto-generowanie dokumentów per zlecenie (Generate Documents)
- Preview, Send (mail), Print, Download PDF / Excel
- Upload dokumentów: internal vs. customer-facing
- Konfigurowalne szablony dokumentów

### 1.9 Warehouse / WMS
- Warehouse receipts, przyjęcia, stany magazynowe
- Ruchy towaru, wydania, powiązanie z jobem

### 1.10 Track & Trace
- Śledzenie po numerze BL i numerze kontenera
- Widok mapowy, milestone'y, timestampy, lokalizacje kontenerów
- Auto-eventy w cyklu życia zlecenia, alerty i powiadomienia stron
- Publiczny link trackingowy do przekazania shipperowi

### 1.11 Customer Portal (white-label)
- Dashboard klienta: aktywne zlecenia, wyjątki, statusy
- Request a quote przez portal
- Drag & drop dokumentów wpadających wprost do joba w ERP
- Podgląd faktur, raportów, analityki
- Messaging kontekstowy per zlecenie

### 1.12 Settings / Admin
- Organization: preferencje, logo, regiony, branding
- Users: pracownicy
- Roles: role, uprawnienia, widoczności
- Customize: pola własne na stronach billi, vendorów, faktur
- Workflow engine: workflow per typ zlecenia/płatności/kredytu + taski, eventy, akcje
- Email log
- Add-ons: integracje
- Billing: rozliczenie subskrypcji

### 1.13 Setup (słowniki)
- Porty / lotniska
- Kategorie: typy kontenerów, opakowań, dokumentów, pojazdów
- Shipping: warunki (Incoterms), linie żeglugowe, statki, linie lotnicze

### 1.14 Add-ony / integracje
- EDI, otwarte API, webhooki
- eAWB submission
- Trade / compliance messaging
- Feed bankowy
- Rozliczane transakcyjnie (per użycie), nie w abonamencie

### 1.15 Warstwa AI
- Parsowanie maili RFQ → strukturalne zapytanie ofertowe w systemie
- Automatyzacja dokumentacji
- Boty automatyzujące eventy w cyklu życia zlecenia + alerty

---

## 2. Model domenowy (rdzeń)

```
Organization
 └─ User ─ Role ─ Permission

Party (abstrakcja: Customer | Vendor | Agent | Shipper | Consignee | NotifyParty)
 ├─ Contact
 ├─ Address
 ├─ CreditLimit, PaymentTerms
 └─ CustomerSpecificCharge[]

RateSheet
 ├─ FreightRate    (mode, origin, destination, container/weight break, carrier, validity, currency)
 ├─ LocalCharge    (port/airport, side: origin|destination, applicability)
 └─ TransportRate  (from, to, vehicle type, weight break)

Quotation
 ├─ QuotationLine (chargeCode, basis, qty, buyRate, sellRate, currency)
 ├─ status: draft|sent|accepted|lost|expired
 └─ → Booking

Booking → Shipment (JobFile)
 ├─ jobNumber, mode (AIR|SEA_FCL|SEA_LCL|LAND|RAIL), direction (IMPORT|EXPORT|CROSS)
 ├─ Route ─ Leg[] (carrier, vessel/flight, ETD, ETA, ATD, ATA)
 ├─ Container[] / Package[]  (type, qty, weight, volume, chargeable weight)
 ├─ Milestone[] / Event[]    (code, plannedAt, actualAt, source)
 ├─ Task[]                   (assignee, dueDate, status)
 ├─ Document[]               (type, template, visibility: internal|customer)
 └─ Charge[]                 (chargeCode, buy: vendor+amount, sell: customer+amount, currency, fxRate)

Invoice  (AR)  ← Charge[sell]
Bill     (AP)  ← Charge[buy]
CreditNote / DebitNote
Payment
JournalEntry ─ Account (Chart of Accounts)

Workflow ─ WorkflowStep ─ TriggerRule ─ Action (task|email|statusChange)
AuditLog (entity, entityId, userId, before, after, at)
```

Kluczowa zasada: **Charge to jedyne miejsce prawdy o marży.** Buy i sell na jednym rekordzie, waluta i kurs zamrożone na moment księgowania. Cała rentowność (per job, per klient, per handlowiec, per relacja) liczy się z tej jednej tabeli.

---

## 3. Luka rynkowa — czego tu nie ma, a jest potrzebne w PL

Żaden z powyższych modułów nie obsługuje polskiej specyfiki. To jest przewaga, nie brak:

- **KSeF** — wystawianie i odbiór faktur ustrukturyzowanych, numer KSeF na fakturze
- **JPK_V7M / JPK_KR** — struktury raportowe
- **SENT / PUESC** — zgłoszenia przewozu towarów wrażliwych
- **AIS/AES, NCTS2** — zgłoszenia celne, tranzyt
- **Split payment, biała lista VAT** — walidacja rachunku kontrahenta
- **Kursy NBP** — tabela A z dnia poprzedzającego, do przeliczeń
- **VAT 0% na usługach transportu międzynarodowego** — reguły i dokumentacja dowodowa
- **CMR, list przewozowy** — szablony zgodne z PL/CEE
- **GUS/REGON, VIES** — autouzupełnianie danych kontrahenta po NIP

---

## 4. Sugerowana kolejność budowy

Każda faza kończy się czymś, co da się realnie używać i sprzedać.

**F1 — Ofertowanie (6–8 tyg.)**
Słowniki (porty, kontenery, Incoterms) → Party → RateSheet + import Excela → Quotation z kalkulacją buy/sell → PDF oferty → wysyłka mailem.
*Efekt: przestajesz liczyć oferty w Excelu.*

**F2 — Job file (6–8 tyg.)**
Quotation → Booking → Shipment. Legs, kontenery, milestone'y, taski, statusy, dokumenty z szablonów.
*Efekt: operacja siedzi w systemie zamiast w mailach.*

**F3 — Pieniądze (6–10 tyg.)**
Charge jako rdzeń, faktura AR, bill AP, multi-currency + NBP, KSeF, P&L per job / klient / relacja.
*Efekt: wiesz, gdzie zarabiasz. To jest moduł, który sprzedaje resztę.*

**F4 — AI + portal (8–12 tyg.)**
Parsowanie RFQ z maila → prefill Quotation. Portal klienta: status, dokumenty, faktury, publiczny link trackingowy.
*Efekt: różnica jakościowa vs. konkurencja.*

**F5 — Reszta**
Track & trace (integracje z liniami), WMS, EDI, celne, pełna księgowość.

---

## 5. Decyzje architektoniczne do podjęcia na starcie

1. **Multi-tenancy od pierwszego dnia** — `organization_id` w każdej tabeli + RLS. Doklejenie tego później to przepisanie wszystkiego.
2. **Numeracja dokumentów** — sekwencje per organizacja, per typ, per rok. Musi być transakcyjna i bez dziur.
3. **Waluty** — wszystkie kwoty jako `numeric`, nigdy float. Kurs zamrożony na rekordzie, nie liczony w locie.
4. **Audit log globalny** — trigger na poziomie bazy, nie w kodzie aplikacji.
5. **Workflow engine konfigurowalny, nie hardcodowany** — inaczej każdy nowy klient to nowy deploy.
6. **Księgowość: integrować, nie pisać.** Podwójny zapis, zamknięcia okresów i zgodność z UoR to osobny produkt. API do wFirma / Fakturownia / Comarch daje 90% wartości za 5% pracy.
