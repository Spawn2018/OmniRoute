# Spec: rag_sop_mark (EXP4.18)

HITL katalog znacznika zakresu RAG (tylko SOP) per tenant.

## Pola

- `mark_code` — snake 2–32
- `scope_kind` — `sop` | `adr` | `mail` | `other`
- `source_ref` — `tenant:manual` albo `fixture://rag-sop-mark/…`

## Poza zakresem

pgvector · RAG na wycenie/VAT/schemacie · kwota
