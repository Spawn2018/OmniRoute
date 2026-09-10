import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listLaneKms, type LaneKmRow } from "@/lib/lane-kms-api"
import { getTenantContext } from "@/lib/tenant"
import { LaneKmSave } from "./lane-km-form"

const helper = createColumnHelper<LaneKmRow>()

const columns = [
  helper.accessor("km_code", { header: "Kod" }),
  helper.accessor("loaded_km", { header: "Ładowny" }),
  helper.accessor("empty_km", { header: "Pusty" }),
  helper.accessor("approach_km", { header: "Dolot" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  km_code: "Kod",
  loaded_km: "Ładowny",
  empty_km: "Pusty",
  approach_km: "Dolot",
  source_ref: "Pochodzenie",
}

function LaneKmRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["lane-kms", args.organizationId],
    queryFn: listLaneKms,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <div className="min-w-0 flex-1">
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <DataTableShell
        tableKey={BUSINESS_LISTS.laneKm.tableKey}
        columns={columns}
        data={listed.data ?? []}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj km korytarza…"
      />
    </div>
  )
}

export function LaneKmDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-lane-km="desk">
      <CatalogHeading
        title="Km ładowny"
        subtitle="G2.21 lane_km · ładowny/pusty/dolot jako dane · nie Haversine"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <LaneKmSave organizationId={ctx.organizationId} />
          <LaneKmRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
