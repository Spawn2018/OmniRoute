# Weryfikacja wypłacalności JDG — ramy prawne (szkic; TO_VERIFY z prawnikiem przed wdrożeniem)

**Kiedy:** Plan pogłębienia M-14 (kredyt) i M-10 (kontrahent); Fala F6; umowy z wywiadowniami.

## Fakty prawne (stan wiedzy 2026-09; każdy punkt potwierdzić u prawnika)

- JDG = osoba fizyczna prowadząca działalność → **RODO stosuje się** do jej danych,
  ale dane rejestrowe działalności (CEIDG, NIP, biała lista VAT) są jawne.
- Podstawa przetwarzania: **art. 6(1)(f) RODO — uzasadniony interes** (ocena ryzyka
  kredytowego kontrahenta-przedsiębiorcy); wymaga udokumentowanego testu równowagi
  i klauzuli informacyjnej (art. 14) w umowie/regulaminie.
- **Art. 22 RODO:** decyzja kredytowa wobec JDG nie może być wyłącznie
  zautomatyzowana z istotnym skutkiem → recenzja kredytowa ZAWSZE przez człowieka
  (mamy: `credit_review` M-14 + szyna decyzji M-71).
- **AI Act:** scoring zdolności kredytowej osób fizycznych = wysokie ryzyko →
  w OmniRoute ZAKAZ auto-scoringu `natural_person`/JDG (anti-cel w PLAN).
  Dozwolone: deterministyczne fakty + raport wywiadowni + decyzja człowieka.
- **KRD formalnie JEST BIG-iem** (ustawa z 9.04.2010 o udostępnianiu informacji
  gospodarczych). Zapytanie o dłużnika-przedsiębiorcę (w tym JDG w zakresie
  działalności) co do zasady bez zgody dłużnika; dłużnik-konsument wymaga
  upoważnienia (60 dni). Granica konsument/przedsiębiorca przy JDG = TO_VERIFY.
- BIK / systemy bankowe — poza zakresem produktu (decyzja operatora 2026-09-07).

## Dozwolone źródła w OmniRoute

CEIDG · biała lista VAT · REGON/GUS · VIES · wywiadownie handlowe
(KRD, Coface, D&B, CreditSafe — raport = załącznik `bureau_attachment_ref`
do recenzji M-14) · własna historia płatnicza tenanta (bank M-42).

## Zasady produktu (twarde)

1. **Nigdy B2C** — kontrahent bez identyfikatora biznesowego nie istnieje
   w systemie (walidacja przy zapisie; plaster M10-1).
2. Raport wywiadowni = fakt do wglądu, nie automatyczna decyzja.
3. Decyzję kredytową podejmuje człowiek; system podaje fakty i historię.
4. Retencja raportów wg polityki tenanta; sekrety dostępowe wywiadowni
   szyfrowane per tenant (HC-05).
