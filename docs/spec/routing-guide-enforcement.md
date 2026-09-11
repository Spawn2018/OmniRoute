# Spec: routing_guide_enforcement (CT4 leftover)

**Moduł żywy:** CT4 leftover (`routing_guide_enforcement` HITL katalog)

## 285.0 katalog trybu egzekucji przewodnika

- Tabela `routing_guide_enforcement`: `mark_code`, `enforcement_kind` (`record_only`|`block_409`), `source_ref`
- POST INSERT / GET lista
- Nie HTTP 409 na shipment; nie matching trasy w Pythonie
