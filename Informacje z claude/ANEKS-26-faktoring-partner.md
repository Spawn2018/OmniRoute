# Aneks 26 — Finansowanie z partnerem faktoringowym

Zmiana założenia: usługę świadczy zewnętrzna firma faktoringowa.
Ty jesteś platformą i źródłem danych.

---

# 1. CO SIĘ ZMIENIA

| | Faktoring własny | Z partnerem |
|---|---|---|
| Status instytucji obowiązanej AML | tak | **nie** |
| Kapitał obrotowy | konieczny | **zerowy** |
| Ryzyko kredytowe | twoje | **partnera** |
| Wycena ryzyka i rezerwy | twoje | partnera |
| Windykacja przy braku spłaty | twoja | partnera |
| Przychód | odsetki i prowizje | **prowizja za pozyskanie i dane** |

**Odpada niemal wszystko, co odradzałem.** Zostają cztery rzeczy do przemyślenia,
opisane w sekcji 6.

---

# 2. TRZY RÓŻNE PRODUKTY

To jest kluczowe rozróżnienie. Twoje dwa zdania z poprzedniej wiadomości
opisują dwa różne produkty finansowe, a trzeci warto dołożyć.

## 2.1 Faktoring wierzytelności — dla twojego klienta

Klient sprzedaje faktorowi swoje faktury wystawione odbiorcom. Dostaje
zaliczkę, faktor ściąga należność.

```
Twój klient (spedytor) → faktura → jego odbiorca
                       ↓
                    faktor płaci zaliczkę
```

- **kto płaci:** faktor
- **kto zarabia:** faktor (dyskonto), ty (prowizja)
- **korzyść klienta:** gotówka teraz zamiast za 60 dni
- **ryzyko:** cesja wierzytelności, zakaz cesji w umowach

## 2.2 Faktoring odwrotny — dla podwykonawców klienta

Podwykonawca dostaje zapłatę wcześniej od faktora, klient płaci faktorowi
w wydłużonym terminie.

```
Podwykonawca → faktura → twój klient
             ↓
          faktor płaci podwykonawcy wcześniej
             ↓
          klient płaci faktorowi później
```

- **kto płaci:** faktor
- **kto zarabia:** faktor
- **korzyść klienta:** wydłużony termin, poprawa cyklu gotówkowego
- **korzyść podwykonawcy:** gotówka od ręki, bez własnej zdolności kredytowej
- **uwaga:** klient tutaj **nie zarabia**, tylko zyskuje termin

## 2.3 Dynamiczne dyskonto — to, co opisałeś

Klient płaci podwykonawcy wcześniej **z własnych środków**, w zamian za rabat,
który sam ustala.

```
Podwykonawca → faktura → twój klient
             ↓
          klient płaci wcześniej ze swojej gotówki, z upustem
```

- **kto płaci:** klient
- **kto zarabia:** **klient** — i to jest to, o co ci chodziło
- **regulacyjnie:** najlżejsze, brak cesji, brak finansowania przez osobę trzecią
- **ograniczenie:** działa tylko przy nadwyżce gotówki u klienta

## 2.4 Model hybrydowy — rekomendowany

Połącz 2.2 i 2.3 w jeden program. Podwykonawca widzi jedną ofertę,
źródło finansowania rozstrzyga się w tle.

```
Podwykonawca prosi o wcześniejszą zapłatę
        ↓
Klient ma wolną gotówkę w budżecie dnia?
   TAK → płaci sam, zgarnia całe dyskonto        (dynamiczne dyskonto)
   NIE → wchodzi faktor, klient dostaje termin   (faktoring odwrotny)
```

**Dla podwykonawcy doświadczenie jest identyczne.** Dla klienta — zarabia,
gdy ma czym, i nie traci możliwości, gdy nie ma. Dla ciebie — jeden moduł
obsługuje oba scenariusze i w obu masz przychód.

To jest projekt, którego nie ma na polskim rynku w segmencie MŚP.

---

# 3. MODEL DANYCH

```sql
finance_partner
  id, name, kind,              -- factor | bank | fintech
  products text[],             -- receivables | reverse | dynamic_discount
  api_endpoint, auth_method, credentials_encrypted
  min_invoice, max_invoice, currencies text[]
  advance_rate_pct, fee_structure jsonb
  decision_sla_hours
  our_commission_model jsonb   -- stała, procent, wg wolumenu
  agreement_ref, valid_from, valid_to

finance_program                -- program uruchomiony u tenanta
  id, organization_id, partner_id
  product,                     -- receivables | reverse | dynamic_discount | hybrid
  is_active
  eligible_debtors uuid[],     -- przy odwrotnym: kto jest kotwicą
  eligible_suppliers uuid[]
  limit_total, limit_per_debtor, currency
  discount_formula jsonb,      -- przy dyskoncie: stawka za dzień
  daily_budget,                -- ile klient chce wydać dziennie z własnej gotówki
  auto_offer bool,             -- czy propozycja idzie automatycznie
  approval_policy_id

finance_request
  id, program_id
  invoice_id NULL, bill_id NULL
  requested_by,                -- customer | supplier | auto
  requested_at, requested_amount, requested_date
  eligibility_score, eligibility_details jsonb
  status,                      -- draft | eligible | rejected_internal
                               -- sent_to_partner | offered | accepted
                               -- funded | settled | expired
  funding_source               -- partner | buyer_own_cash

finance_offer
  id, request_id, source
  advance_amount, discount_amount, net_amount
  fee_partner, fee_ours, benefit_to_buyer
  effective_annual_rate
  valid_until, presented_at
  accepted_at, accepted_by

finance_settlement
  id, offer_id
  funded_at, funded_amount
  repayment_due, repaid_at, repaid_amount
  our_commission_amount, our_commission_invoiced_at
  status
```

---

# 4. SILNIK KWALIFIKACJI — TU JEST TWOJA PRZEWAGA

Faktor widzi fakturę. Ty widzisz zlecenie, dokumenty, potwierdzenie dostawy
i historię płatniczą dłużnika. **To pozwala odsiać złe wnioski przed wysłaniem
i negocjować lepszą prowizję.**

```sql
receivable_eligibility
  invoice_id, computed_at

  -- twarde wykluczenia
  assignment_allowed bool,        -- ⚠ zakaz cesji z umowy (M-93)
  has_active_dispute bool,        -- spór z M-41
  is_credit_noted bool,
  debtor_is_related_party bool,   -- podmiot powiązany — faktorzy wykluczają
  debtor_sanctions_hit bool,      -- z M-53

  -- jakość dokumentacji
  delivery_confirmed bool,        -- POD z M-89
  documents_complete bool,        -- z M-205
  shipment_closed bool,

  -- jakość dłużnika
  debtor_credit_score,            -- z M-14
  debtor_dso_actual,              -- z M-43
  debtor_payment_reliability,
  debtor_open_exposure,

  -- wynik
  eligibility_score, recommendation, blocking_reasons text[]
```

**Cztery wykluczenia twarde, które musisz sprawdzać przed wysłaniem do faktora:**

**Zakaz cesji.** Umowa klienta z jego odbiorcą zakazuje przelewu wierzytelności —
faktoring tej faktury jest nieskuteczny. Dane masz w rejestrze umów.

**Spór.** Faktura kwestionowana albo z niezamkniętą rozbieżnością nie nadaje się
do finansowania. Dane masz z modułu rozliczeń.

**Brak potwierdzenia dostawy.** Faktor będzie go żądał. Jeśli nie masz POD,
wniosek wróci — lepiej odsiać wcześniej.

**Podmiot powiązany.** Faktura między spółkami tego samego właściciela
jest zwykle wykluczona. Dane masz z grup kapitałowych.

**Wartość dla ciebie:** wysyłasz do faktora wnioski o wysokiej jakości.
Wskaźnik akceptacji rośnie, a to jest argument w rozmowie o prowizji.

---

# 5. INTEGRACJA Z PARTNEREM

```sql
finance_partner_message
  id, partner_id, request_id
  direction, message_type,     -- application | decision | funding
                               -- repayment | dispute | statement
  payload jsonb, sent_at, acknowledged_at
  status, error
```

**Przepływ:**

```
[1] Faktura wystawiona → silnik kwalifikacji → wynik
[2] Kwalifikuje się? → propozycja dla klienta w interfejsie
[3] Klient akceptuje → wniosek do faktora przez API
      + faktura + POD + B/L + dane dłużnika + ocena
[4] Decyzja faktora → prezentacja warunków klientowi
[5] Akceptacja → uruchomienie → zapis w finance_settlement
[6] Powiadomienie o cesji do dłużnika (jeśli jawna)
[7] Spłata → rozliczenie → twoja prowizja
```

**Wszystko przez outbox z idempotencją** — to są operacje finansowe,
duplikat wniosku jest problemem.

**Uzgodnienia z partnerem przed integracją:**

```
□ format wymiany: API czy pliki
□ jakie dokumenty w komplecie wniosku
□ czas decyzji i sposób powiadomienia
□ obsługa cesji: jawna czy cicha, kto powiadamia dłużnika
□ co przy spornej fakturze albo korekcie
□ raport spłat: kiedy i w jakim formacie
□ rozliczenie twojej prowizji: od wniosku, uruchomienia czy spłaty
□ wyłączność czy możliwość wielu partnerów
□ SLA i procedura eskalacji
```

**Punkt o wyłączności jest istotny.** Model wielu partnerów pozwala pokazać
klientowi konkurencyjne oferty i podnosi twoją wartość jako platformy —
ale partner będzie chciał wyłączności. To jest negocjacja, nie techniczna decyzja.

---

# 6. CZTERY RZECZY, KTÓRYCH NADAL PILNUJ

**① Ujawnienie prowizji.** Klient ma wiedzieć, że zarabiasz na skierowaniu.
Zapis w regulaminie i widoczna informacja przy ofercie. Konflikt interesów
ujawniony przestaje być konfliktem.

**② Odpowiedzialność za dane.** Przekazujesz faktorowi dane, na podstawie
których podejmuje decyzję. Umowa z partnerem musi jasno mówić, że
dostarczasz dane „takie, jakie są", a ocena ryzyka należy do niego.
Bez tego przy złym długu poszukają odpowiedzialnego.

**③ Powierzenie danych.** Przekazujesz dane osobowe i handlowe osobie trzeciej.
Umowa powierzenia z faktorem, zgoda klienta, informacja w polityce prywatności,
wpis do rejestru podprzetwarzających.

**④ Powiązanie kapitałowe.** Jeśli firma faktoringowa jest z tobą powiązana,
dochodzą ceny transferowe i obowiązek ujawnienia wobec klienta.

---

# 7. MODEL PRZYCHODU

| Produkt | Twój przychód | Uwaga |
|---|---|---|
| Faktoring wierzytelności | prowizja od uruchomionej kwoty | negocjowana z partnerem |
| Faktoring odwrotny | prowizja od wolumenu programu | zwykle niższa stawka, większy wolumen |
| Dynamiczne dyskonto | **udział w zrealizowanym dyskoncie** albo opłata za moduł | tu partner nie uczestniczy — przychód w całości twój |
| Moduł jako funkcja | abonament dodatkowy | patrz cennik |

**Dynamiczne dyskonto jest twoim najlepszym produktem finansowym**, bo nie
dzielisz się z nikim. Klient płaci własną gotówką, ty dostarczasz mechanizm.
Udział w dyskoncie rzędu kilkunastu procent jest do obrony, bo klient zarabia
resztę na kapitale, który i tak leżał na rachunku.

---

# 8. CO ZBUDOWAĆ I W JAKIEJ KOLEJNOŚCI

| Etap | Zakres | Dni |
|---|---|---|
| 1 | Silnik kwalifikacji wierzytelności | 5 |
| 2 | **Dynamiczne dyskonto — pełny moduł** | 10 |
| 3 | Portal podwykonawcy: widok faktur i wybór terminu | 4 |
| 4 | Integracja z partnerem: wnioski i decyzje | 8 |
| 5 | Faktoring wierzytelności — pełna ścieżka | 6 |
| 6 | Faktoring odwrotny | 5 |
| 7 | Model hybrydowy: automatyczny wybór źródła | 4 |
| 8 | Rozliczanie prowizji i raportowanie | 3 |

**45 dni. Moduły M-207 (faktoring z partnerem) i M-208 (dyskonto)
rozbite na osiem plastrów.**

## Zacznij od etapu 2, nie od 4

Dynamiczne dyskonto nie wymaga partnera, nie wymaga integracji, nie wymaga
ustaleń umownych. Możesz je uruchomić u pierwszego klienta w dziesięć dni
i zobaczyć, czy podwykonawcy z niego korzystają.

**Jeśli korzystają — masz dowód popytu przed rozmową z faktorem, a to jest
najlepsza pozycja negocjacyjna.** Jeśli nie korzystają, dowiedziałeś się
o tym za dziesięć dni pracy zamiast po integracji z partnerem.

## Silnik kwalifikacji buduj pierwszy niezależnie od wszystkiego

Ocena, które należności są zdrowe, a które ryzykowne, jest wartościowa sama
w sobie — nawet gdyby żaden produkt finansowy nie powstał. Pokazuje klientowi,
gdzie ma pieniądze zagrożone, i zasila limity kredytowe z M-14.
