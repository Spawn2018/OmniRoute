# Szablon opłat

Na `/charge-templates` zapisujesz **kolekcję kodów** z katalogu i daty ważności. Nakładanie okien tego samego kodu w tym samym szablonie blokuje Postgres, nie arkusz.

1. Wejdź na Szablony opłat. Podaj `template_code` (snake), token `charge_code` już istniejący w katalogu i okno dat.
2. Nieznany kod i odwrócone daty odpadają. Kilka wierszy z tym samym kodem szablonu to kolekcja.
3. Kolejny okres tego samego kodu wolno zapisać, gdy daty się nie nakładają. Nakładanie wraca z komunikatem o nakładaniu.
4. „Zapisz szablon opłat” z `source_ref` (`fixture://charge-template/…` albo `tenant:manual`).

Czego tu nie ma: parser nakładania w przeglądarce, kwota, FSC, zapis na `charge`. Marża zostaje na `/charges`. Strefy pocztowe zostają na `/locations`.

Nazwy w kodzie: `charge_template` · `template_code` · `charge_code` · `valid_from` · `valid_until` · `source_ref`.
