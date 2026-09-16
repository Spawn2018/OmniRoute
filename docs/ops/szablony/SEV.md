# SEV — klasy incydentu (Microsoft IcM / Google — skrót)

Nie scoring osoby. Nie 12 dyżurów. Wypełnij **przy zdarzeniu**.

| Klasa | Co | Kto | Mechanizm |
|---|---|---|---|
| **SEV-1** | Dwaj pisarze na `main`; `--no-verify`/force-push; podejrzenie cross-tenant; sekret w logu/prompcie | CEO (D2) + stop linii | Andon + PM-FAC (A2) |
| **SEV-2** | Nocka martwa; 3× czerwone CI na tym Q; CURRENT ≠ git | Nocka stop; Ask | Andon → AAR albo PM-FAC |
| **SEV-3** | Pierwszy czerwony gate w Q; echo złapane przed claimem DONE | Plasterownik, ten sam Q | Andon 1–2; nie PM-FAC |
| **SEV-T** (po G0) | Incydent u tenanta (5xx, wyciek, IdP pad) | CEO | PRR leftover + park live; nie ten szablon zanim host żyje |

- Klasa:
- Fakt (bez winy etatu):
- Start / stop:
- Następny artefakt: Andon / PM-FAC / AAR / wiersz inbox

Zakaz: nowy skill „żeby nie było SEV”. Tenant SEV-T bez G0 = nie wymyślaj.
