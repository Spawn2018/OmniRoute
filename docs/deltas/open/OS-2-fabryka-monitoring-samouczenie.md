# OS-2 — monitoring 9/10 i samouczenie 9/10 bez operatora

**Status:** open  
**Data:** 2026-09-02  
**Oś:** fabryka. **Poza osią Q/S.** Nie startuje zamiast S4.

## Co jest 9/10

| Warstwa | Mechanizm | Auto na komendach |
|---|---|---|
| Monitoring | C2 w meta-gate; `run_gate.py` zbiera kod+meta; komentarz CI na push; `quality_floor` | `/noc` preflight, `/zamknij` meta-gate, pre-push |
| Samouczenie | `factory_cycle --start` retrieve; `--close` bench + karta z 3× czerwonego `gh run`; podłoga tylko w górę | `/plan-modul` `/plaster` `/refaktor` `/noc` `/zamknij` |
| Konstytucja | test HC + floor `grounding_hc=8` | spadek = czerwony gate |

Jakość **tylko w górę.** GROUNDING nie edytuje się sam. Zero Auto-AGENTS.

## Świadomie nie 10/10

- promptfoo nadal `synth://` (liczba fixture’ów nie spada)
- D1 piątek off
- ~20 benchy urośnie z zamykanych plastrów, nie z generatora
