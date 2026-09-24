# M-55 reklamacja ładunku — tabela `cargo_claim`

**Moduł żywy:** M-55 (token `cargo_claim`)  
**Plaster:** **645.0** (zamknięty; 191.0 OS&D; 113.0 nagłówek)  
**Status:** operator zapisuje reklamację na zleceniu z OS&D, terminami CMR i evidence HITL. Nie kwota. Nie scoring. Nie silnik 7/21/365. Nie live GPS.

Delta 113.0: [docs/deltas/archived/113.0-cargo-claim.md](../deltas/archived/113.0-cargo-claim.md).  
Delta 191.0: [docs/deltas/archived/191.0-cargo-claim-cmr.md](../deltas/archived/191.0-cargo-claim-cmr.md).  
Delta 645.0: [docs/deltas/archived/645.0-cargo-claim-evidence.md](../deltas/archived/645.0-cargo-claim-evidence.md).

## 113.0 zapis na `/claims`

### Zakres

- Tabela `cargo_claim` na `shipment`
- `claim_kind`: `damage` | `shortage` | `other`
- Ekran `/claims`

### Poza 113.0

S52 · kwota · ubezpieczenie · LLM · terminy CMR

## 191.0 OS&D + terminy CMR

### Zakres

- `damage_code`: `overage` | `shortage` | `damage` | `loss`
- `cmr_notice_window`: `notice_7` | `notice_21`
- `notice_due_at` / `suit_due_at` jako dni HITL

### Poza 191.0

Deadline Engine · evidence GPS/temp/photo · `liable_party_id` · kwota

## 645.0 evidence HITL

### Zakres

- `evidence_gps` / `evidence_temp` / `evidence_photo` jako niezależne bool HITL
- UI `/claims` — trzy checkboxy

### Poza 645.0

Deadline Engine · live GPS · bajty zdjęcia · `liable_party_id` · kwota
