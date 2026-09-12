import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadJitJisMarks,
  type JitJisMarkRow,
} from "@/lib/jit-jis-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { JitJisComposer } from "./mark-form"

const col = createColumnHelper<JitJisMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("flow_kind", { header: "Tryb flow" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function JitJisBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const flows = useQuery({
    enabled: ready,
    queryFn: loadJitJisMarks,
    queryKey: ["jit-jis-marks", orgId],
    retry: false,
  })

  return (
    <div className="grid gap-4" data-jj="board">
      <CatalogHeading
        title="JIT/JIS"
        subtitle="EXP3.1 · jit|jis|kanban · bez WMS live"
      />
      {!ready ? <TenantSessionNotice /> : <JitJisComposer organizationId={orgId} />}
      {flows.error ? <CatalogError error={flows.error} /> : null}
      {ready && flows.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            flow_kind: "Tryb flow",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={flows.data ?? []}
          globalFilterPlaceholder="Szukaj JIT/JIS…"
          tableKey={BUSINESS_LISTS.jitJisMark.tableKey}
        />
      ) : null}
    </div>
  )
}
