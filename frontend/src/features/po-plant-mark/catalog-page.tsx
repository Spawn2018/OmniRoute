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
  loadPoPlantMarks,
  type PoPlantMarkRow,
} from "@/lib/po-plant-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PoPlantMarkComposer } from "./mark-form"

const helper = createColumnHelper<PoPlantMarkRow>()
const COLS = [
  helper.accessor("plant_kind", { header: "Plant" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function PoPlantMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadPoPlantMarks,
    queryKey: ["po-plant-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-ppm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Znacznik PO plant"
          subtitle="EXP3.0b · plant|batch|sku|other · bez live EDI"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik plant/batch/SKU na PO — tylko katalog danych.</li>
          <li>Bez live EDI i bez auto shipment.</li>
          <li>Odrębny od purchase_orders — znacznik katalogowy, nie nagłówek PO.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow po plant.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              plant_kind: "Plant",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika po plant…"
            tableKey={BUSINESS_LISTS.poPlantMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <PoPlantMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
