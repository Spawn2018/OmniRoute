import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchComplianceProgramMarks,
  type ComplianceProgramMarkRow,
} from "@/lib/compliance-program-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ComplianceProgramMarkSave } from "./mark-form"

const helper = createColumnHelper<ComplianceProgramMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("program_kind", { header: "Stancja" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function ComplianceProgramMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchComplianceProgramMarks,
    queryKey: ["compliance-program-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-compliance-program-mark="board">
      <CatalogHeading
        title="PROGRAM ZGODNOŚCI"
        subtitle="AI9.2 compliance_program_mark · HITL draft/review/signed/exempt · nie PDF · nie U-art50"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <ComplianceProgramMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            program_kind: "Stancja",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj stancje programu…"
          tableKey={BUSINESS_LISTS.complianceProgramMark.tableKey}
        />
      ) : null}
    </section>
  )
}
