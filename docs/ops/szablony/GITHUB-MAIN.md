# GITHUB-MAIN — ruleset fabryki

Trigger: stop `/noc` + jawne **„włącz ochronę main”**. Nie INSTALL-UXCL. Nie kod produktu.  
Mapa: `GIGANT-LUKI-2026.md` §2.

## Audyt (2026-09-16, `gh api`)

| Fakt | Wartość |
|---|---|
| Widoczność | **public** |
| `main` protection | **brak** (HTTP 404) |
| Rulesets | `[]` |
| Semafor lokalny | `/noc` + hooki + `git-push-main.ps1` — nie zastępuje rulesetu |

## L0 — ruleset `main-factory` (Settings → Rules → Rulesets)

| Reguła | Wartość | Dlaczego |
|---|---|---|
| Target | branch `main` | jedyny trunk |
| Block force-push | **ON** | SEV-1 w polityce; dziś GitHub nie egzekwuje |
| Block deletions | **ON** | publiczne `main` |
| Require pull request | **OFF** | `/noc` pcha trunk |
| Required approvals / CODEOWNERS | **OFF** | do drugiego człowieka |
| Restrict updates (tylko Actions) | **OFF** | złamie lokalny push |
| Bypass | tylko admin (CEO) | Amazon STO |
| Required checks na direct push | nie udawaj | W38: czekaj na `gate=success`; `cancel-in-progress` już jest |

Po zapisie: `gh api repos/Spawn2018/OmniRoute/rulesets` ≠ `[]`.

## L1 — public repo

- [ ] Secret scanning / push protection (Code security)
- [ ] Actions: read contents default; brak `pull_request_target` z sekretami
- [ ] Fork PR: nie poszerzaj uprawnień jobów
- [ ] Publiczne logi Actions: zero sekretów w echo (`JWT_SECRET` tylko z `secrets.*`)

## L2 / L3

Environments = G0. Required PR + 1 review = pierwszy etat ludzki (`HIRE-HUMAN.md`).

## Zakaz

Włączać podczas `/noc` · GitFlow · required PR „jak Google” · CODEOWNERS-agent · GitHub-agent · force-push „tylko tym razem”.
