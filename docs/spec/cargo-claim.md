# M-55 reklamacja ładunku — tabela `cargo_claim`

**Moduł żywy:** M-55 (token `cargo_claim`)  
**Plaster:** **191.0** (zamknięty; 113.0 nagłówek)  
**Status:** operator zapisuje reklamację na zleceniu z OS&D i terminami CMR. Nie kwota. Nie scoring. Nie silnik 7/21/365.

Delta 113.0: [docs/deltas/archived/113.0-cargo-claim.md](../deltas/archived/113.0-cargo-claim.md).  
Delta 191.0: [docs/deltas/archived/191.0-cargo-claim-cmr.md](../deltas/archived/191.0-cargo-claim-cmr.md).

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
