# M-32 integracja pocztowa — tablica znanych adresów + inbound_message

**Moduł żywy:** M-32  
**Plaster:** **65.0** (zamknięty) · 64.0 tabela · 25.0 tablica adresów  
**Status:** operator zapisuje fixture, dopina nadawcę przez `resolve_email`. Nie IMAP. Nie Graph. Nie send. Extract z treści = S3.

Delta: [65.0](../deltas/archived/65.0-inbound-resolve-email.md) · [64.0](../deltas/archived/64.0-inbound-message.md) · [25.0](../deltas/archived/25.0-mail-integration.md).

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

extract z treści (S3) · IMAP · Graph · send · załączniki blob · outbox

## 65.0 resolve_email na wiadomości

### Zakres

- `inbound_message.party_id` nullable, FK tenanta (`organization_id` + `party_id`)
- `POST /inbound-messages/{id}/resolve-email` — istniejący matcher domeny
- `/mail`: przycisk „Dopasuj nadawcę”
- BC inbound nie importuje parties; API składa

### Poza 65.0

extract (S3) · IMAP · Graph · auto przy INSERT · INSERT kontaktu

### HC

- Adresy kontaktów zostają w `party_contact` / `party_email_domain` (SQL).
- Wiadomość nie jest `party`. Lookup nie zapisuje karty.
- LLM nie czyta skrzynki i nie liczy.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje inbound_messages
