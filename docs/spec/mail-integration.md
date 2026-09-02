# M-32 integracja pocztowa — tablica znanych adresów + inbound_message

**Moduł żywy:** M-32  
**Plaster:** **64.0** (zamknięty) · 25.0 tablica adresów zostaje  
**Status:** operator **widzi** domeny i maile kontaktów, resolve adresu, oraz **zapisuje** wiadomość przychodzącą z fixture. Nie IMAP. Nie Graph. Nie send.

Delta: [docs/deltas/archived/64.0-inbound-message.md](../deltas/archived/64.0-inbound-message.md) · [25.0](../deltas/archived/25.0-mail-integration.md).

## 25.0 tablica odczytu na `/mail`

### Zakres

- Ekran `/mail`: wybór `party` + lista `party_email_domain` i `party_contact.email` + `resolve_email`
- Zero IMAP. Zero SMTP. Zero sekretu skrzynki
- Zero N+1 po całym katalogu

### Poza 25.0

Live IMAP · magazyn sekretów tenanta · Outlook (M-33) · powiadomienia (M-34) · auto-INSERT kontaktu · LLM

## 64.0 inbound_message

### Zakres

- Tabela `inbound_message` per tenant: `source_ref`, `from_address`, `subject`, `body_text`, `status = draft`
- RLS FORCE. OpenFGA `can_manage_inbound_messages` = member
- `GET/POST /inbound-messages`. Zapis tylko z `fixture://` albo `synth://`
- Ten sam `/mail`: lista DataTableShell + formularz fixture

### Poza 64.0

`resolve_email` na wierszu (S2) · extract z treści (S3) · IMAP · Graph · send · `party_id` · załączniki blob · outbox

### HC

- Adresy kontaktów zostają w `party_contact` / `party_email_domain` (SQL).
- Wiadomość nie jest `party`. Lookup nie zapisuje karty.
- LLM nie czyta skrzynki i nie liczy.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje inbound_messages
