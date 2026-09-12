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
  loadPoBatchMarks,
  type PoBatchMarkRow,
} from "@/lib/po-batch-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PoBatchMarkComposer } from "./mark-form"

const helper = createColumnHelper<PoBatchMarkRow>()
const COLS = [
  helper.accessor("batch_kind", { header: "Batch" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function PoBatchMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadPoBatchMarks,
    queryKey: ["po-batch-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-pbm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Znacznik PO batch"
          subtitle="EXP3.0d · batch|lot|serial|other · bez live EDI"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik batch/lot na linii PO — tylko katalog danych.</li>
          <li>Bez live EDI i bez auto shipment.</li>
          <li>Odrębny od purchase_orders, po_plant_mark i po_sku_mark.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow po batch.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              batch_kind: "Batch",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika po batch…"
            tableKey={BUSINESS_LISTS.poBatchMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <PoBatchMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
