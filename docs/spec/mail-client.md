# M-33 klient poczty — `mailto:` z znanego kontaktu

**Moduł żywy:** M-33 (token UI `mail_client`, nie tabela) + ekran M-32 `/mail`  
**Plaster:** **26.0** (plan)  
**Status:** operator **otwiera** znany adres w kliencie poczty. Nie dodatek Office. Nie Graph.

Delta: [docs/deltas/open/26.0-mail-client.md](../deltas/open/26.0-mail-client.md).

## 26.0 mailto na `/mail`

### Zakres

- Na `/mail`: link `mailto:` przy `party_contact.email`
- Zero Office.js. Zero manifestu. Zero Graph
- Zero nowej tabeli

### Poza 26.0

Dodatek Outlook · Microsoft Graph · IMAP wysyłka · M-34 · LLM

### HC

- Adres zostaje w `party_contact` (SQL). Link nic nie liczy.
- LLM nie pisze treści maila.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje parties
