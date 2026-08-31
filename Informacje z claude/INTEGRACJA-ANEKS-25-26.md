# Integracja aneksów 25 i 26 do projektu

Formalne wprowadzenie dziesięciu modułów do rejestru, planu, schematu bazy
i specyfikacji. Materiał gotowy do wrzucenia do repozytorium.

---

# CZĘŚĆ I — WPISY DO REJESTRU

Do `docs/MODULES.md`, w formacie pozostałych wpisów.

## M-199 · Portal przewoźnika i podwykonawcy
**Domena:** M (sprzedaż i portale) · **Spec:** `carrier-portal.md` · **Faza:** 8

| Obiekty | Funkcje kluczowe |
|---|---|
| `carrier_portal_user` · `carrier_portal_invitation` · rozszerzenia `carrier_order` | przyjęcie lub odrzucenie zlecenia · podanie kierowcy i pojazdu · aktualizacja statusu · **wgranie CMR i zdjęć z telefonu** · **samodzielne wgrywanie dokumentów zgodnościowych** · podgląd rozliczeń · faktura z danych zlecenia · podgląd oceny |

**Zależy od:** M-200, M-35, M-79 · **Repozytoria:** `vercel/next.js` (PWA), `refinedev/refine`

## M-200 · Zgodność podwykonawców
**Domena:** C (kontrahenci) · **Spec:** `carrier-compliance.md` · **Faza:** 8

| Obiekty | Funkcje kluczowe |
|---|---|
| `carrier_compliance` · `carrier_vehicle` · `carrier_rating` | **blokada przypisania zlecenia przy wygasłym OCP** · weryfikacja okresowa z automatycznym zawieszeniem · ocena terminowości i szkód · zwolnienie blokady wyłącznie przez M-179 |

**Zależy od:** M-10, M-179 · **Ryzyko przy braku:** roszczenie ze szkody trafia do spedytora

## M-201 · Hub integracyjny
**Domena:** N (platforma) · **Spec:** `integration-hub.md` · **Faza:** 7

| Obiekty | Funkcje kluczowe |
|---|---|
| `integration_connection` · `integration_mapping` · `integration_run` · `data_share` | osiem kanałów: REST, webhooki, **SFTP z harmonogramem**, skrzynka mailowa, eksport planowany, import z mapowaniem, EDI, iPaaS · **kreator mapowania bez kodu** · katalog gotowych łączników · udostępnianie danych klientowi |

**Zależy od:** M-94, M-02 · **Repozytoria:** `hey-api/openapi-ts`, `dlt-hub/dlt`, `n8n-io/n8n`

## M-202 · Framework pomiarowy
**Domena:** L (analityka) · **Spec:** `kpi.md` · **Faza:** 6

| Obiekty | Funkcje kluczowe |
|---|---|
| `kpi_definition` · `kpi_target` · `kpi_measurement` · `kpi_dashboard` | **definicja wskaźnika raz w warstwie semantycznej** · dziewięć kategorii, ~80 wskaźników · cele i progi per wymiar · dashboardy per rola · przeliczanie w tle, nie na żądanie |

**Zależy od:** M-59 (Cube), M-46, M-13 · **Krytyczne:** bez wspólnej warstwy semantycznej trzy narzędzia podadzą trzy różne marże

## M-205 · Wymagalność dokumentów
**Domena:** H (zlecenia) · **Spec:** `document-requirements.md` · **Faza:** 2

| Obiekty | Funkcje kluczowe |
|---|---|
| `document_requirement` · `document_checklist` | zestawy wymagań warunkowe (mode, DG, kraj, gałąź) · **blokady, nie ostrzeżenia** · terminy ważności dokumentów · odpowiedzialna strona · przypomnienia |

**Zależy od:** M-79 (attachment), M-03 · **Rozszerza:** M-38, M-89, M-99

## M-206 · Prognoza stawki na relacji
**Domena:** L · **Spec:** `market.md` sekcja 4 · **Faza:** 9

| Obiekty | Funkcje kluczowe |
|---|---|
| `lane_rate_forecast` | prognoza z własnych danych, minimum 12 miesięcy na relacji · **obowiązkowy backtesting przeciw modelowi naiwnemu** · zawsze z przedziałem, nigdy liczba punktowa · publikowana zmierzona skuteczność · brak prognozy przy zbyt małej próbie |

**Zależy od:** M-61, M-17 · **Repozytoria:** `Nixtla/statsforecast`, `unit8co/darts`, `mlflow/mlflow`

## M-207 · Finansowanie z partnerem
**Domena:** I (finanse) · **Spec:** `finance-partner.md` · **Faza:** 9

| Obiekty | Funkcje kluczowe |
|---|---|
| `finance_partner` · `finance_program` · `finance_request` · `finance_offer` · `finance_settlement` · `finance_partner_message` · `receivable_eligibility` | **silnik kwalifikacji z czterema wykluczeniami twardymi** · faktoring wierzytelności · faktoring odwrotny · integracja z partnerem przez outbox z idempotencją · rozliczanie prowizji · ujawnienie prowizji klientowi |

**Zależy od:** M-40, M-14, M-93, M-89, M-53 · **Uwaga:** ty nie finansujesz — status instytucji obowiązanej nie powstaje

## M-208 · Dynamiczne dyskonto
**Domena:** I · **Spec:** `dynamic-discount.md` · **Faza:** 9

| Obiekty | Funkcje kluczowe |
|---|---|
| `early_payment_program` · `early_payment_offer` · `early_payment_settlement` | klient płaci z własnej gotówki wcześniej za rabat · **klient ustala formułę, terminy i budżet dzienny** · portal podwykonawcy z wyborem terminu · **model hybrydowy: własna gotówka, a przy jej braku partner** |

**Zależy od:** M-42, M-45, M-199 · **Uwaga:** nie jest faktoringiem — brak cesji, brak finansowania przez osobę trzecią

---

# CZĘŚĆ II — NOWE PLASTRY

Do `PLAN-GLOWNY.md`, część VII.

## Faza 2 — uzupełnienie

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| **2.15** | M-205 | 2.9 | `document_requirement`, `document_checklist`, sześć zestawów wymagań, blokady statusów | zlecenie bez kompletu nie przechodzi do gotowości |
| **2.16** | M-84 | 2.9 | Edytor szablonu wydruku: bloki, pola, warunki, podgląd na realnych danych | klient zmienia układ oferty bez twojego udziału |

## Faza 6 — uzupełnienie

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| **6.15** | M-202 | 6.11, 9.2 | Warstwa semantyczna Cube, `kpi_definition`, 30 wskaźników rdzeniowych | dashboard i raport podają tę samą marżę |
| **6.16** | M-202 | 6.15 | Cele, progi, dashboardy per rola, przeliczanie w tle | otwarcie dashboardu poniżej 500 ms |
| **6.17** | M-202 | 6.16 | Pozostałe ~50 wskaźników w dziewięciu kategoriach | katalog kompletny |

## Faza 7 — uzupełnienie

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| **7.16** | M-201 | 7.10 | `integration_connection`, kanał SFTP z harmonogramem, kanał mailowy | klient odbiera plik codziennie o 6:00 |
| **7.17** | M-201 | 7.16 | Kreator mapowania: wgraj plik, mapuj przeciągnięciem, podgląd 100 wierszy | integracja w godzinę zamiast tygodnia |
| **7.18** | M-201 | 7.17 | `data_share`, katalog łączników PL, iPaaS | klient dostaje swoje dane u siebie |

## Faza 8 — uzupełnienie

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| **8.16** | M-200 | 8.4 | `carrier_compliance`, blokada przypisania, weryfikacja okresowa | przewoźnik z wygasłym OCP nie da się przypisać |
| **8.17** | M-199 | 8.16 | Portal: logowanie, przyjęcie zlecenia, kierowca i pojazd, status | przewoźnik przyjmuje zlecenie bez telefonu |
| **8.18** | M-199 | 8.17 | PWA: zdjęcia i CMR z telefonu, wgrywanie dokumentów zgodnościowych | POD ze zdjęciem w systemie w dniu dostawy |
| **8.19** | M-199 | 8.18 | Faktura przewoźnika z danych zlecenia, podgląd rozliczeń i oceny | zero rozbieżności w kwotach faktur podwykonawców |

## Faza 9 — uzupełnienie

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| **9.17** | M-206 | 9.8 | `lane_rate_forecast` z backtestingiem, prognoza tylko z przedziałem | wskaźnik skuteczności publikowany, brak prognozy przy próbie < 12 mies. |
| **9.18** | M-207 | 6.5 | **`receivable_eligibility` — silnik kwalifikacji** | cztery wykluczenia twarde działają, raport zdrowia należności |
| **9.19** | M-208 | 9.18, 6.7 | `early_payment_program`, formuła dyskonta, budżet dzienny | klient uruchamia program dla wybranych podwykonawców |
| **9.20** | M-208 | 9.19, 8.17 | Portal podwykonawcy: lista faktur, wybór terminu, akceptacja | podwykonawca wybiera termin i widzi kwotę netto |
| **9.21** | M-208 | 9.20 | Rozliczenie, efektywna stopa roczna, raport korzyści obu stron | klient widzi zwrot z zaangażowanej gotówki |
| **9.22** | M-207 | 9.18 | `finance_partner`, integracja: wniosek, decyzja, uruchomienie | wniosek dociera do faktora i wraca decyzja |
| **9.23** | M-207 | 9.22 | Faktoring wierzytelności — pełna ścieżka z cesją | pierwsza faktura sfinansowana |
| **9.24** | M-207 | 9.23 | Faktoring odwrotny dla podwykonawców klienta | podwykonawca finansowany przez faktora |
| **9.25** | M-208 | 9.21, 9.24 | **Model hybrydowy: automatyczny wybór źródła finansowania** | podwykonawca widzi jedną ofertę, źródło rozstrzyga się w tle |
| **9.26** | M-207 | 9.25 | Rozliczanie prowizji, ujawnienie klientowi, raportowanie | prowizja naliczana i fakturowana automatycznie |

**Razem 20 nowych plastrów. Plan: 123 plastry.**

## Kolejność wewnątrz finansowania

Uwaga z Aneksu 26: **9.18 i 9.19 przed 9.22.** Silnik kwalifikacji i dynamiczne
dyskonto nie wymagają partnera. Uruchom je u pierwszego klienta i dopiero
z dowodem popytu idź na rozmowę o warunkach z faktorem.
---

# CZĘŚĆ III — MIGRACJE

Do `backend/alembic/versions/`. Każda tabela z `organization_id`, RLS,
audytem i wzorcami globalnymi z Aneksu 24.

## III.1 Funkcja pomocnicza — stosuj w każdej migracji

```python
def apply_tenant_policies(table: str) -> None:
    """RLS, audyt i indeks tenanta. Wywołaj dla każdej nowej tabeli."""
    op.create_index(f"ix_{table}_org", table, ["organization_id"])
    op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
    op.execute(f"""
        CREATE POLICY tenant_isolation ON {table}
        USING (
            organization_id = current_setting('app.current_org', true)::uuid
            AND current_setting('app.current_org', true) IS NOT NULL
        )
    """)
    op.execute(f"""
        CREATE TRIGGER {table}_audit
        AFTER INSERT OR UPDATE OR DELETE ON {table}
        FOR EACH ROW EXECUTE FUNCTION write_audit_log()
    """)
```

Warunek `IS NOT NULL` wynika z błędu wykrytego przy plastrze 0.3:
`current_setting` z drugim argumentem zwraca NULL zamiast błędu, więc bez
tego polityka przepuszcza zapytania bez kontekstu.

## III.2 M-205 · Wymagalność dokumentów

```sql
CREATE TABLE document_requirement (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    entity_type         text NOT NULL,
    condition           jsonb NOT NULL DEFAULT '{}',
    document_kind       text NOT NULL,
    is_mandatory        boolean NOT NULL DEFAULT true,
    blocks              text[] NOT NULL DEFAULT '{}',
    valid_period_days   integer,
    reminder_days_before integer DEFAULT 30,
    responsible_party   text NOT NULL,
    effective_from      date NOT NULL DEFAULT CURRENT_DATE,
    effective_to        date,
    version             integer NOT NULL DEFAULT 1,
    created_source      text NOT NULL DEFAULT 'manual',
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    created_by          uuid REFERENCES app_user(id),
    deleted_at          timestamptz,
    deleted_by          uuid REFERENCES app_user(id)
);

CREATE INDEX ix_docreq_lookup ON document_requirement
    (organization_id, entity_type, document_kind)
    WHERE deleted_at IS NULL;

-- checklist jako widok materializowany, odświeżany zdarzeniem
CREATE MATERIALIZED VIEW document_checklist AS
SELECT
    r.organization_id,
    r.entity_type,
    e.entity_id,
    count(*) FILTER (WHERE r.is_mandatory)              AS required_count,
    count(a.id) FILTER (WHERE r.is_mandatory)           AS provided_count,
    array_agg(r.document_kind) FILTER (
        WHERE r.is_mandatory AND a.id IS NULL)          AS missing,
    array_agg(r.document_kind) FILTER (
        WHERE a.valid_to < CURRENT_DATE)                AS expired,
    bool_and(a.id IS NOT NULL OR NOT r.is_mandatory)    AS is_complete
FROM document_requirement r
CROSS JOIN LATERAL (SELECT ...) e
LEFT JOIN attachment a
       ON a.entity_type = r.entity_type
      AND a.entity_id   = e.entity_id
      AND a.document_kind = r.document_kind
      AND a.deleted_at IS NULL
WHERE r.deleted_at IS NULL
GROUP BY r.organization_id, r.entity_type, e.entity_id;

CREATE UNIQUE INDEX ix_checklist_pk ON document_checklist
    (organization_id, entity_type, entity_id);
```

Zgodnie z zasadą z Aneksu 25: **nic prezentowanego na liście nie jest liczone
przy otwarciu listy.** Checklist odświeżany zdarzeniem `attachment.added`.

## III.3 M-200 · Zgodność podwykonawców

```sql
CREATE TABLE carrier_compliance (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    party_id            uuid NOT NULL REFERENCES party(id),
    document_kind       text NOT NULL,
    number              text,
    issuer              text,
    insured_sum         numeric(14,2),
    currency            char(3) REFERENCES currency(code),
    scope               jsonb,
    valid_from          date,
    valid_to            date,
    attachment_id       uuid REFERENCES attachment(id),
    verified_by         uuid REFERENCES app_user(id),
    verified_at         timestamptz,
    status              text NOT NULL DEFAULT 'missing',
    blocks_assignment   boolean NOT NULL DEFAULT true,
    next_review_at      date,
    created_source      text NOT NULL DEFAULT 'manual',
    is_manually_overridden boolean NOT NULL DEFAULT false,
    override_reason     text,
    overridden_by       uuid REFERENCES app_user(id),
    overridden_at       timestamptz,
    version             integer NOT NULL DEFAULT 1,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    created_by          uuid REFERENCES app_user(id),
    deleted_at          timestamptz,
    CONSTRAINT chk_status CHECK (status IN
        ('valid','expiring','expired','missing','rejected'))
);

CREATE INDEX ix_compliance_blocking ON carrier_compliance
    (organization_id, party_id)
    WHERE blocks_assignment AND status IN ('expired','missing')
      AND deleted_at IS NULL;

CREATE INDEX ix_compliance_expiring ON carrier_compliance
    (organization_id, valid_to)
    WHERE status = 'valid' AND deleted_at IS NULL;

CREATE TABLE carrier_vehicle (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    party_id            uuid NOT NULL REFERENCES party(id),
    plate               text NOT NULL,
    kind                text NOT NULL,
    adr_valid_to        date,
    inspection_valid_to date,
    is_approved         boolean NOT NULL DEFAULT false,
    approved_at         timestamptz,
    approved_by         uuid REFERENCES app_user(id),
    version             integer NOT NULL DEFAULT 1,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    deleted_at          timestamptz,
    UNIQUE (organization_id, plate)
);

CREATE TABLE carrier_rating (
    organization_id     uuid NOT NULL REFERENCES organization(id),
    party_id            uuid NOT NULL REFERENCES party(id),
    period              date NOT NULL,
    on_time_pickup_pct  numeric(5,2),
    on_time_delivery_pct numeric(5,2),
    damage_incidents    integer NOT NULL DEFAULT 0,
    claim_amount        numeric(14,2),
    doc_completeness_pct numeric(5,2),
    response_time_hours numeric(6,2),
    price_rank          integer,
    overall_score       numeric(5,2),
    computed_at         timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id, party_id, period)
);
```

**Funkcja blokująca przypisanie:**

```sql
CREATE FUNCTION check_carrier_eligible(p_org uuid, p_party uuid)
RETURNS TABLE (eligible boolean, blocking text[]) AS $$
    SELECT
        NOT EXISTS (
            SELECT 1 FROM carrier_compliance
            WHERE organization_id = p_org AND party_id = p_party
              AND blocks_assignment
              AND status IN ('expired','missing')
              AND deleted_at IS NULL
        ),
        COALESCE(array_agg(document_kind) FILTER (
            WHERE status IN ('expired','missing')), '{}')
    FROM carrier_compliance
    WHERE organization_id = p_org AND party_id = p_party
      AND blocks_assignment AND deleted_at IS NULL;
$$ LANGUAGE sql STABLE;
```

Wywoływana przy tworzeniu `carrier_order`. Zwolnienie wyłącznie przez
`approval_request` z M-179.

## III.4 M-201 · Hub integracyjny

```sql
CREATE TABLE integration_connection (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    name                text NOT NULL,
    direction           text NOT NULL,
    transport           text NOT NULL,
    format              text NOT NULL,
    schedule            text NOT NULL DEFAULT 'manual',
    cron_expression     text,
    entity_types        text[] NOT NULL,
    mapping_id          uuid,
    credentials_encrypted bytea,
    endpoint_config     jsonb NOT NULL DEFAULT '{}',
    is_active           boolean NOT NULL DEFAULT false,
    last_run_at         timestamptz,
    last_status         text,
    consecutive_failures integer NOT NULL DEFAULT 0,
    version             integer NOT NULL DEFAULT 1,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    created_by          uuid REFERENCES app_user(id),
    deleted_at          timestamptz,
    CONSTRAINT chk_transport CHECK (transport IN
        ('rest','webhook','sftp','email','ftp','s3','manual_upload','edi')),
    CONSTRAINT chk_direction CHECK (direction IN
        ('inbound','outbound','bidirectional'))
);

CREATE TABLE integration_mapping (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    name                text NOT NULL,
    entity_type         text NOT NULL,
    source_schema       jsonb,
    field_mappings      jsonb NOT NULL,
    transformations     jsonb NOT NULL DEFAULT '[]',
    validation_rules    jsonb NOT NULL DEFAULT '[]',
    sample_payload      jsonb,
    version             integer NOT NULL DEFAULT 1,
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now(),
    created_by          uuid REFERENCES app_user(id)
);

ALTER TABLE integration_connection
    ADD CONSTRAINT fk_mapping FOREIGN KEY (mapping_id)
    REFERENCES integration_mapping(id);

CREATE TABLE integration_run (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    connection_id       uuid NOT NULL REFERENCES integration_connection(id),
    started_at          timestamptz NOT NULL DEFAULT now(),
    finished_at         timestamptz,
    records_in          integer NOT NULL DEFAULT 0,
    records_ok          integer NOT NULL DEFAULT 0,
    records_failed      integer NOT NULL DEFAULT 0,
    errors              jsonb NOT NULL DEFAULT '[]',
    file_path           text,
    triggered_by        text NOT NULL DEFAULT 'schedule'
) PARTITION BY RANGE (started_at);

CREATE TABLE data_share (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    party_id            uuid NOT NULL REFERENCES party(id),
    scope               text NOT NULL,
    connection_id       uuid REFERENCES integration_connection(id),
    filters             jsonb NOT NULL DEFAULT '{}',
    field_whitelist     text[],
    api_key_id          uuid REFERENCES api_key(id),
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now()
);
```

`integration_run` partycjonowane miesięcznie — refaktoryzacja R-04 z Aneksu 25.

## III.5 M-202 · Framework pomiarowy

```sql
CREATE TABLE kpi_definition (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid REFERENCES organization(id),   -- NULL = systemowa
    code                text NOT NULL,
    name                text NOT NULL,
    description         text,
    category            text NOT NULL,
    cube_measure        text NOT NULL,     -- odwołanie do warstwy semantycznej
    unit                text NOT NULL,
    direction           text NOT NULL,
    aggregation         text NOT NULL DEFAULT 'sum',
    dimensions          text[] NOT NULL DEFAULT '{}',
    refresh_frequency   text NOT NULL DEFAULT 'daily',
    is_active           boolean NOT NULL DEFAULT true,
    version             integer NOT NULL DEFAULT 1,
    created_at          timestamptz NOT NULL DEFAULT now(),
    UNIQUE (organization_id, code),
    CONSTRAINT chk_category CHECK (category IN
        ('customer','quote','shipment','carrier','agent',
         'employee','financial','operational','quality'))
);

CREATE TABLE kpi_target (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    kpi_id              uuid NOT NULL REFERENCES kpi_definition(id),
    dimension_key       text,
    dimension_ref       uuid,
    period              date NOT NULL,
    target_value        numeric(18,4) NOT NULL,
    threshold_warning   numeric(18,4),
    threshold_critical  numeric(18,4),
    set_by              uuid REFERENCES app_user(id),
    approved_by         uuid REFERENCES app_user(id),
    created_at          timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE kpi_measurement (
    organization_id     uuid NOT NULL REFERENCES organization(id),
    kpi_id              uuid NOT NULL REFERENCES kpi_definition(id),
    dimension_key       text NOT NULL DEFAULT '',
    dimension_ref       uuid,
    period              date NOT NULL,
    value               numeric(18,4) NOT NULL,
    target_value        numeric(18,4),
    variance_pct        numeric(8,2),
    status              text,
    trend               text,
    computed_at         timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id, kpi_id, dimension_key,
                 COALESCE(dimension_ref, '00000000-0000-0000-0000-000000000000'),
                 period)
);

CREATE INDEX ix_kpi_dashboard ON kpi_measurement
    (organization_id, period DESC, kpi_id);
```

**`cube_measure` jest tu kluczowe.** Wskaźnik nie ma własnej formuły SQL —
odwołuje się do miary zdefiniowanej w warstwie semantycznej. Dzięki temu
dashboard, raport, eksport i zapytanie językiem naturalnym liczą to samo.

## III.6 M-207 i M-208 · Finansowanie

```sql
CREATE TABLE finance_partner (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid REFERENCES organization(id),   -- NULL = partner platformy
    name                text NOT NULL,
    kind                text NOT NULL,
    products            text[] NOT NULL,
    api_endpoint        text,
    auth_method         text,
    credentials_encrypted bytea,
    min_invoice         numeric(14,2),
    max_invoice         numeric(14,2),
    currencies          char(3)[] NOT NULL,
    advance_rate_pct    numeric(5,2),
    fee_structure       jsonb NOT NULL DEFAULT '{}',
    decision_sla_hours  integer,
    our_commission_model jsonb NOT NULL DEFAULT '{}',
    agreement_ref       text,
    valid_from          date,
    valid_to            date,
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE finance_program (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    partner_id          uuid REFERENCES finance_partner(id),
    product             text NOT NULL,
    name                text NOT NULL,
    is_active           boolean NOT NULL DEFAULT false,
    eligible_debtors    uuid[],
    eligible_suppliers  uuid[],
    limit_total         numeric(14,2),
    limit_per_party     numeric(14,2),
    currency            char(3) NOT NULL REFERENCES currency(code),
    discount_formula    jsonb,
    min_days_early      integer,
    max_days_early      integer,
    daily_budget        numeric(14,2),
    auto_offer          boolean NOT NULL DEFAULT false,
    auto_approve_below  numeric(14,2),
    approval_policy_id  uuid REFERENCES approval_policy(id),
    version             integer NOT NULL DEFAULT 1,
    created_at          timestamptz NOT NULL DEFAULT now(),
    created_by          uuid REFERENCES app_user(id),
    CONSTRAINT chk_product CHECK (product IN
        ('receivables','reverse','dynamic_discount','hybrid'))
);

CREATE TABLE receivable_eligibility (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    invoice_id          uuid NOT NULL REFERENCES invoice(id),
    computed_at         timestamptz NOT NULL DEFAULT now(),

    -- wykluczenia twarde
    assignment_allowed      boolean NOT NULL,
    has_active_dispute      boolean NOT NULL,
    is_credit_noted         boolean NOT NULL,
    debtor_is_related_party boolean NOT NULL,
    debtor_sanctions_hit    boolean NOT NULL,

    -- jakość dokumentacji
    delivery_confirmed      boolean NOT NULL,
    documents_complete      boolean NOT NULL,
    shipment_closed         boolean NOT NULL,

    -- jakość dłużnika
    debtor_credit_score     numeric(5,2),
    debtor_dso_actual       integer,
    debtor_reliability      numeric(5,2),
    debtor_open_exposure    numeric(14,2),

    eligibility_score       numeric(5,2),
    recommendation          text,
    blocking_reasons        text[] NOT NULL DEFAULT '{}',
    UNIQUE (invoice_id, computed_at)
);

CREATE INDEX ix_eligible_invoices ON receivable_eligibility
    (organization_id, eligibility_score DESC)
    WHERE cardinality(blocking_reasons) = 0;

CREATE TABLE early_payment_offer (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    program_id          uuid NOT NULL REFERENCES finance_program(id),
    bill_id             uuid NOT NULL REFERENCES bill(id),
    supplier_party_id   uuid NOT NULL REFERENCES party(id),
    original_due_date   date NOT NULL,
    offered_payment_date date NOT NULL,
    original_amount     numeric(14,2) NOT NULL,
    discount_amount     numeric(14,2) NOT NULL,
    net_amount          numeric(14,2) NOT NULL,
    currency            char(3) NOT NULL REFERENCES currency(code),
    effective_annual_rate numeric(6,2),
    funding_source      text NOT NULL,      -- buyer_own_cash | partner
    offered_at          timestamptz NOT NULL DEFAULT now(),
    expires_at          timestamptz NOT NULL,
    status              text NOT NULL DEFAULT 'offered',
    accepted_at         timestamptz,
    accepted_by         uuid,
    paid_at             timestamptz,
    idempotency_key     text UNIQUE,
    version             integer NOT NULL DEFAULT 1,
    CONSTRAINT chk_eps CHECK (status IN
        ('offered','accepted','rejected','expired','paid','cancelled'))
);

CREATE INDEX ix_eps_supplier ON early_payment_offer
    (organization_id, supplier_party_id, status)
    WHERE status = 'offered';
```

**`idempotency_key` na `early_payment_offer`** — zasada 13. Duplikat oferty
wcześniejszej zapłaty oznaczałby podwójny przelew.

## III.7 Brakujące tabele referencyjne z Aneksu 24

Wymagane przez powyższe, wcześniej nieistniejące:

```sql
CREATE TABLE currency (
    code        char(3) PRIMARY KEY,
    name_pl     text NOT NULL,
    name_en     text NOT NULL,
    decimals    smallint NOT NULL DEFAULT 2,
    symbol      text,
    is_active   boolean NOT NULL DEFAULT true
);
INSERT INTO currency VALUES
    ('PLN','złoty polski','Polish zloty',2,'zł',true),
    ('EUR','euro','Euro',2,'€',true),
    ('USD','dolar amerykański','US dollar',2,'$',true),
    ('JPY','jen japoński','Japanese yen',0,'¥',true),
    ('KWD','dinar kuwejcki','Kuwaiti dinar',3,NULL,true);
```

**Kolumna `decimals` nie jest ozdobnikiem.** JPY ma zero miejsc, KWD trzy.
Zaokrąglanie do dwóch daje błędne kwoty na fakturach.
---

# CZĘŚĆ IV — ZMIANY W ISTNIEJĄCYCH MODUŁACH

## IV.1 Rozszerzenia tabel

```sql
-- M-93: potrzebne przez silnik kwalifikacji (M-207)
ALTER TABLE customer_agreement
    ADD COLUMN assignment_allowed boolean NOT NULL DEFAULT true,
    ADD COLUMN assignment_clause_text text;

-- M-89: potwierdzenie dostawy jako warunek finansowania
ALTER TABLE proof_of_delivery
    ADD COLUMN verified_by uuid REFERENCES app_user(id),
    ADD COLUMN verified_at timestamptz;

-- M-79: załącznik musi znać swój rodzaj, żeby checklist działał
ALTER TABLE attachment
    ADD COLUMN document_kind text,
    ADD COLUMN valid_from date,
    ADD COLUMN valid_to date,
    ADD COLUMN issued_by text,
    ADD COLUMN document_number text;

CREATE INDEX ix_attachment_kind ON attachment
    (organization_id, entity_type, entity_id, document_kind)
    WHERE deleted_at IS NULL;

-- M-84: edytor szablonów
ALTER TABLE document_layout
    ADD COLUMN blocks jsonb NOT NULL DEFAULT '[]',
    ADD COLUMN editor_version integer NOT NULL DEFAULT 1,
    ADD COLUMN preview_entity_id uuid;

-- M-35: powiązanie z bookingiem (brak wykryty w audycie)
ALTER TABLE shipment
    ADD COLUMN booking_id uuid REFERENCES booking(id);

-- M-06: konto księgowe (brak wykryty w audycie)
ALTER TABLE charge_code
    ADD COLUMN account_code text,
    ADD COLUMN account_code_cost text;

-- M-05: strefa czasowa portu (brak wykryty w audycie)
ALTER TABLE port
    ADD COLUMN timezone text,
    ADD COLUMN country_code char(2) REFERENCES country(code);
```

## IV.2 Zdarzenia międzymodułowe

Do rejestru zdarzeń outbox. Wzorzec W-06 z Aneksu 24.

```
attachment.added                → document_checklist.refresh
attachment.expired              → carrier_compliance.recheck
carrier_compliance.expired      → carrier_order.block_assignment
carrier_order.completed         → carrier_rating.recompute
invoice.issued                  → receivable_eligibility.compute
bill.approved                   → early_payment_offer.generate
early_payment_offer.accepted    → payment.schedule
finance_settlement.funded       → cash_flow_forecast.refresh
shipment.closed                 → kpi_measurement.refresh
document_checklist.incomplete   → shipment.block_status_change
```

## IV.3 Uzupełnienie ręcznej korekty

Wynika z audytu w Aneksie 24, wymiar 1. Dla nowych modułów wzorzec W-01
zastosowany od razu — wszystkie tabele mają `created_source`,
`is_manually_overridden`, `override_reason`.

Konkretne drogi ręczne do zbudowania:

| Moduł | Droga ręczna |
|---|---|
| M-200 | ręczne oznaczenie dokumentu jako zweryfikowanego, zwolnienie blokady przez zatwierdzenie |
| M-201 | ręczne uruchomienie połączenia, ręczna korekta mapowania, ponowienie nieudanego przebiegu |
| M-202 | ręczna korekta wartości wskaźnika z uzasadnieniem, wykluczenie okresu z wyliczenia |
| M-205 | oznaczenie dokumentu jako niewymaganego dla konkretnego zlecenia z powodem |
| M-206 | ręczne nadpisanie prognozy, oznaczenie relacji jako nieprognozowalnej |
| M-207 | ręczne wprowadzenie wniosku złożonego poza systemem, ręczne dopasowanie spłaty |
| M-208 | ręczne utworzenie oferty poza harmonogramem, ręczna zmiana warunków |

## IV.4 Nowe wpisy w `AGENTS.md`

```
18. Każda wartość prezentowana na liście jest wyliczona wcześniej
    i zapisana. Nic nie liczy się przy otwarciu ekranu.
19. Operacje finansowe wymagają klucza idempotencji i przechodzą
    przez outbox. Bez wyjątków.
20. Kwoty zaokrąglaj według liczby miejsc z tabeli currency,
    nigdy na sztywno do dwóch.
```

## IV.5 Nowe bramki w CI

```yaml
- name: Idempotencja operacji finansowych
  run: pytest -m financial_idempotency --strict-markers

- name: Kompletność wzorca korekty ręcznej
  run: python scripts/quality/check_manual_override.py
```

`check_manual_override.py` sprawdza, czy każda tabela z `created_source`
ma komplet kolumn wzorca W-01. Zapobiega powstawaniu luki, którą wykrył audyt.

---

# CZĘŚĆ V — PLIKI SPECYFIKACJI

Do utworzenia w `docs/spec/`. Struktura wg procedury kompilacji.

| Plik | Moduł | Źródło | Szacowana długość |
|---|---|---|---|
| `carrier-portal.md` | M-199 | Aneks 25 cz. II | ~180 linii |
| `carrier-compliance.md` | M-200 | Aneks 25 §1.2 | ~150 linii |
| `integration-hub.md` | M-201 | Aneks 25 §1.3 | ~280 linii |
| `kpi.md` | M-202 | Aneks 25 §1.4 | ~320 linii |
| `document-requirements.md` | M-205 | Aneks 25 §1.1 | ~160 linii |
| `finance-partner.md` | M-207 | Aneks 26 §2.1, 2.2, 4, 5 | ~300 linii |
| `dynamic-discount.md` | M-208 | Aneks 26 §2.3, 2.4 | ~220 linii |
| `market.md` (aktualizacja) | M-206 | Aneks 26 cz. IV | +80 linii |

**Polecenie do kompilacji** — do użycia w Claude Code:

```
Skompiluj docs/spec/ dla modułów M-199, M-200, M-205 na podstawie
ANEKS-25-portal-faktoring-kpi.md sekcje 1.1, 1.2 i część II.

Struktura pliku jak w pozostałych: Cel, Obiekty danych, Reguły biznesowe,
Zależności, Rozstrzygnięcia, Kryteria akceptacji.

Zasady: maksimum 400 linii, odsyłacze [[M-xx]], zero powtórzeń,
brak interpretacji — braki oznacz jako DO USTALENIA.

Zachowaj dokładnie: cztery wykluczenia twarde silnika kwalifikacji,
blokady przypisania przy wygasłym OCP, osiem kanałów integracji.
```

---

# CZĘŚĆ VI — STAN PROJEKTU PO INTEGRACJI

## VI.1 Statystyki

| | Przed | Po |
|---|---|---|
| Moduły | 198 | **208** |
| Plastry | 103 | **123** |
| Nowe tabele | — | 21 |
| Rozszerzone tabele | — | 7 |
| Nowe zdarzenia outbox | — | 10 |
| Zasady w `AGENTS.md` | 17 | **20** |
| Bramki CI | 14 | **16** |

## VI.2 Rozkład nakładu na fazy

| Faza | Plastry przed | Nowe | Dodatkowe dni |
|---|---|---|---|
| 2 | 16 | +2 | +10 |
| 6 | 15 | +3 | +10 |
| 7 | 15 | +3 | +15 |
| 8 | 19 | +4 | +17 |
| 9 | 26 | +10 | +53 |

**Razem +105 dni.** Fazy 0–3 rosną o 10 dni — punkt kontrolny po fazie 2
przesuwa się nieznacznie.

## VI.3 Co weszło do faz wczesnych i dlaczego

**2.15 wymagalność dokumentów** — bo blokady kompletności są warunkiem
sensownego demo. System, który pozwala zamknąć zlecenie bez B/L, wygląda
na prototyp.

**2.16 edytor szablonów** — bo klient, który nie może sam zmienić układu
oferty, będzie o to prosił przy każdym drobiazgu. To koszt wsparcia, nie funkcja.

Reszta świadomie w fazach 6–9: portal przewoźnika wymaga działającego modułu
drogowego, finansowanie wymaga fakturowania i rozliczeń, KPI wymaga warstwy
semantycznej.

## VI.4 Trzy rzeczy do rozstrzygnięcia przed fazą 9

| # | Decyzja | Termin |
|---|---|---|
| O-07 | **Wyłączność dla partnera faktoringowego** czy model wielu partnerów | przed 9.22 |
| O-08 | Model prowizji: od wniosku, uruchomienia czy spłaty | przed 9.22 |
| O-09 | Udział w dyskoncie przy dynamicznym dyskoncie: procent czy opłata za moduł | przed 9.19 |

**O-07 wpływa na architekturę.** Model wielu partnerów wymaga porównywarki
ofert i kolejkowania wniosków; wyłączność upraszcza moduł, ale odbiera
argument sprzedażowy.

## VI.5 Kolejność w obrębie finansowania — przypomnienie

```
9.18  silnik kwalifikacji        ← wartościowy sam w sobie, bez partnera
9.19  dynamiczne dyskonto        ← bez partnera, dowód popytu
9.20  portal podwykonawcy
9.21  rozliczenie i raport korzyści
      ────────── dopiero teraz rozmowa z faktorem ──────────
9.22  integracja z partnerem
9.23  faktoring wierzytelności
9.24  faktoring odwrotny
9.25  model hybrydowy
9.26  prowizje i ujawnienie
```

Dziesięć dni na plastry 9.18–9.21 daje ci odpowiedź, czy podwykonawcy
twoich klientów w ogóle chcą wcześniejszej zapłaty. **Z tą odpowiedzią
idziesz na rozmowę z faktorem w innej pozycji negocjacyjnej niż z pomysłem.**

## VI.6 Aktualizacja cennika

Nowe moduły wchodzą do oferty jako dodatki:

| Dodatek | Cena | Uwaga |
|---|---|---|
| Portal przewoźnika | 390 zł/mies. | do 20 przewoźników, powyżej +10 zł za każdego |
| Hub integracyjny | 490 zł/mies. | jedno połączenie w cenie, kolejne po 190 zł |
| Framework KPI | w pakiecie Pro | wyróżnik pakietu wyższego |
| Program wcześniejszej zapłaty | **15% zrealizowanego dyskonta** | albo 690 zł/mies. ryczałtem |
| Pośrednictwo faktoringowe | prowizja od partnera | dla klienta bezpłatne |

**Model prowizyjny przy dyskoncie jest twoim najlepszym produktem finansowym** —
klient płaci własną gotówką, ty dostarczasz mechanizm i bierzesz udział
w korzyści, której bez ciebie by nie było.
