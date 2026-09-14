import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchL3GateMarks, type L3GateMarkRow } from "@/lib/l3-gate-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { L3GateMarkSave } from "./mark-form"

const helper = createColumnHelper<L3GateMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("gate_kind", { header: "Brama" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function L3GateMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchL3GateMarks,
    queryKey: ["l3-gate-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-l3-gate-mark="board">
      <CatalogHeading
        title="Brama L3"
        subtitle="AI8.2 l3_gate_mark · HITL sot/owner/exception/rollback/blast · nie L3 write · nie autonomy_level"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <L3GateMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            gate_kind: "Brama",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj stancje bramy L3…"
          tableKey={BUSINESS_LISTS.l3GateMark.tableKey}
        />
      ) : null}
    </section>
  )
}
