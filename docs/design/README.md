# Makiety UI OmniRoute

**ADR:** [0003](../adr/0003-frontend-ui-system-2026.md) (uzupełnia 0002).  
**Nie kod produktu.** Nie bundel Vite.

## DNA wizualne przy plasterze UI

Źródło wyglądu (kolory, radius, spacing, padding, typografia) — nie markup, nie zakres kolejki:

1. [omniroute-briefing-mockup.html](omniroute-briefing-mockup.html) — ekrany **Wyceny** i **Zlecenia**.
2. Tokeny w `frontend/src/index.css` (hue tła ~106, akcent zieleń ~170, `--radius: 0.375rem`). Nowy ekran używa tych zmiennych, nie wpisuje OKLCH z palca.
3. Żywy kod: `frontend/src/features/quotations/catalog-page.tsx` i `frontend/src/features/shipment/catalog-page.tsx`.

Skala z mockupu: powierzchnia `p-4 gap-4`; panel `p-3` + obramowanie 1px + `rounded-md` + `bg-card`; kontrolki `h-8`; body `text-sm`; meta i tabela `text-xs`; sidebar 11rem; header 2.5rem. Kwoty: `<Money/>`, zero `sum()` w JS.

**Nie** brać palety z [omniroute-ui.html](omniroute-ui.html) (sprzedaż, hue-165) ani z [app-preview.html](app-preview.html) (leftover ADR, hue 250). Nie kopiować HTML. Nie dorysowywać Watchtower / mapy.

**Podgląd sprzedażowy (klikalny, M-01…M-212):** [omniroute-ui.html](omniroute-ui.html) — nie kod produktu, nie plaster kolejki. Katalog: [omniroute-ui-catalog.js](omniroute-ui-catalog.js).

**Kanon leftoverów ADR-0003:** [app-preview.html](app-preview.html) — układ rail + powierzchnia + prawa szyna, tokeny OKLCH (zieleń hue 165), tenant w topbarze, HITL, kwoty jako string z „serwera” (zero `sum()` w JS). Otwórz w przeglądarce, nie w Canvas IDE. Nie jest paletą produktu.

Canvas IDE dziedziczy kolory edytora i wygląda jak dokument, nie jak aplikacja.

Statyczne klatki (1480 × 940, render z `app-preview.html`):
[oferta jasna](screens/omniroute-oferta-light.png) · [oferta ciemna](screens/omniroute-oferta-dark.png) ·
[stawki jasne](screens/omniroute-stawki-light.png) · [stawki ciemne](screens/omniroute-stawki-dark.png) ·
[HITL](screens/omniroute-hitl-light.png) · [zlecenie](screens/omniroute-zlecenie-light.png).

Kanon jest źródłem dla leftoverów **U-oklch-dark** (rampy i elewacja w obu motywach),
**U-money-align** (siatka integer / fraction / ISO 4217) i **U-condensed** (tryb gęsty wyłącznie na katalogu `rate_line`).

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
