# Czego klienci oczekują od TMS (44 case'y + 59 newsów Qargo; wdrożenia SPEED)

**Kiedy:** decyzje o kolejności fal; teksty sprzedażowe; DoD modułów UI.

## Co realnie sprzedaje (ranking z case'ów)

1. AI order entry — mail/PDF → zlecenie bez przepisywania (−75% adminu).
2. Fakturowanie natychmiast po POD + integracje księgowe.
3. Driver app / ePOD (skan, podpis, zdjęcie z dostawy).
4. Planning board z widocznością zasobów.
5. Portale self-service (klient sam sprawdza status — mniej telefonów).

## Bolączki rynku

- Podwójne wpisywanie danych i „umierający" legacy TMS = powód migracji nr 1.
- Cash flow przewoźnika (szybka faktura, faktoring).
- Puste kilometry: 31% UK / 25,9% UE.
- Wdrożenia legacy TMS bolą: ROHLIG SUUS ~rok poślizgu, Rhenus „łzy
  i zgrzytanie zębami" (SPEED) — czas-do-wartości to broń konkurencyjna.

## Czego wciąż brakuje na rynku (luki do zajęcia)

e-CMR · WhatsApp/komunikatory · AI-planowanie (nie tylko AI-wklepywanie) ·
control tower dla załadowców (Qargo nie adresuje — nasza przewaga nr 1:
łańcuch skutków „co się stanie, jeśli nie zareagujesz").

## Zasada produktowa

„Wpisz raz, zapisz na stałe": słowniki per tenant + szablony + wartości
domyślne (M-03) + saved views (`table_view`). Każdy nowy formularz musi
wskazać, skąd bierze wartości domyślne — karta pól przed Planem.

Źródła: `docs/_source/benchmark/qargo-cases.md`, `interlan-cases-ispeed.md`.
