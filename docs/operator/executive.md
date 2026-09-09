# Pytanie zarządu

Na `/executive-marks` zapisujesz **znacznik rodzaju pytania zarządu** tenanta (strata, korytarz, ryzyko, gotówka, inne). To nie suma z modelu i nie zdania z agregatów SQL.

1. Wejdź na Pytanie zarządu. Wybierz rodzaj (`loss` / `lane` / `risk` / `cash` / `other`).
2. Podaj `source_ref` (`fixture://executive-mark/…` albo `tenant:manual`).
3. „Zapisz pytanie zarządu”.

Czego tu nie ma: suma LLM, EBITDA, narracja 117.0, ranking W5, suma w przeglądarce. Tablica finansowa zostaje na `/finance`. Marża zostaje na `/charges`.

Nazwy w kodzie: `executive_mark` · `question_kind` · `source_ref`.
