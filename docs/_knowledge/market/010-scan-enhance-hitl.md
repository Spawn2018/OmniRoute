# Enhance skanu + recenzja split

**Kiedy:** Plan X9. Szczegóły: `docs/analysis/benchmark-tms-2026.md` §13o.

## Jakość (wygląd skanera płaskiego)

Apka: ramka na żywo; Android ML Kit (`BASE_WITH_FILTER` na FV), iOS VisionKit.
Serwer: OpenCV — 4 rogi, deskew, spłaszczenie światła, punkt bieli, Lanczos do ~300 DPI.
Oryginał zostaje. Zakaz GAN i inpaintingu tekstu. `FULL` (plamy/palce) nie na fakturach.

## Recenzja

Docling: bbox + `ocr_grade`. Instructor: pole + `amount_text` + pewność.
Lewo strona z ramkami, prawo wartość / rodzaj / %, edycja = `operator_override`.
Accept tylko człowiek. Jeden ekran: RFQ, FV, cennik, CMR.
