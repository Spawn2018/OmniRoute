# SUPPLY-CHAIN — łańcuch dostaw fabryki

Trigger: P-Y po idle (L1) albo G0 (L3). Nie w `/noc`. Nie third job CI.  
Mapa: `GIGANT-LUKI-2026.md` §1. Kotwica: GitHub supply-chain docs; SLSA; `just audit` już w `gate`.

Repo IX 2026: CodeQL (`upload: never`) + piny SHA + pip-audit. Brak `dependabot.yml`. Brak SBOM.

## L0 — inwentarz (odhacz, nie buduj)

- [x] Actions pinowane do SHA (`gate.yml`, `codeql.yml`)
- [x] `just audit` w jobie `gate`
- [x] CodeQL Python + JS/TS (schedule + push/PR)
- [ ] Dependabot alerts w Settings
- [ ] Auto-PR Dependabot = **OFF** przy busy `/noc`
- [ ] Jeden SBOM (CycloneDX **lub** SPDX) z lockfile — nie required check
- [ ] Attestation / SLSA — tylko gdy jest obraz/host (G0)

## L1 — Settings (człowiek, po stop nocy + jawne)

1. Settings → Code security → Dependabot alerts: ON.
2. Dependabot security updates: OFF (włącz tylko na sesję idle, jedna paczka, WIP=1).
3. Dependabot version updates: OFF (nie `.github/dependabot.yml` w nocy).
4. CodeQL upload SARIF: TO_VERIFY na publicznym repo; nie rób z tego required check.

## L2 — SBOM (Ask, idle)

Jedna komenda lokalna z lockfile (`pnpm-lock` + graf pip). Plik do `sesje/YYYY-Www/` albo Release **po** G0. Nie commituj SBOM do ścieżki plastra HITL.

## L3 — podpis (G0)

GitHub artifact attestations / Cosign na **obraz hosta**. Claim SLSA tylko gdy attestation istnieje. `git push` ≠ build L3.

## Zakaz

Supply-agent · SBOM w każdym Q · auto-merge Dependabot · Scorecard-gate · in-toto/TUF/GUAC dziś · 11. skill.
