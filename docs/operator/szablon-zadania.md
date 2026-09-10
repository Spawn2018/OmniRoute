# Szablon zadania

Na `/task-templates` zapisujesz **szablon zadania** tenanta: kod snake i warunek jako tekst. To nie jest zadanie na zleceniu i nie silnik, który ten warunek odpala.

1. Wejdź na Szablon zadania. Podaj `template_code` (snake, 2–32 znaków).
2. Wpisz `applies_when` (tekst do 512 znaków). System go **nie** interpretuje.
3. Podaj `source_ref` (`fixture://task-template/…` albo `tenant:manual`).
4. „Zapisz szablon zadania”. Zły kod wraca jako `szablon`, pusty warunek jako `warunek`, obce pochodzenie jako `obce`.

Czego tu nie ma: instancja `task` na `shipment`/`trip`/`stop`, matching SQL, outbox, live KSeF, live VIES. Marża zostaje na `/charges`. Szablon opłat zostaje na `/charge-templates`.

Nazwy w kodzie: `task_template` · `template_code` · `applies_when` · `source_ref`.
