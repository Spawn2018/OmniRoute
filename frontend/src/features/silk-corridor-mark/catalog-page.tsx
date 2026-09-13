import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchSilkCorridorMarks,
  type SilkCorridorMarkRow,
} from "@/lib/silk-corridor-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SilkCorridorMarkSave } from "./mark-form"

const helper = createColumnHelper<SilkCorridorMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("corridor_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function SilkCorridorMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchSilkCorridorMarks,
    queryKey: ["silk-corridor-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-silk-corridor-mark="board">
      <CatalogHeading
        title="Jedwabny Szlak"
        subtitle="BR4.4 silk_corridor_mark · katalog HITL · nie live CR Express · nie lane_pattern"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SilkCorridorMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            corridor_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj stance Jedwabnego Szlaku…"
          tableKey={BUSINESS_LISTS.silkCorridorMark.tableKey}
        />
      ) : null}
    </section>
  )
}
