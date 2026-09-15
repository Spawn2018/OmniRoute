import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchIngestGateMarks,
  type IngestGateMarkRow,
} from "@/lib/ingest-gate-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { IngestGateMarkSave } from "./mark-form"

const helper = createColumnHelper<IngestGateMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("gate_kind", { header: "Brama" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function IngestGateMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchIngestGateMarks,
    queryKey: ["ingest-gate-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-ingest-gate-mark="board">
      <CatalogHeading
        title="Brama ingest"
        subtitle="AI5.0 ingest_gate_mark · HITL truth/owner/exception · nie live ingest"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <IngestGateMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            gate_kind: "Brama",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj bramy ingest…"
          tableKey={BUSINESS_LISTS.ingestGateMark.tableKey}
        />
      ) : null}
    </section>
  )
}
