# Compliance EU: pogoda, BDO, dokumenty, SENT, myto

**Kiedy:** Plan C6–C9, V2/V2b. Szczegóły: `docs/analysis/benchmark-tms-2026.md` §13h.

## Pogoda

Open-Meteo wzdłuż geometrii `trip` (cała Europa). IMGW/DWD/Météo-France = suplement.

## Odpady

PL: BDO REST (darmowe, `bdo.mos.gov.pl`; test swagger). KPO/KPOK. Kontrakt API zmienia się 1.01.2027.  
UE: DIWASS od 21.05.2026 (WSR 2024/1157) + eFTI. Tranzyt przez PL = też numer BDO.

## Blokada zlecenia

`party_document`: polisa / składka / licencja. 409 gdy wygasło lub `unpaid`. Odblokowanie = nowy ważny wiersz. Historia niemutowalna.

## Trans.eu

Partners API: `overall_rating`, satisfaction, TransRisk, `documents.expire_date`. Komentarze słowne na platformie — endpoint listy **TO_VERIFY**. Nie scrapować.

## Monitoring

Katalog danych. Unia: EMCS, NCTS, DIWASS, eFTI. Naród: SENT, EKAER, BIREG, RO e-Transport. Większość krajów **nie ma** klona SENT.

## Myto

Geometria + pojazd + data → `charge` z `source_ref`. Winieta ≠ km. Brak taryfy = warning.
