import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchOpsRoomMarks, type OpsRoomMarkRow } from "@/lib/ops-room-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OpsRoomMarkSave } from "./mark-form"

const helper = createColumnHelper<OpsRoomMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("layer_kind", { header: "Warstwa" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function OpsRoomMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchOpsRoomMarks,
    queryKey: ["ops-room-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-ops-room-mark="board">
      <CatalogHeading
        title="Sala operacyjna — warstwa"
        subtitle="BR7.0 ops_room_mark · HITL shift/board/escalation · nie N8 · nie widok sklejony"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <OpsRoomMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            layer_kind: "Warstwa",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj warstwy sali…"
          tableKey={BUSINESS_LISTS.opsRoomMark.tableKey}
        />
      ) : null}
    </section>
  )
}
