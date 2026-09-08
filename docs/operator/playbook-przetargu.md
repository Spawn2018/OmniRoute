# Playbook przetargu

Na `/tender-playbooks` zapisujesz **twierdzenie** przy istniejącym nagłówku przetargu. To nie extract RFP i nie auto-award.

1. Wejdź na Playbook przetargu. Wklej `tender_id` nagłówka tenanta.
2. Podaj kod tezy (snake) i treść twierdzenia (1–512 znaków).
3. „Zapisz tezę” z `source_ref` (`fixture://tender-playbook/…` albo `tenant:manual`).

Czego tu nie ma: extract RFP, win/loss, four-eyes, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_playbook` · `tender_id` · `claim_code` · `claim_text` · `source_ref`.
