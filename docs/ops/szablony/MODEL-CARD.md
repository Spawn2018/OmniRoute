# MODEL-CARD extract (Mitchell et al. 2019 — skrót)

Trigger: zmiana modelu / Instructor wiring / nowy `prompt_version` (Park: żywy model w CI).  
Nie jest next-ID. Nie zastępuje `PROMPT-CHG.md` (ten jest na tekst promptu).

- model_id / vendor / data:
- Do czego wolno: szkic NLP pól dokumentu (HITL przed zapisem)
- Do czego nie wolno: liczyć marży/VAT/kursu; zapis L0–2; accept extractu; scoring osoby
- Wejście (typ dokumentu): taryfa / mail / PDF — bez 30 PDF klienta w git
- Wyjście: draft pól, nie `rate_line` / `charge`
- Eval: fixture/golden, które zostają zielone (`just promptfoo` dziś = echo)
- Dane treningu / licencja: `07` + datasheet gdy DocLayNet
- PII / sekrety: model nie widzi sekretów tenanta
- Werdykt: D2 | leftover AI3 | park
