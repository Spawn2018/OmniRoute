import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchStyleCascadeMarks,
  type StyleCascadeMarkRow,
} from "@/lib/style-cascade-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { StyleCascadeMarkSave } from "./mark-form"

const helper = createColumnHelper<StyleCascadeMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("cascade_kind", { header: "Poziom" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function StyleCascadeMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchStyleCascadeMarks,
    queryKey: ["style-cascade-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-style-cascade-mark="board">
      <CatalogHeading
        title="Kaskada stylu"
        subtitle="AI8.0 style_cascade_mark · HITL global→…→context · nie fidelity · nie scoring osoby"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <StyleCascadeMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            cascade_kind: "Poziom",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj poziomy kaskady stylu…"
          tableKey={BUSINESS_LISTS.styleCascadeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
