# Spec: freight_audit_mark (CT10)

**Moduł żywy:** CT10 (`freight_audit_mark` HITL katalog)

## 283.0 katalog rodzaju audytu frachtu

- Tabela `freight_audit_mark`: `mark_code`, `audit_kind` (`expected_vs_invoice`|`expected_vs_charge`), `source_ref`
- POST INSERT / GET lista
- Nie SQL vs `charge`; nie druga marża
