# Karty pól — Fala Plat / Demo-1 / Admin-P

**Kanon:** PLAN § Fala Plat. Pin 2026-09-08c.

## Środowiska

prod · stage (klon prod) · sandbox API · demo.

## Admin-P

OpenFGA `platform_admin`. Usage z `platform_usage_daily` (nie SELECT cross-tenant). Umowy CI: tylko `contracts_count`. Impersonation nie odszyfrowuje CI9.

## Demo-1

Jedno kliknięcie → 10 miesięcy. Morze+droga obowiązkowo; też air/OOG. 150 ciągników `demo_sim`. GPS live **7 dni** 30–60 s; 10 mies. = agregaty km/dzień. Pogoda strefy EU. `demo_disruption`. ETA przedział. Tacho 4,5h + naruszenia. LTL solver OR (nie LLM). Maile na sandbox, nie skrzynkę gościa. Koniec: `USUN`. Pełne po T+V+D+G6.

## Skala / DR

k6 10k VU na stage zanim copy 15k. PITR; RPO≤15 min; RTO≤4 h; restore stage co tydzień. EU. Nie Infisical.
