# Leftover U-omniroute-ui-dna · tokeny z makiety sprzedażowej

**Spec źródłowa:** [docs/design/omniroute-ui.html](../../design/omniroute-ui.html)  
**Zależy od:** ADR-0003 + leftover U-oklch-dark (51.0)

**Status:** Otwarty leftover UI. Nie S4. Nie nowa tabela. Nie Watchtower.

## Wybrane / odrzucone / dlaczego

**Wybrane:** `frontend/src/index.css` kopiuje rampę hue **165**, `--s1`…`--s6`, radius 12px/8px i IBM Plex Sans/Mono/Condensed z `docs/design/omniroute-ui.html`. Shell: header 3rem, rail `--ink`. Docs i skill `nowy-plaster` wskazują ten HTML jako DNA.

**Łowca:** ISTNIEJE `index.css` + `.dark`. PODOBNE: `omniroute-briefing-mockup.html` (hue 106) — nie paleta produktu.

**Odrzucone:** kopiowanie markup HTML do `frontend/`; paleta hue 250 z `app-preview.html`; paleta hue 106 z briefingu; mapa / Watchtower.

## Zakres

Tokeny CSS, fonty w `index.html`, kontrast rail w sidebarze, header `h-12` / `px-3`. Dokumentacja DNA.

## Poza zakresem

S4 RFQ · ikonowy rail 3.35rem (żywy katalog ma etykiety) · nowa trasa · k6

## Ustalenia

- Druga paleta poza `index.css` zakazana.
- LLM nie liczy. `<Money/>` zostaje stringiem.
