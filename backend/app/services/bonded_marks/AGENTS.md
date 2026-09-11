# BC bonded_mark (G11)

HITL katalog znacznika bonded/miejsce uznane per tenant. mark_code + bond_kind bonded|recognized|other + source_ref. Nie WMS. Nie procedura live.

## Dozwolone zależności
- `app.models.bonded_mark`
- `app.repositories.bonded_marks`
- `app.domain`

## Zakaz
- import innych BC services (dock_appointments, geography, charges, extraction)
- zapis `dock_appointment` / `location` / `charge` / `shipment`
- WMS e-com / procedura bonded live / amount / wms / float / kwota
- HTTP
- UPDATE / DELETE wiersza
