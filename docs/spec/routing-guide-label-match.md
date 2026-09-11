# Spec: routing guide label match (CT4 leftover)

**Moduł żywy:** CT4 leftover matching lane/mode

## 289.0 matching etykiet na ASN

- Po `assert_asn_on_routing_guide`: gdy `block_409` i katalog `routing_guide_match` ma `lane_label` / `mode_label`, porównaj `plant_label` / `carrier_label` z polami przewodnika (trim + casefold)
- `guide_code_only` = bez dodatkowego checku
- Składanie w API ASN; BC `purchase_orders` bez importu services przewodnika
- Nie matching na shipment w tym plasterze
