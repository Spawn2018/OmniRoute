# Threat model — tenant + HITL

Zakres Q-E4: izolacja organizacji i ścieżka extract → akceptacja → stawka. Nie 70 BC. Nie scoring osoby.

Aktorzy: operator tenanta (member), recenzent (`can_review_extractions`), proces API, model językowy (niezaufany).

## STRIDE

| Threat | Tenant | HITL | Mitygacja w kodzie |
|---|---|---|---|
| Spoofing | token bez `organization_id` / hello UUID | accept bez recenzenta | JWT iss/aud/jti; `hello_token` off; OpenFGA `can_review_extractions` ≠ member |
| Tampering | `UPDATE` kwoty `rate_line` | extract zapisuje stawkę | `rate_line` niemutowalna; accept w warstwie API; ExtractionService nie importuje rates |
| Repudiation | stawka bez pochodzenia | akceptacja bez śladu | `source_ref` obowiązkowy; szkic + accept |
| Information disclosure | SELECT cudzego tenanta | szkic innej organizacji | RLS FORCE + WITH CHECK; test izolacji; draft B / token A → 404 |
| Denial of service | ogromny `document_base64` | kolejka extractu | max_length przed decode (0.15 T0) |
| Elevation of privilege | endpoint bez OpenFGA | member = admin extractu | undeclared `/api/v1` = deny; reviewer ≠ member |

## Świadomie poza kartą

Portale, Auth0 I1/I2, outbox (parked). Auto-scoring `natural_person`. CodeQL na prywatnym Free = GitHub Code Security (GHAS) — workflow jest, **nie** w `just gate`.

## Edge — Cloudflare (dopisek 2026-09-13, poza Q-E4)

Właściciel wymaga warstwy bezpieczeństwa **zanim** SPA jest publiczna. Kanon: [VISION.md](../VISION.md) § B.8. To nie jest plaster i nie zdejmuje leftover S53.

Dziś w kodzie nie ma CORS, HSTS ani rate limitu (`main.py` = `RequestIdMiddleware`). DoS w tabeli STRIDE dotyczy `document_base64`, nie Internetu. Cloudflare (DNS + proxy, TLS Full/strict, HSTS, Free Managed Ruleset, 1 reguła rate limit na `/api`, Access deny-by-default) zamyka host operatora **przed** publicznymi tenantami. Managed + OWASP = plan Pro dostawcy, nie Free. Bot Fight Mode chroni całą domenę i może challenge'ować `/api` — nie włączać na API bez sprawdzenia.

Nie kłaść na krawędź: Postgres, klucze LLM, sekrety tenanta, playground OpenFGA. Access ≠ Auth0. RLS i HITL zostają w aplikacji.

LLM nie liczy. `charge` = marża. Nic z extractu do bazy bez człowieka.
