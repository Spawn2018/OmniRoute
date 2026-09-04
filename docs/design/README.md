# Makiety UI OmniRoute

**ADR:** [0003](../adr/0003-frontend-ui-system-2026.md) (uzupełnia 0002).  
**Nie kod produktu.** Nie bundel Vite.

## DNA wizualne

Źródło wyglądu produktu (kolory, spacing, padding, radius, typografia, elementy):
dopracowane ekrany **Wyceny** i **Zlecenia** w [omniroute-ui.html](omniroute-ui.html)
(`#v-quote`, `#v-ship`) — nie cały katalog sprzedażowy M-01…M-212, nie Watchtower, nie mapa.

Żywy kod tych dwóch obiektów: `frontend/src/features/quotations/catalog-page.tsx`
i `frontend/src/features/shipment/catalog-page.tsx`. Tokeny w `frontend/src/index.css`
mapują z tych widoków: OKLCH hue **165**, `--s1`…`--s6` (4–24px), `--radius` 12px /
`--radius-sm` 8px, IBM Plex Sans / Mono, rail `--ink` / `--on-ink` (sidebar aliasuje te
tokeny), pasek `.banner` z przejściem
`linear-gradient(120deg, oklch(.32 .06 165), oklch(.42 .1 165))`. Condensed tylko przy
gęstości katalogu `rate_line`.
Nowy ekran używa zmiennych, nie wpisuje OKLCH z palca. Kwoty: `<Money/>`, zero `sum()` w JS.

Klatki [oferta](screens/omniroute-oferta-light.png) i [zlecenie](screens/omniroute-zlecenie-light.png)
ilustrują te dwa ekrany. Render historyczny z [app-preview.html](app-preview.html) — nie paleta
(chrom leftover, hue 250; akcent 165).

**Nie kanon palety:** [omniroute-briefing-mockup.html](omniroute-briefing-mockup.html)
(stara rampa hue 106, radius 0.375rem). [app-preview.html](app-preview.html) zostaje leftoverem
ADR-0003 (układ rail + szyna), nie DNA koloru.

**Reszta [omniroute-ui.html](omniroute-ui.html)** (M-01…M-212, Stawki, HITL, Watchtower):
podgląd sprzedażowy, nie plaster kolejki, nie drugi kanon. Katalog: [omniroute-ui-catalog.js](omniroute-ui-catalog.js).

**Kanon leftoverów ADR-0003:** [app-preview.html](app-preview.html) — układ rail + powierzchnia + prawa szyna, tokeny OKLCH (zieleń hue 165), tenant w topbarze, HITL, kwoty jako string z „serwera” (zero `sum()` w JS). Otwórz w przeglądarce, nie w Canvas IDE. Nie jest paletą produktu.

Canvas IDE dziedziczy kolory edytora i wygląda jak dokument, nie jak aplikacja.

Statyczne klatki (1480 × 940, render z `app-preview.html`):
[oferta jasna](screens/omniroute-oferta-light.png) · [oferta ciemna](screens/omniroute-oferta-dark.png) ·
[stawki jasne](screens/omniroute-stawki-light.png) · [stawki ciemne](screens/omniroute-stawki-dark.png) ·
[HITL](screens/omniroute-hitl-light.png) · [zlecenie](screens/omniroute-zlecenie-light.png).

Klatki leftoverów ADR-0003 zostają źródłem układu dla **U-oklch-dark** (elewacja w obu motywach),
**U-money-align** (siatka integer / fraction / ISO 4217) i **U-condensed** (tryb gęsty wyłącznie na katalogu `rate_line`). Paleta produktu = Wyceny/Zlecenia, nie te klatki.

| Plik | Ekran |
|---|---|
| [ui-01-foundations.canvas.tsx](ui-01-foundations.canvas.tsx) | Tokeny OKLCH, trzy gęstości, Money, status, fokus |
| [ui-02-shell.canvas.tsx](ui-02-shell.canvas.tsx) | Shell bar, tenant, ⌘K, motyw |
| [ui-03-data-grid.canvas.tsx](ui-03-data-grid.canvas.tsx) | Grid stawek, pin, source_ref, superseded_by |
| [ui-04-hitl.canvas.tsx](ui-04-hitl.canvas.tsx) | HITL PDF / confidence / accept / odrzucenie |
| [ui-05-quotation.canvas.tsx](ui-05-quotation.canvas.tsx) | Warianty oferty i wiersz `charge` |
| [ui-06-vision.canvas.tsx](ui-06-vision.canvas.tsx) | Watchtower / oś / portale — **bez backendu** |

Implementacja w `frontend/` tylko przez leftover **U-oklch-dark** … **U-print** w [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Nie Q1.
**2026-09-02:** makieta ujednolicona pod język Wyceny/Zlecenia; ekrany FE: Stawki, Opłaty, Ekstrakcje, Kontrahenci, Porty, Lokalizacje, Oferty kanału, Użytkownicy. Nie kod produktu.
