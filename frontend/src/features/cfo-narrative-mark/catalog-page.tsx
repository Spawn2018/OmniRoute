import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchCfoNarrativeMarks,
  type CfoNarrativeMarkRow,
} from "@/lib/cfo-narrative-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CfoNarrativeMarkSave } from "./mark-form"

const helper = createColumnHelper<CfoNarrativeMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("narrative_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function CfoNarrativeMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCfoNarrativeMarks,
    queryKey: ["cfo-narrative-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-cfo-narrative-mark="board">
      <CatalogHeading
        title="Narracja CFO"
        subtitle="AI7.1 cfo_narrative_mark · HITL anomaly/story/summary · nie silnik narracji"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <CfoNarrativeMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            narrative_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj narracje CFO…"
          tableKey={BUSINESS_LISTS.cfoNarrativeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
