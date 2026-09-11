# Spec · shipment lane/mode match (290.0)

Gdy tenant ma `routing_guide_enforcement.enforcement_kind = block_409` oraz wiersze `routing_guide_match` z `lane_label` / `mode_label`, POST `/shipments` wymaga zgodnych `plant_label` / `carrier_label` względem wybranego `routing_guide` (trim, casefold). Reużywa `assert_asn_labels_on_routing_guide`. Nie live EDI.
