# M-10 Kontrahenci — `party` i katalog zależny

**Moduł żywy:** M-10 (archiwum M-10; nie koliduje z żywym M-07 `rate_line` / M-08 `charge`)  
**Plaster:** **5.0** (Plan zaakceptowany; kod w `/plaster`)  
**Status:** szkielet. Nie Q3. Nie M-11–M-14. Nie M-19.

Delta: [docs/deltas/open/5.0-party.md](../deltas/open/5.0-party.md).

## 5.0 katalog kontrahenta

### Zakres

- Tabela `party` per tenant: `organization_id`, `legal_name`, `short_name`, `tax_id`, `vat_eu`, `regon`, `krs`, `country_code`, adres kolumnami (`address_line`, `city`, `postal_code` — nie `jsonb`), `roles text[]` (`customer` | `vendor` | `agent` | `carrier` | `shipper` | `consignee` | `notify`), `payment_terms_days`, `credit_limit`+`credit_currency` (Numeric, ręcznie, para albo oba NULL), `default_currency`, `language`, `gus_synced_at` / `vies_checked_at`, `is_active`, `source_ref`, timestamps
- Unikat częściowy `(organization_id, country_code, tax_id)` gdy `tax_id` nie NULL. Nośnik FK: `UNIQUE (organization_id, id)`
- `resolve(tax_id)` — dokładne, bez wielkości liter; nieznany = `UnknownParty`; nie luźna nazwa. PL: NIP 10 cyfr + suma kontrolna
- Tabele zależne, FK złożone `(organization_id, party_id)`:
  - `party_contact` — name, email, phone, position, `is_primary`; bez portalu
  - `party_bank_account` — IBAN, currency, bank_name, `whitelist_status`, `whitelist_checked_at`
  - `party_email_domain` — domena lowercase; unikat `(organization_id, domain)`
  - `party_charge_override` — token `charge_code` (FK do `charge_code(organization_id, code)`), `lane_pattern`, `amount` Numeric(14,4)+`currency`, `basis`, `valid_from`/`valid_to`, `source_ref`
  - `carrier_profile` — 1:1; `scac_code`, `is_nvocc`, `rate_source_email`, `api_adapter` (`none`|`maersk`|`hapag`|`cma`|`msc`), `dcsa_tnt_version`; zero HTTP do armatorów
- Lookup GUS/VIES/biała lista: szkic w odpowiedzi, bez INSERT; CI = fixture; timeout + idempotencja
- OpenFGA `can_manage_parties` = member
- UI `/parties`: DataTableShell + dodanie + resolve + lookup + panele zależne
- ALTER `terminal.operator_party_id` (nullable, FK złożone); `operator_name` zostaje. Picker na `/terminals` woła API `/parties`. Serwis geografii nie importuje `app.services.parties`

### Poza 5.0

Q3 (`quotation.party_id`, POL/POD) · M-11 matcher domen · M-12 sieci · M-13 scorecard · M-14 auto-scoring · M-19 live adapter · portal · outbox · Auth0 · `quotation`/`charge` czytające override · „handlowiec widzi swoich”.

### HC

- RLS FORCE + test izolacji na każdej tabeli
- `organization_id` na każdym wierszu (archiwalny NULL odrzucony)
- HC-02: `credit_limit` i `party_charge_override.amount` = Decimal + waluta; LLM nie liczy; marża zostaje w `charge.margin()` — override **nie** jest silnikiem wyceny
- HC-03: `source_ref` na `party`, override i domenie
- HC-04: lookup nie zapisuje; człowiek potwierdza
- HC-05: brak sekretów GUS w repo; każdy endpoint z `require_permission`
- HC-06: lookup idempotentny + timeout; nie outbox (M-02 parked)
- ExtractionService nie importuje `parties`
