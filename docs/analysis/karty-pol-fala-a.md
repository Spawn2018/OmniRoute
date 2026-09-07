# Karty pól — Fala A (automatyzacja)

**Kanon:** PLAN. Parasuraman: detect/draft wolno; decyzja pieniężna = człowiek. Pin 2026-09-08c.

| Poziom | Wolno | Nigdy |
|---|---|---|
| detect | notice / semafor | send, INSERT charge, booking HTTP |
| draft | mail_draft / suggested / SENT XML | accept, mailto, Graph |
| act | cyfra kontrolna, geofence, grace GPS, numer M-03 | limity, marża, FV, przelew |

A1–A8 detect (cutoff, D&D szkic, geofence, odchylenie, credit hold 409, restrykcje drop, backhaul SQL, sankcje odczyt).  
A9–A16 draft (SOP→task, standing order, FSC nowy rate_line, SENT szkic, Qi-reguła szkic, auto-assign jako task, accrual, N mail).  
A17–A18 act (ISO/NIP/IBAN/UN; GPS grace).  
A19–A22 rozbudowa (prom, standing_rate, ePOD match, won/lost).

Zakaz: auto-send, auto-award, auto-limit, charge z LLM, Selenium, LLM-VRP, GAN, scoring osoby.
