# Zadanie

Na `/tasks` zapisujesz **wpis zadania** tenanta: kod snake, kod szablonu jako tekst i status. To nie jest matching warunku szablonu i nie FK do zlecenia.

1. Wejdź na Zadanie. Podaj `task_code` (snake, 2–32 znaków).
2. Podaj `template_code` (snake) — to tekst, nie wybór z listy UUID.
3. Ustaw `status_kind`: `open`, `done`, `skipped` albo `other`.
4. Podaj `source_ref` (`fixture://task/…` albo `tenant:manual`).
5. „Zapisz zadanie”. Zły kod wraca jako `zadanie`, zły status jako `status`, obce pochodzenie jako `obce`.

Czego tu nie ma: ewaluacja `applies_when`, FK `shipment`/`trip`/`stop`, assignee, outbox, Temporal, M-71. Szablon zostaje na `/task-templates`. Marża zostaje na `/charges`.

Nazwy w kodzie: `task` · `task_code` · `template_code` · `status_kind` · `source_ref`.
