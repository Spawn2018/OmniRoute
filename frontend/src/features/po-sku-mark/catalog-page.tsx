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
  loadPoSkuMarks,
  type PoSkuMarkRow,
} from "@/lib/po-sku-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PoSkuMarkComposer } from "./mark-form"

const helper = createColumnHelper<PoSkuMarkRow>()
const COLS = [
  helper.accessor("sku_kind", { header: "SKU" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function PoSkuMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadPoSkuMarks,
    queryKey: ["po-sku-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-psm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Znacznik PO SKU"
          subtitle="EXP3.0c · sku|gtin|customer_sku|other · bez live EDI"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik SKU na linii PO — tylko katalog danych.</li>
          <li>Bez live EDI i bez auto shipment.</li>
          <li>Odrębny od purchase_orders i po_plant_mark — znacznik katalogowy.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow po sku.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              sku_kind: "SKU",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika po sku…"
            tableKey={BUSINESS_LISTS.poSkuMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <PoSkuMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
