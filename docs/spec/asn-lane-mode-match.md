# Spec: ASN lane/mode matching (CT4 leftover)

**Moduł żywy:** CT4 leftover matching

## 289.0 matching etykiet na ASN

- Przy `block_409` + `routing_guide_match.match_kind`:
  - `lane_label` → `plant_label` vs guide.lane_label
  - `mode_label` → `carrier_label` vs guide.mode_label
- Domain `assert_asn_labels_on_routing_guide`
- Nie matching na shipment
