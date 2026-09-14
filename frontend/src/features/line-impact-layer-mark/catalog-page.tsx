import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchLineImpactLayerMarks,
  type LineImpactLayerMarkRow,
} from "@/lib/line-impact-layer-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LineImpactLayerMarkSave } from "./mark-form"

const col = createColumnHelper<LineImpactLayerMarkRow>()

export function LineImpactLayerMarkDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const sessionOk = Boolean(org && tenant.userId)
  const rows = useQuery({
    enabled: sessionOk,
    queryFn: fetchLineImpactLayerMarks,
    queryKey: ["line-impact-layer-marks", org],
    retry: false,
  })
  const tableCols = [
    col.accessor("mark_code", { header: "Oznaczenie" }),
    col.accessor("layer_kind", { header: "Tryb" }),
    col.accessor("source_ref", { header: "Pochodzenie" }),
  ]

  return (
    <main className="space-y-5 p-1" data-line-impact-layer="desk">
      <CatalogHeading
        title="Warstwa liczona wpływu na linię"
        subtitle="BR7.1 · scored / forecast / actual · bez SQL EBITDA i bez plant feed"
      />
      {sessionOk ? null : <TenantSessionNotice />}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {sessionOk && !rows.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            layer_kind: "Tryb",
            source_ref: "Pochodzenie",
          }}
          columns={tableCols}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj warstwy…"
          tableKey={BUSINESS_LISTS.lineImpactLayerMark.tableKey}
        />
      ) : null}
      {sessionOk ? <LineImpactLayerMarkSave organizationId={org} /> : null}
    </main>
  )
}
