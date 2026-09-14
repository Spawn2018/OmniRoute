import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchRiskRegisterMarks,
  type RiskRegisterMarkRow,
} from "@/lib/risk-register-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RiskRegisterMarkSave } from "./mark-form"

const col = createColumnHelper<RiskRegisterMarkRow>()

export function RiskRegisterMarkDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const sessionOk = Boolean(org && tenant.userId)
  const rows = useQuery({
    enabled: sessionOk,
    queryFn: fetchRiskRegisterMarks,
    queryKey: ["risk-register-marks", org],
    retry: false,
  })
  const tableCols = [
    col.accessor("mark_code", { header: "Oznaczenie" }),
    col.accessor("risk_kind", { header: "Rodzaj" }),
    col.accessor("source_ref", { header: "Pochodzenie" }),
  ]

  return (
    <main className="space-y-5 p-1" data-risk-register="desk">
      <CatalogHeading
        title="Rejestr ryzyka"
        subtitle="AI9.2 · open / mitigated / accepted · bez scoringu osoby, L3 silnika i Mob Expo"
      />
      {sessionOk ? null : <TenantSessionNotice />}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {sessionOk && !rows.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            risk_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={tableCols}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj rejestru…"
          tableKey={BUSINESS_LISTS.riskRegisterMark.tableKey}
        />
      ) : null}
      {sessionOk ? <RiskRegisterMarkSave organizationId={org} /> : null}
    </main>
  )
}
