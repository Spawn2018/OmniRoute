# Szablon opłat

Na `/charge-templates` zapisujesz **kolekcję kodów** z katalogu i daty ważności. To nie silnik nakładania i nie wiersz `charge`.

1. Wejdź na Szablony opłat. Podaj `template_code` (snake), token `charge_code` już istniejący w katalogu i okno dat.
2. Nieznany kod i odwrócone daty odpadają. Kilka wierszy z tym samym kodem szablonu to kolekcja.
3. „Zapisz szablon opłat” z `source_ref` (`fixture://charge-template/…` albo `tenant:manual`).

Czego tu nie ma: exclusion GiST jak strefy pocztowe, kwota, FSC, zapis na `charge`. Marża zostaje na `/charges`.

Nazwy w kodzie: `charge_template` · `template_code` · `charge_code` · `valid_from` · `valid_until` · `source_ref`.
