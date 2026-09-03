# S21 · park live HTTP kanału (M-19)

**Spec źródłowa:** [docs/PLAN-REALIZACJA.md](../../PLAN-REALIZACJA.md) § Kolejka S21  
**Zależy od:** 13.0 `channel_quote`

**Status:** Zaparkowane `/noc` 2026-09-03. Zero kodu produktu. Nie F9.1.

## Wybrane / odrzucone / dlaczego

**Wybrane:** PLAN: live HTTP **tylko przy umowie**. W repo i CURRENT **nie ma** umowy kanału armatora (brak adaptera, sekretu tenanta, specyfikacji API). Więc S21 = park. Katalog 13.0 zostaje. 83.0 `carrier_inquiry` zostaje śladem kupna bez HTTP.

**Łowca:** ISTNIEJE 13.0 `channel_quote` (ręczny katalog). BRAK umowy / httpx w `channel_quotes`. PODOBNE: Graph/IMAP ingest miały `source_ref` i leftover live — tu nawet tego nie ma.

**Odrzucone:**

- Teatr HTTP (`httpx` do zmyślonego URL, mock „live”).
- Sekrety w kodzie.
- F9.1 · Auth0 · portale.

## Zakres

Aktualizacja kolejki: S21 parked. Następny S22.

## Poza zakresem

Adapter armatora · sekrety · Temporal · F9.1

## Ustalenia

- S21 wraca, gdy CURRENT wskaże umowę (nazwa kanału + kontrakt).
- How-to bez zmian.

## Kryteria akceptacji

- [x] Zero `httpx` / live client w tym commicie
- [x] S22 jest następnym wierszem kolejki

## Pytania

Brak. `/noc` akceptuje park.
