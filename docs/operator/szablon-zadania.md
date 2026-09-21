# Szablon zadania

Na `/task-templates` zapisujesz **szablon zadania** tenanta: kod snake i warunek jako tekst. To nie jest zadanie na zleceniu i nie silnik, który ten warunek odpala.

1. Wejdź na Szablon zadania. Podaj `template_code` (snake, 2–32 znaków).
2. Wpisz `applies_when` (tekst do 512 znaków). System go **nie** interpretuje.
3. Podaj `source_ref` (`fixture://task-template/…` albo `tenant:manual`).
4. „Zapisz szablon zadania”. Zły kod wraca jako `szablon`, pusty warunek jako `warunek`, obce pochodzenie jako `obce`.
5. Zapis dokłada też zdarzenie na `/outbox` o rodzaju `task_template_saved`. Ten sam szablon = ten sam wiersz. Konsument go nie zjada.

Czego tu nie ma: ewaluacja `applies_when`, FK `shipment`/`trip`/`stop`, assignee, Temporal. Wpis zadania jest na `/tasks`. Marża zostaje na `/charges`. Szablon opłat zostaje na `/charge-templates`.

Nazwy w kodzie: `task_template` · `template_code` · `applies_when` · `source_ref` · `task_template_saved`.
