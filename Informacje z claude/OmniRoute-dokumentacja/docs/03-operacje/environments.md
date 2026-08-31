---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Środowiska

| Środowisko | Cel | Infrastruktura | Dane |
|---|---|---|---|
| **local** | codzienna praca | Docker Compose na laptopie | syntetyczne, fabryki |
| **branch** | weryfikacja PR | Neon, gałąź bazy per PR | kopia z anonimizacją |
| **staging** | testy przed wdrożeniem | Hetzner, mniejszy zasób | anonimizowane |
| **production** | klienci | Hetzner, Niemcy | rzeczywiste |
| **trial** | środowiska próbne klientów | Hetzner, izolowane | dane klienta |

## Zasady

**Dane produkcyjne nigdy nie trafiają poza produkcję bez anonimizacji.**
Dotyczy także laptopa. To wymóg z umowy powierzenia, nie preferencja.

**Konfiguracja przez zmienne środowiskowe**, sekrety przez Infisical.
Żadnych wartości produkcyjnych w repozytorium.

**Staging odzwierciedla produkcję** w wersjach zależności i konfiguracji.
Różni się wyłącznie skalą zasobów i danymi.

## Lokalizacja

Produkcja: Hetzner, centrum danych w Niemczech. Dane pozostają w Unii
Europejskiej. Deklarowane w umowie powierzenia i w centrum zaufania.

## Dostęp

| Środowisko | Kto |
|---|---|
| local | Sebastian Bożek |
| branch, staging | Sebastian Bożek |
| production | Sebastian Bożek, dostęp przez klucz SSH z 2FA |
| production — baza | wyłącznie przez aplikację, brak dostępu bezpośredniego |

Przy dołączeniu kolejnej osoby: przegląd uprawnień i osobne konta.
