import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchFuelAnomalyMarks, type FuelAnomalyMarkRow } from "@/lib/fuel-anomaly-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FuelAnomalyIntake } from "./mark-form"

const col = createColumnHelper<FuelAnomalyMarkRow>()

const TABLE = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("anomaly_kind", { header: "Rodzaj" }),
  col.accessor("source_ref", { header: "Źródło" }),
]

export function FuelAnomalyCatalog() {
  const ctx = getTenantContext()
  const org = ctx.organizationId
  const signedIn = Boolean(org && ctx.userId)
  const list = useQuery({
    enabled: signedIn,
    queryFn: fetchFuelAnomalyMarks,
    queryKey: ["fuel-anomaly-marks", org],
    retry: false,
  })

  return (
    <article className="space-y-8" data-fuel="catalog">
      <CatalogHeading
        title="Fuel anomaly"
        subtitle="EXP2.14 · katalog HITL · card/tank/spike · bez live fuel card"
      />
      {!signedIn ? <TenantSessionNotice /> : null}
      {signedIn ? <FuelAnomalyIntake organizationId={org} /> : null}
      {list.error ? <CatalogError error={list.error} /> : null}
      {signedIn && list.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            anomaly_kind: "Rodzaj",
            source_ref: "Źródło",
          }}
          columns={TABLE}
          data={list.data ?? []}
          globalFilterPlaceholder="Filtruj anomalie…"
          tableKey={BUSINESS_LISTS.fuelAnomalyMark.tableKey}
        />
      ) : null}
    </article>
  )
}
