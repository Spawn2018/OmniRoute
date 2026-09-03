# M-55 reklamacja ładunku — tabela `cargo_claim`

**Moduł żywy:** M-55 (token `cargo_claim`)  
**Plaster:** **113.0** (S51 plan)  
**Status:** operator zapisuje reklamację na zleceniu. Nie kwota. Nie scoring.

Delta: [docs/deltas/open/113.0-cargo-claim.md](../deltas/open/113.0-cargo-claim.md).

## 113.0 zapis na `/claims`

### Zakres

- Tabela `cargo_claim` na `shipment`
- `claim_kind`: `damage` | `shortage` | `other`
- Ekran `/claims`

### Poza 113.0

S52 · kwota · ubezpieczenie · LLM
