# Karty pól — leftover P0 + Fala P (pricing) — SZKIC do `/plan-modul`

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Matching w SQL (wzorzec M-18). Marża zostaje w `charge`. LLM/JS nie liczą.  
**Pełne kolumny wizji:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md). Plan tnie do jednego plastra.

## P0 leftover — `charge.source_ref` (**następny** po pinie)

Tabela `charge` ISTNIEJE (migracja 009). Brak `source_ref` = luka HC-05. V2b i F11 tego wymagają.

| Pole | Typ | Uwagi |
|---|---|---|
| `source_ref` | text | nullable na starych fixture; **NOT NULL** na nowym INSERT (myto, znaczek PP, accept) |

Nie zgadywać numeru migracji. Nie nowa tabela marży.

## P1 — rate card warunkowy

Rozszerzenie wzorca `port_surcharge.applies_when`. WHEN/IF/CALC/MIN/MAX/ważność = **dane**, nie T-SQL per wdrożenie.

## P2 — charge templates

Kolekcje kodów opłat z datami ważności bez nakładania (exclusion / CHECK jak strefy pocztowe).

## P3 — FSC / indeks

Katalog indeksu obok `nbp_rate` (paliwo). Przeliczenie w SQL na `charge`.

## P4 — Local Charge Library

Armator × port × serwis × typ kontenera. Brak dopłaty = **warning**, nie fakt i nie zmyślona kwota. Inne niż O2 (fracht ręczny na lane).

## P5 — expected vs actual

Snapshot kosztu `trip` przy `planned → in_transit`. Wariancja = SQL na `charge`. Nie druga marża.

## P6 — tender quotes

Ważność + limit orderów z oferty. Pogłębienie M-25/M-26/M-29. Nie auto-award.
