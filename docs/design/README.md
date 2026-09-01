# Makiety UI OmniRoute

**ADR:** [0003](../adr/0003-frontend-ui-system-2026.md) (uzupełnia 0002).  
**Nie kod produktu.** Nie bundel Vite.

**Kanon wizualny:** [app-preview.html](app-preview.html) — układ rail + powierzchnia + prawa szyna (wzorzec z makiety Claude), tokeny OKLCH OmniRoute (zieleń, nie niebieski SaaS), tenant w topbarze, HITL, kwoty jako string z „serwera” (zero `sum()` w JS). Otwórz w przeglądarce, nie w Canvas IDE.

Canvas IDE dziedziczy kolory edytora i wygląda jak dokument, nie jak aplikacja.

Statyczne klatki: [screens/omniroute-stawki-light.png](screens/omniroute-stawki-light.png), [screens/omniroute-hitl-light.png](screens/omniroute-hitl-light.png), [screens/omniroute-oferta-light.png](screens/omniroute-oferta-light.png).

| Plik | Ekran |
|---|---|
| [ui-01-foundations.canvas.tsx](ui-01-foundations.canvas.tsx) | Tokeny OKLCH, trzy gęstości, Money, status, fokus |
| [ui-02-shell.canvas.tsx](ui-02-shell.canvas.tsx) | Shell bar, tenant, ⌘K, motyw |
| [ui-03-data-grid.canvas.tsx](ui-03-data-grid.canvas.tsx) | Grid stawek, pin, source_ref, superseded_by |
| [ui-04-hitl.canvas.tsx](ui-04-hitl.canvas.tsx) | HITL PDF / confidence / accept / odrzucenie |
| [ui-05-quotation.canvas.tsx](ui-05-quotation.canvas.tsx) | Warianty oferty i wiersz `charge` |
| [ui-06-vision.canvas.tsx](ui-06-vision.canvas.tsx) | Watchtower / oś / portale — **bez backendu** |

Implementacja w `frontend/` tylko przez leftover **U-oklch-dark** … **U-print** w [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Nie Q1.
