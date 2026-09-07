# interLAN SPEED — wzorce formularzy i finansów PL

**Kiedy:** karty pól (kontener, stop, kurs wg daty), Fala D/F.

## Zlecenie = buy + sell na jednym ekranie

Fracht zleceniodawcy (sprzedaż) i fracht przewoźnika (kupno) na jednym
zleceniu, każdy z własną walutą, tabelą kursów, terminem płatności i VAT
(kraj / UE / poza UE). „Marża z faktur" vs „Marża z kalk." = dokładnie
nasz model `charge` (M-08) + rozliczenie (M-41).

## Kurs wg daty (wymóg PL)

Tabela kursu wybierana wg daty: ETD / data załadunku / **−1 dzień roboczy**
(NBP D-1, art. 31a ustawy o VAT); tabele NBP-A/B; typ kursu średni.
OmniRoute: polityka `fx_rate_basis` na opłacie, przeliczenie w SQL (T7).

## Kontener (najbogatszy publiczny formularz)

ISO 6346 z walidacją cyfry kontrolnej, typ/rozmiar + TEU, 3 plomby, PIN,
HBL/MBL, terminal pobrania pełnego / złożenia pustego + daty, gate-in,
demurrage/detention/MIX D/D, reefer + temp. min/max + zasilanie,
VGM/TARA, ref 1–5, „zwolnienie kontenera dla". Karta: `karty-pol-fala-t.md` § T3.

## Podzlecenia

Pole „Zlecenie główne"; rentowność ZM pokazuje osobno przychód/koszt
z podzleceń; wynik spływa na zlecenie główne. → T4.

## Anty-wzorzec

Cenniki = ręczne procedury T-SQL per wdrożenie (tabele `zz_XXXX`,
pola z tabel PRZESYLKI/PACZKI) — każde wdrożenie to dialekt. U nas:
konfiguracja jako dane (M-03) + matching w SQL (wzorzec M-18).
