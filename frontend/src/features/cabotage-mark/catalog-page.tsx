import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadCabotageMarks, type CabotageMarkRow } from "@/lib/cabotage-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CabotageMarkForm } from "./mark-form"

const columns = createColumnHelper<CabotageMarkRow>()

const TABLE_COLS = [
  columns.accessor("mark_code", { header: "Kod" }),
  columns.accessor("cabotage_kind", { header: "Rodzaj" }),
  columns.accessor("source_ref", { header: "Źródło" }),
]

export function CabotageMarkPage() {
  const ctx = getTenantContext()
  const org = ctx.organizationId
  const signedIn = Boolean(org && ctx.userId)
  const list = useQuery({
    enabled: signedIn,
    queryFn: loadCabotageMarks,
    queryKey: ["cabotage-marks", org],
    retry: false,
  })

  return (
    <div className="space-y-6" data-cabotage="page">
      <CatalogHeading
        title="Kabotaż"
        subtitle="EXP2.11 · HITL · counter / driver_return / vehicle_return · bez silnika"
      />
      {!signedIn ? <TenantSessionNotice /> : null}
      {signedIn ? <CabotageMarkForm organizationId={org} /> : null}
      {list.error ? <CatalogError error={list.error} /> : null}
      {signedIn && !list.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            cabotage_kind: "Rodzaj",
            source_ref: "Źródło",
          }}
          columns={TABLE_COLS}
          data={list.data ?? []}
          globalFilterPlaceholder="Szukaj kabotażu…"
          tableKey={BUSINESS_LISTS.cabotageMark.tableKey}
        />
      ) : null}
    </div>
  )
}
