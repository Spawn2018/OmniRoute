# Lejek oferty (otwarcie maila / PDF / odpowiedź)

**Kiedy:** Plan X7. Szczegóły: `docs/analysis/benchmark-tms-2026.md` §13i.

## Sygnały

- `sent` — `mail_draft` (Graph pewniejszy niż mailto).
- `email_opened` — piksel **tylko** przy `tracking_consent` na kontakcie. Apple MPP / skanery fałszują.
- `pdf_viewed` — `GET /q/{token}` hostowanego PDF (główny sygnał; załącznik nie trackuje).
- `replied` — `inbound_message` po wątku / numerze oferty.
- `converted` / `lost` — M-29 / `shipment`.

## Czasy (SQL)

sent→open · sent→pdf · sent→reply · pdf→reply · sent→converted.

## Prawo

Piksel = ePrivacy, zgoda osobna od maila (także B2B). Link kliknięty = świadoma akcja. Bez trackera trzeciej strony. Token wygasa.
