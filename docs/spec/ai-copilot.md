# M-57 AI — tablica extract pending + szkic maila

**Moduł żywy:** M-57 (token UI `ai_copilot` + tabela `mail_draft`) + M-20 `extraction_draft`  
**Plaster:** **47.0** tablica · **76.0** `mail_draft` · **81.0** świadomy mailto · **116.0** szkice na wieży  
**Status:** operator widzi pending extract, zapisuje szkic, po Akceptuj otwiera klient poczty; wieża czyta szkice. Nie czat. Nie Graph HTTP.

Delta: [47.0](../deltas/archived/47.0-ai-copilot.md) · [76.0](../deltas/archived/76.0-mail-draft.md) · [116.0](../deltas/archived/116.0-copilot-watchtower.md).

## 47.0 tablica odczytu na `/ai`

### Zakres

- Ekran `/ai`: `aiProposals` zostawia `status` pending
- Pokazuje `source_ref`; nie `input_text`
- Link do `/extractions`
- Zero nowej tabeli w 47.0

### Poza 47.0

Tabela czatu · accept z tej trasy · scoring osoby

## 76.0 tabela `mail_draft`

### Zakres

- Tabela per serwis: `subject_kind` tylko `extraction_draft`, `subject_id` UUID bez FK, `body`, `status = draft`, `source_ref`
- RLS FORCE. OpenFGA `can_manage_mail_drafts` = member
- `GET/POST /mail-drafts`. Ten sam `/ai`: lista + utwórz. „Zgłoś do decyzji” → pending `operator_decision` z `subject_kind=mail_draft`
- CHECK decyzji: `inbound_message` albo `mail_draft`

### Poza 76.0

Czat · Graph HTTP · outbox · `changed` · lock S14 · accept extractu 1.3 · F9.1

## 116.0 szkice na `/watchtower`

### Zakres

- Wieża listuje `mail_draft` (GET)
- Zapis zostaje na `/ai`
- Zero nowej tabeli

### Poza 116.0

Czat · MCP · Graph HTTP

## HC

- Marża zostaje w `charge`.
- LLM nie liczy i nie składa treści.
- HITL extract zostaje na `/extractions`.
- ExtractionService nie importuje rates
- Serwis `mail_drafts` nie importuje extraction / inbound / quotations / operator_decisions
