---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Kontekst systemu (C4 poziom 1)

```
                    ┌──────────────────┐
                    │  Klient końcowy  │
                    │   (załadowca)    │
                    └────────┬─────────┘
                             │ mail z zapytaniem, portal
                             ▼
┌────────────┐      ┌────────────────────┐      ┌──────────────┐
│ Handlowiec │─────▶│                    │◀─────│   Agent      │
│  Operator  │      │     OmniRoute      │      │ zagraniczny  │
│ Właściciel │◀─────│                    │─────▶│              │
└────────────┘      │  wyceny, zlecenia  │      └──────────────┘
                    │  stawki, finanse   │
┌────────────┐      │                    │      ┌──────────────┐
│ Przewoźnik │◀────▶│                    │◀────▶│   Armator    │
│Podwykonawca│      └─────────┬──────────┘      │ (API/DCSA)   │
└────────────┘                │                 └──────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐   ┌───────────────┐
│  KSeF        │    │ GUS · KRS · RDF  │   │  Bank         │
│  MF: biała   │    │ Biała lista VIES │   │  MT940 · PSD2 │
│  lista       │    │ NBP              │   │               │
└──────────────┘    └──────────────────┘   └───────────────┘
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐   ┌───────────────┐
│ Listy        │    │  Claude API      │   │  Partner      │
│ sankcyjne    │    │  (ekstrakcja)    │   │  faktoringowy │
│ UE·ONZ·OFAC  │    │                  │   │               │
└──────────────┘    └──────────────────┘   └───────────────┘
```

## Systemy zewnętrzne

| System | Kierunek | Cel | Poświadczenia |
|---|---|---|---|
| Armatorzy | dwustronny | stawki spot, tracking, booking | tenanta |
| Agenci | mail | zapytania i cenniki | skrzynka tenanta |
| KSeF | wychodzący | faktury ustrukturyzowane | certyfikat tenanta |
| GUS, KRS, RDF, VIES | przychodzący | dane kontrahentów | klucz tenanta lub platformy |
| Biała lista VAT | przychodzący | weryfikacja rachunków | publiczne |
| NBP | przychodzący | kursy walut | publiczne |
| Bank | dwustronny | wyciągi, płatności | tenanta |
| Listy sankcyjne | przychodzący | screening | publiczne |
| Claude API | wychodzący | ekstrakcja, klasyfikacja | platformy |
| Partner faktoringowy | dwustronny | wnioski, decyzje | platformy |

## Granica zaufania

Wszystko poza prostokątem OmniRoute jest niezaufane. Dane wejściowe z maili,
plików i API zewnętrznych przechodzą walidację, a przy przetwarzaniu modelem
dodatkowo przez `llm-guard`.
