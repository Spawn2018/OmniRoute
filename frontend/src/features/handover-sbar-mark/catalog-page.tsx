import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchHandoverSbarMarks,
  type HandoverSbarMarkRow,
} from "@/lib/handover-sbar-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { HandoverSbarMarkSave } from "./mark-form"

const helper = createColumnHelper<HandoverSbarMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("sbar_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function HandoverSbarMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchHandoverSbarMarks,
    queryKey: ["handover-sbar-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-handover-sbar-mark="board">
      <CatalogHeading
        title="Przekazanie zmiany SBAR"
        subtitle="N11 handover_sbar_mark · HITL S/B/A/R · nie drugi czat"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <HandoverSbarMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            sbar_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj znaczniki SBAR…"
          tableKey={BUSINESS_LISTS.handoverSbarMark.tableKey}
        />
      ) : null}
    </section>
  )
}
