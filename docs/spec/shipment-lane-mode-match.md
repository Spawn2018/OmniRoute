# Spec: shipment routing guide label match (CT4 leftover)

**Moduł żywy:** CT4 leftover matching lane/mode na zleceniu

## 290.0 matching etykiet na shipment

- Opcjonalne `plant_label` / `carrier_label` na `shipment` (HITL, jak ASN)
- Po `assert_asn_on_routing_guide`: `assert_asn_labels_on_routing_guide` przy `block_409` + match kinds
- Składanie w API; BC shipments bez importu services przewodnika
