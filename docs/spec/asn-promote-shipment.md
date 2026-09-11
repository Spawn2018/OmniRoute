# Spec: ASN promote → shipment (CT1 leftover)

**Moduł żywy:** CT1 leftover auto shipment (HITL)

## 291.0 promote

- `POST /asns/{id}/promote` z `quotation_id`
- Kopiuje `guide_code` / `plant_label` / `carrier_label` z ASN na nowe `shipment`
- `shipment.asn_id` opcjonalne FK; unique per org gdy ustawione
- Nie auto przy zapisie ASN
