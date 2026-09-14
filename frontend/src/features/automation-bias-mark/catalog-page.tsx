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

const col = createColumnHelper<AutomationBiasMarkRow>()

export function AutomationBiasMarkDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const sessionOk = Boolean(org && tenant.userId)
  const rows = useQuery({
    enabled: sessionOk,
    queryFn: fetchAutomationBiasMarks,
    queryKey: ["automation-bias-marks", org],
    retry: false,
  })
  const tableCols = [
    col.accessor("mark_code", { header: "Oznaczenie" }),
    col.accessor("bias_kind", { header: "Rodzaj" }),
    col.accessor("source_ref", { header: "Pochodzenie" }),
  ]

  return (
    <main className="space-y-5 p-1" data-automation-bias="desk">
      <CatalogHeading
        title="Automation bias"
        subtitle="AI9.1 · confirm / delay / review · bez przebudowy ui-04, scoringu i auto-accept"
      />
      {sessionOk ? null : <TenantSessionNotice />}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {sessionOk && !rows.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            bias_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={tableCols}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj stancji…"
          tableKey={BUSINESS_LISTS.automationBiasMark.tableKey}
        />
      ) : null}
      {sessionOk ? <AutomationBiasMarkSave organizationId={org} /> : null}
    </main>
  )
}
