# Operator: ticket produktu

Zapisujesz zgłoszenie błędu programu: kod, tytuł, treść, rodzaj
(report / triage / owner_ok / other) oraz wskazanie źródła.
To są dane HITL — nie uruchamiają auto-naprawy ani CAPA.

Przy `owner_ok` podajesz `reviewed_ticket_id` (wcześniejszy zgłoszony ticket).
Bez accepted decyzji S11 API zwraca 409 z `decision_id` — akceptujesz na
`/decisions`, potem ponawiasz POST z `owner_decision_id`.

Katalog stancji (`/product-ticket-marks`) zostaje osobno. Tu jest wpis z
treścią. Zmiana stancji = nowy wpis (brak UPDATE). Mob i auto-fix = leftover.
