# Leftover U-omniroute-ui-dna · tokeny z ekranów Wyceny i Zlecenia

**Spec źródłowa:** [docs/design/omniroute-ui.html](../../design/omniroute-ui.html) — tylko `#v-quote` i `#v-ship`  
**Zależy od:** ADR-0003 + leftover U-oklch-dark (51.0)

**Status:** Otwarty leftover UI. Nie S4. Nie nowa tabela. Nie Watchtower.

## Wybrane / odrzucone / dlaczego

**Wybrane:** DNA = dopracowane **Wyceny** i **Zlecenia** w `docs/design/omniroute-ui.html` (`#v-quote`, `#v-ship`). `frontend/src/index.css` mapuje hue **165**, `--s1`…`--s6`, radius 12px/8px i IBM Plex z tych widoków. Żywy kod: `frontend/src/features/quotations/catalog-page.tsx`, `frontend/src/features/shipment/catalog-page.tsx`. Shell: header 3rem, rail `--ink`.

**Łowca:** ISTNIEJE `frontend/src/index.css` + `.dark`. PODOBNE: `docs/design/omniroute-briefing-mockup.html` (hue 106) — nie paleta.

**Odrzucone:** cały katalog M-01…M-212 jako kanon; kopiowanie markup HTML; paleta hue 250 z `docs/design/app-preview.html`; paleta hue 106 z briefingu; mapa / Watchtower.

## Zakres

Tokeny CSS, fonty w `index.html`, kontrast rail w sidebarze, header `h-12` / `px-3`. Dokumentacja DNA.

## Poza zakresem

S4 RFQ · ikonowy rail 3.35rem (żywy katalog ma etykiety) · nowa trasa · k6

## Ustalenia

- Druga paleta poza `index.css` zakazana.
- LLM nie liczy. `<Money/>` zostaje stringiem.
