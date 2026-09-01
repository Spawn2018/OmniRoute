# Wklejka — agent budujący (nowy czat)

Skopiuj **cały blok** poniżej. Auth0 I1/I2 **odroczone** (brak tenanta — nie startować, nie pytać). Wave A i Wave FE U-* (ID) są na origin. Exit Wave FE **nie** claim.

---

```
Charge 1.3 + U-* ID na origin. Auth0 I1/I2 odroczone (brak tenanta). Nie implementuj Auth0/BFF/OIDC.

1. Przeczytaj docs/state/CURRENT.md
2. Przeczytaj docs/state/PROGRAM-12M.md (jedyny SoT programu; canvas NIE jest git SoT)
3. git status — drzewo ma być czyste; jeśli nie, STOP
4. Wykonaj **0.24** (pip-audit / pin SHA / /ready / request-id) albo leftover AI **2.1–2.2** (Presidio instructor stub + 8–12 syntetyk). Nie I1/I2.

WIP=1. Max 12 plików. Test-first. Schemat = MCP Postgres (brak = stop).
Nie czytaj Informacje z claude/. Nie twórz Temporal/Hatchet/outbox na zapas, Infisical, 70 pustych M-xx, kodu Auth0.

Kolejność leftover (PROGRAM, I1/I2 pominięte):
→ 0.24 pip-audit / pin SHA / /ready / request-id
→ 2.1–2.2 Presidio instructor stub + 8–12 syntetyk (nie 30 PDF klienta, nie Presidio-all)

Sesja = email+hasło+JWT. 0.12/0.15 ≠ IdP. echo ≠ DoD. Po plasterze: post-plaster + push + nowa rozmowa.

Exit Wave FE: wszystkie U-* w PROGRAM-12M.md — ID na origin, claim powierzchni **zakazany**. D0 nie zdejmuje HITL / LLM nigdy nie liczy.
```
