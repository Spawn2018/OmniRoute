# M-32 integracja pocztowa — tablica znanych adresów

**Moduł żywy:** M-32 (token UI `mail_integration`, nie tabela) + katalog M-10 `party`  
**Plaster:** **25.0** (zamknięty)  
**Status:** operator **widzi** domeny i maile kontaktów oraz resolve adresu. Nie IMAP. Nie nowa tabela.

Delta: [docs/deltas/archived/25.0-mail-integration.md](../deltas/archived/25.0-mail-integration.md).

## 25.0 tablica odczytu na `/mail`

### Zakres

- Ekran `/mail`: wybór `party` + lista `party_email_domain` i `party_contact.email` + `resolve_email`
- Zero IMAP. Zero SMTP. Zero sekretu skrzynki
- Zero nowej tabeli. Zero N+1 po całym katalogu

### Poza 25.0

Live IMAP · magazyn sekretów tenanta · Outlook (M-33) · powiadomienia (M-34) · auto-INSERT kontaktu · LLM

### HC

- Adresy zostają w `party_contact` / `party_email_domain` (SQL). Ekran nic nie liczy.
- LLM nie czyta skrzynki i nie liczy.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje parties
