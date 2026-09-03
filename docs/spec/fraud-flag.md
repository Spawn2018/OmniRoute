# M-54 oszustwo — tabela `fraud_flag`

**Moduł żywy:** M-54 (token `fraud_flag`)  
**Plaster:** **114.0** (zamknięty)  
**Status:** operator zapisuje flagę oszustwa na kontrahencie. Nie scoring. Nie kwota.

Delta 114.0: [docs/deltas/archived/114.0-fraud-flag.md](../deltas/archived/114.0-fraud-flag.md).

## 114.0 zapis na `/fraud`

### Zakres

- Tabela `fraud_flag` na `party`
- `flag_kind`: `billing` | `document` | `other`
- Ekran `/fraud`

### Poza 114.0

S53 · scoring osoby · live lista · LLM
