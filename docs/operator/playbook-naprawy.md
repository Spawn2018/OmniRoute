# Playbook naprawy (CI8)

Operator zapisuje katalogowy playbook naprawy: kod, `stance_kind`
(`contain` / `reroute` / `claim` / `other`) i `source_ref`. To dane HITL,
nie auto-send S11 i nie treść maila.

Nie wysyła wiadomości. Nie zapisuje `mail_draft`. Marża nadal tylko na `charge`.

Ścieżka UI: `/repair-playbooks`.
