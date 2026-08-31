---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Model bezpieczeństwa

## Uwierzytelnianie

| Powierzchnia | Mechanizm | Dwuskładnikowe |
|---|---|---|
| Aplikacja wewnętrzna | OIDC, sesja z tokenem odświeżania | opcjonalne, wymuszalne przez tenanta |
| Portal klienta | link jednorazowy albo hasło | opcjonalne |
| Portal przewoźnika | link jednorazowy | nie |
| API publiczne | klucz z zakresem | — |
| Konsola administratora | OIDC + osobna domena | **obowiązkowe** |

## Autoryzacja

OpenFGA w modelu relacyjnym. Każdy endpoint deklaruje wymagane uprawnienie
jawnie — brak deklaracji oznacza odmowę i jest wychwytywany testem.

**Widoczność kosztów** jako osobny wymiar roli: `full`, `margin_only`,
`sell_only`, `none`. Egzekwowana w warstwie serializacji, nie w interfejsie.

## Izolacja danych

RLS na poziomie bazy z `FORCE ROW LEVEL SECURITY`. Kontekst tenanta
ustawiany przez `SET LOCAL app.current_org`. Polityka wymaga jawnie,
by wartość nie była pusta.

Zasada 12: żadne zapytanie nie sięga po dane więcej niż jednego tenanta.
Egzekwowana testem architektonicznym.

## Szyfrowanie

| Zakres | Mechanizm |
|---|---|
| W transporcie | TLS 1.3, HSTS, bez wersji starszych |
| W spoczynku | szyfrowanie wolumenu, AES-256 |
| Poświadczenia zewnętrzne | szyfrowane kluczem per tenant |
| Sekrety aplikacji | Infisical, rotacja kwartalna |
| Kopie zapasowe | szyfrowane, klucz osobno od danych |

## Powierzchnie o podwyższonym ryzyku

| Moduł | Zagrożenie | Zabezpieczenie |
|---|---|---|
| M-01 wielodostępność | dostęp międzytenantowy | RLS + test izolacji per tabela |
| M-19 poświadczenia armatorów | wyciek kluczy klienta | szyfrowanie per tenant, brak logowania |
| M-20 ekstrakcja | prompt injection z pliku | llm-guard, schemat wymuszony |
| M-100 widoczność kosztów | ujawnienie marży handlowcowi | filtracja w DTO |
| M-207 finansowanie | duplikat operacji | klucz idempotencji |
| M-209 płatności | przelew na podstawiony rachunek | biała lista, potwierdzenie kanałem |
| M-211 konsola | eskalacja uprawnień | 2FA, IP, audyt, limit sesji |
| M-94 API publiczne | wyczerpanie zasobów | limity per klucz |

## Zasada najmniejszych uprawnień

Konto bazy dla MCP: wyłącznie odczyt, wyłącznie baza deweloperska.
Konto aplikacji: bez uprawnień DDL na produkcji.
Konsola administratora: brak bezpośredniego dostępu do bazy.
