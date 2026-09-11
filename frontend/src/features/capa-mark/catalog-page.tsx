import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCapaMarks, type CapaMarkRow } from "@/lib/capa-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CapaMarkSave } from "./capa-mark-form"

const helper = createColumnHelper<CapaMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("mark_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CapaMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCapaMarks,
    queryKey: ["capa-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-capa-mark="board">
      <CatalogHeading
        title="Znacznik CAPA"
        subtitle="CT12 capa_mark · katalog HITL · nie workflow · nie scoring"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CapaMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{ mark_code: "Kod", mark_kind: "Rodzaj", source_ref: "Pochodzenie" }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj CAPA…"
          tableKey={BUSINESS_LISTS.capaMark.tableKey}
        />
      ) : null}
    </section>
  )
}
