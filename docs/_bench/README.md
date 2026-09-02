# docs/_bench — korpus rzemiosła fabryki

Po każdym zamkniętym plasterze agent zapisuje jeden przypadek
(`python scripts/quality/craft_close.py --write`). Operator tego nie redaguje.

Orakulum w `just craft-check` (wchodzi w `just meta-gate`):
jest plik `cases/<Ostatni plaster>-*.md`; nowy `op.create_table` w przeglądzie
ma `FORCE ROW LEVEL SECURITY` i plik testu izolacji w tym samym commicie.
Styl produktu: `just craft-style` (OS-4) — slop z no-slop.mdc, nie smak.

Korpus mierzy **powtarzalność rzemiosła**, nie notę 4,4–5 ani decyzję biznesową.
Ewolucja AGENTS/GROUNDING z tego korpusu jest **zakazana**. GROUNDING zmienia
człowiek przez ADR. Higiena cytatów = C2 w `check_agent_refs.py`.
