import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCrmPipelineMarks, type CrmPipelineMarkRow } from "@/lib/crm-pipeline-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CrmPipelineMarkSave } from "./mark-form"

const helper = createColumnHelper<CrmPipelineMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("pipeline_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CrmPipelineMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCrmPipelineMarks,
    queryKey: ["crm-pipeline-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-crm-pipeline-mark="board">
      <CatalogHeading
        title="Etap CRM"
        subtitle="BR6.0 crm_pipeline_mark · katalog HITL · nie silnik lejka · nie FK okazji"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CrmPipelineMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            pipeline_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj etapów CRM…"
          tableKey={BUSINESS_LISTS.crmPipelineMark.tableKey}
        />
      ) : null}
    </section>
  )
}
