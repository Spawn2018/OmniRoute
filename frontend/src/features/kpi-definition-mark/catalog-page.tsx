import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchKpiDefinitionMarks,
  type KpiDefinitionMarkRow,
} from "@/lib/kpi-definition-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { KpiDefinitionMarkSave } from "./mark-form"

const helper = createColumnHelper<KpiDefinitionMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("kpi_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function KpiDefinitionMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchKpiDefinitionMarks,
    queryKey: ["kpi-definition-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-kpi-definition-mark="board">
      <CatalogHeading
        title="Definicja KPI"
        subtitle="AI5.0 leftover kpi_definition_mark · HITL otd/otif/custom · nie wzór KPI"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <KpiDefinitionMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            kpi_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj definicje KPI…"
          tableKey={BUSINESS_LISTS.kpiDefinitionMark.tableKey}
        />
      ) : null}
    </section>
  )
}
