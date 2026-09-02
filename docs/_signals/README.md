# Lokalny log czujników

`*.jsonl` jest w `.gitignore`. Nie commituj logu — pre-commit uzna go za drugiego pisarza.

C2 i bench idą przez `just meta-gate` (`check_agent_refs` + `craft_close --check`), nie przez osobny magazyn w git.
