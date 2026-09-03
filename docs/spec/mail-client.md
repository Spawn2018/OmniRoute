# M-33 klient poczty — `mailto:` z znanego kontaktu

**Moduł żywy:** M-33 (token UI `mail_client`) + `/mail` (26.0) + `/ai` (81.0)  
**Plaster:** **26.0** (zamknięty) · **81.0** świadomy dispatch  
**Status:** operator **otwiera** znany adres albo zaakceptowany szkic w kliencie poczty. Nie dodatek Office. Nie Graph HTTP.

Delta: [26.0](../deltas/archived/26.0-mail-client.md) · [81.0](../deltas/archived/81.0-mail-send.md).

## 26.0 mailto na `/mail`

### Zakres

- Na `/mail`: link `mailto:` przy `party_contact.email`
- Zero Office.js. Zero manifestu. Zero Graph
- Zero nowej tabeli

### Poza 26.0

Dodatek Outlook · Microsoft Graph · IMAP wysyłka · M-34 · LLM · send szkicu (81.0)

## 81.0 świadomy mailto po S11+S10

### Zakres

- Ta sama tabela `mail_draft`: status `sent`, `to_address`
- `POST /mail-drafts/{id}/dispatch-mailto` po accepted decyzji
- SOP `blocks_auto` nie blokuje mailto
- `/ai`: przycisk „Wyślij w kliencie”, `data-mail-client="dispatch-mailto"`

### Poza 81.0

Graph HTTP · SMTP · auto-send · Office.js · F9.1

### HC

- Adres zostaje w `party_contact` (SQL). Link nic nie liczy.
- LLM nie pisze treści maila.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje parties
