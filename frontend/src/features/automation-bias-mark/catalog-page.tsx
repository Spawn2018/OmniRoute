import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchAutomationBiasMarks,
  type AutomationBiasMarkRow,
} from "@/lib/automation-bias-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { AutomationBiasMarkSave } from "./mark-form"

const helper = createColumnHelper<AutomationBiasMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("bias_kind", { header: "Mitygacja" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function AutomationBiasMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchAutomationBiasMarks,
    queryKey: ["automation-bias-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-automation-bias-mark="board">
      <CatalogHeading
        title="Automation bias"
        subtitle="AI9.1 automation_bias_mark · HITL confirm/delay/review · nie ui-04 · nie auto-accept"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <AutomationBiasMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            bias_kind: "Mitygacja",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj stancje bias…"
          tableKey={BUSINESS_LISTS.automationBiasMark.tableKey}
        />
      ) : null}
    </section>
  )
}
