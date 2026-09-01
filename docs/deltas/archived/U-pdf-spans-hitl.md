# U-pdf-spans — viewer PDF + spany HITL, lazy pdf.js

**Status:** archived 2026-09-01  
**Moduł:** M-20 UI  
**Spec:** PROGRAM-12M standing #8 · Exit Wave FE U-pdf-spans

## Zakres

- Podgląd HITL: `<mark>` na tokenach kandydata (code / amount / currency)
- Gdy operator wgrał PDF w sesji: strona pdf.js + overlay spanów z warstwy tekstu
- `React.lazy` + `import("pdfjs-dist")` — nie w initial JS
- Brak OCR; brak zapisu PDF w backendzie (draft ma `input_text`)

## Poza zakresem

OCR, persist dokumentu, Exit Wave FE

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | highlight + viewer; pdf.js poza initial |
| Szybkość | PRZESZŁO | initial ~125 kB gzip; pdf.js chunk osobny |
| Dług w diffie | OK | lazy viewer; bez teatrów OCR |
| Docs/OS | PRZESZŁO | CURRENT = U-admin-ref; nie Exit Wave FE |
