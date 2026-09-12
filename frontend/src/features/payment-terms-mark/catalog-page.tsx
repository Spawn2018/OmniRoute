import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadPaymentTermsMarks,
  type PaymentTermsMarkRow,
} from "@/lib/payment-terms-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PaymentTermsMarkComposer } from "./mark-form"

const helper = createColumnHelper<PaymentTermsMarkRow>()
const COLS = [
  helper.accessor("terms_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function PaymentTermsMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadPaymentTermsMarks,
    queryKey: ["payment-terms-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-ptm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Warunki platnosci"
          subtitle="EXP1 · net|prepaid|other · bez kolumny shipment"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik warunkow platnosci — tylko katalog danych.</li>
          <li>Bez kolumny na shipment i bez payment_terms_days.</li>
          <li>Odrębny od charge, party i od ekstrakcji LLM.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow warunkow platnosci.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              terms_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika warunkow platnosci…"
            tableKey={BUSINESS_LISTS.paymentTermsMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <PaymentTermsMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
