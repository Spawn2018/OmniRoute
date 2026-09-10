# API i dostawy operatora — brama test → produkcja

**Nie sekrety.** Klucze tenanta szyfrowane, puste = 503, nie cichy skip. Zakaz scrapingu.

Kanony: [dostepy-do-zdobycia.md](../analysis/dostepy-do-zdobycia.md) (URL, sandbox), [nocna-zmiana.md](nocna-zmiana.md) (park live ≠ skip leftoveru HITL).

## Jak czytać listy

| Lista | Znaczenie | Co wolno w `/noc` |
|---|---|---|
| **A — test publiczny** | Kontrakt HTTP albo sandbox bez umowy na start | Fixture + klient; live gdy sekret tenanta jest |
| **B — kontrakt** | Docs są, ruch wymaga umowy / klucza integratora | Kształt adaptera + 503 bez sekretu; nie udawaj produkcji |
| **C — park live** | Brak testu, docs za loginem albo TO_VERIFY | Nie HTTP. HITL/SQL na własnej tabeli i tak jedzie |

`/noc` nie zgaduje S53, portali ani konsumenta M-02, dopóki CURRENT nie wskaże tego Q.

## A — wolno pisać klienta (test / publiczny kontrakt)

- KSeF API 2.0 TEST/DEMO (OpenAPI). Mandat PL 2026 — TE na osi leftoverów.
- VIES (SOAP Komisji), whitelist VAT UE, KRS Open API, CEIDG (JWT self-serve).
- TED eTendering (publiczne ogłoszenia). BDO swagger **test** (klucz integratora osobno = B).
- IMGW JSON publiczny. IKOL / Flotis REST / Wialon Remote API (klucz tenanta).
- OpenFreeMap, GUGiK WMTS. HERE / PTV — OpenAPI; live = klucz tenanta.
- NBP tabela A — już w kodzie (`nbp_rate`).

## B — kontrakt jest, produkcja czeka na umowę

- SENT / PUESC webservice, EKAER, RO e-Transport.
- Trans.eu Partners + monitoring (klucze aplikacji). Teleroute CRUD ofert — nie visibility.
- GBOX (docs za loginem). TIMOCOM / Transporeon Visibility — credentials od AM.
- Comarch Optima/XL, Symfonia, Subiekt nexo/GT — agent/COM; jeden plaster F9 = Optima fixture.
- Poczta EN / EPO — umowa. Palletforce etykieta — brak publicznego generatora.

## C — park live (nie udawaj API)

- Open-Meteo **hosted** bez płatnego planu albo self-host AGPL — produkt jest komercyjny. Nie free SaaS.
- AIS wieży, T8 TOS live, S21 kanał armatora, GPS GBOX poll, ciphertext adaptera.
- Auth0 (S53), portale X, Graph/IMAP/SMTP send.
- Citizen API KREPTD, scrape kreptd.gitd.gov.pl, TED HTML scrape.
- GUS BIR live bez kontraktu. e-TOLL ZSL (Omni nie jest operatorem).

## XOR widoczności

Jeden feed na `trip` / `shipment`: p44 **albo** FourKites **albo** Shippeo. Nie trzy prawdy. Źródło = `source_ref`.

## Brama

1. Test albo fixture zielone.
2. Sekret tenanta, nie w repo.
3. Idempotencja.
4. HITL zanim wiersz biznesowy (extract, cutoff, myto→`charge`).
5. Brak testu → lista C, nie 200 z powietrza.
