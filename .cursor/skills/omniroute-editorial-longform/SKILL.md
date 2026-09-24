---
name: omniroute-editorial-longform
description: >-
  Składa długi tom PL (spis, numeracja rozdziałów, aneksy, licznik stron
  maszynowych). Używaj przy dokumencie wielostronicowym, tomie audytu,
  aneksach VISION/MODULES/speców, gdy user podaje znaków/stronę.
---

# Tom długi, język formalny

## Język

Polski formalny, pełne zdania. Bez emoji, banerów ASCII, ozdobnych separatorów, „lorem ipsum”, powtórki jednego zdania w pętli.

Objętość dociąga się **treścią źródłową** (cytat, zrzut, aneks), nie wodą.

## Metoda stron

Domyślnie, jeśli user nie podał innej: **1800 znaków ze spacjami = 1 strona maszynowa**.

Na końcu tomu obowiązkowo:

- liczba znaków (len tekstu),
- strony = znaki / 1800 (podać też zaokrąglenie),
- lista włączonych plików źródłowych.

## Struktura tomu

1. Karta metody i ograniczeń (co nie przeczytano).
2. Spis treści z numeracją rozdziałów arabską.
3. Rozdziały merytoryczne — każdy akapit: cytat/streszczenie ze ścieżką **albo** „w przeczytanych plikach tego nie ma”.
4. Aneksy oznaczone literami (A, B, C…). Aneks to **pełny plik** albo spis nagłówków + ścieżka, gdy plik przekracza budżet.
5. Licznik znaków i stron.

Nie zagnieżdżaj trzeciego poziomu „wizji”. Nagłówek aneksu podaje ścieżkę źródła.

## Numeracja

```
# Tytuł tomu
## Spis treści
## 1. …
## 2. …
## Aneks A — …
```

Rozdział nie zaczyna się od negacji. Najpierw fakt ze źródła, potem kontrast (wizja vs kod), jeśli źródła się rozjeżdżają.

## Budżet ±

Cel stron i tolerancja podaje user. Jeśli za krótko: dołącz kolejne **istniejące** zrzuty (najpierw spis + najdłuższe specy, potem pełne benchmarki). Jeśli za długo: **nie obcinaj faktów** — dziel na dwa pliki z sufiksem -czesc-01 oraz -czesc-02; część 1 trzyma spis całego tomu.

## Zakaz

- Wypełnianie do limitu zmyślonym tekstem.
- Edycja `docs/VISION.md` przy składaniu tomu, chyba że user każe.
- Commit, chyba że user każe.
