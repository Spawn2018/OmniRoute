import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchFieldConfidenceMarks,
  type FieldConfidenceMarkRow,
} from "@/lib/field-confidence-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FieldConfidenceMarkSave } from "./mark-form"

const helper = createColumnHelper<FieldConfidenceMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("band_kind", { header: "Pasmo" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function FieldConfidenceMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchFieldConfidenceMarks,
    queryKey: ["field-confidence-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-field-confidence-mark="board">
      <CatalogHeading
        title="PEWNOŚĆ PER POLE"
        subtitle="AI9.1 field_confidence_mark · HITL green/yellow/orange/hold · nie ui-04 · nie float"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <FieldConfidenceMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            band_kind: "Pasmo",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj pasma pewności…"
          tableKey={BUSINESS_LISTS.fieldConfidenceMark.tableKey}
        />
      ) : null}
    </section>
  )
}
