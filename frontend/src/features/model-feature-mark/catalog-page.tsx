import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchModelFeatureMarks,
  type ModelFeatureMarkRow,
} from "@/lib/model-feature-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ModelFeatureMarkSave } from "./mark-form"

const helper = createColumnHelper<ModelFeatureMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("feature_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function ModelFeatureMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchModelFeatureMarks,
    queryKey: ["model-feature-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-model-feature-mark="board">
      <CatalogHeading
        title="Cecha modelu"
        subtitle="AI5.1 model_feature_mark · HITL numeric/categorical/derived · nie live train"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <ModelFeatureMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            feature_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj cechy modelu…"
          tableKey={BUSINESS_LISTS.modelFeatureMark.tableKey}
        />
      ) : null}
    </section>
  )
}
