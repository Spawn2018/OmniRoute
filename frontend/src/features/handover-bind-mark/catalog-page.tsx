import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchHandoverBindMarks,
  type HandoverBindMarkRow,
} from "@/lib/handover-bind-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { HandoverBindMarkSave } from "./mark-form"

const bindCol = createColumnHelper<HandoverBindMarkRow>()

const BIND_COLUMNS = [
  bindCol.accessor("mark_code", { header: "Kod" }),
  bindCol.accessor("bind_kind", { header: "Wiązanie" }),
  bindCol.accessor("source_ref", { header: "source_ref" }),
]

export function HandoverBindMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchHandoverBindMarks,
    queryKey: ["handover-bind-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-handover-bind-mark="desk">
      <CatalogHeading
        title="Wiązania przekazania"
        subtitle="N11 leftover 543 handover_bind_mark · HITL · nie FK UUID · nie T6 live"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <HandoverBindMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            bind_kind: "Wiązanie",
            source_ref: "source_ref",
          }}
          columns={BIND_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr wiązań…"
          tableKey={BUSINESS_LISTS.handoverBindMark.tableKey}
        />
      ) : null}
    </section>
  )
}
