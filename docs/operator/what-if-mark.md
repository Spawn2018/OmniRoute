# What-if (EXP2.10)

Operator zapisuje etykietę scenariusza what-if dla tenanta: paliwo, port, bankructwo
albo inny. To katalog HITL, nie symulator.

Każdy wiersz ma `mark_code`, `scenario_kind` i `source_ref` (ręczne
`tenant:manual` albo fixture). System nie liczy skutku, nie zmienia planu
operacyjnego i nie tworzy charge.

Silnik what-if na `plan_snapshot` (V8) zostaje leftoverem — poza tym plasterem.
