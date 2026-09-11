import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCmmsMarks, type CmmsMarkRow } from "@/lib/cmms-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CmmsMarkSave } from "./mark-form"

const helper = createColumnHelper<CmmsMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("work_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CmmsMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCmmsMarks,
    queryKey: ["cmms-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-cmms-mark="board">
      <CatalogHeading
        title="Znacznik CMMS"
        subtitle="G7 cmms_mark · katalog HITL · nie work_order · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CmmsMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            work_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika CMMS…"
          tableKey={BUSINESS_LISTS.cmmsMark.tableKey}
        />
      ) : null}
    </section>
  )
}
