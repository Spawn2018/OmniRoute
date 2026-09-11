import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchYardMarks, type YardMarkRow } from "@/lib/yard-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { YardMarkSave } from "./mark-form"

const helper = createColumnHelper<YardMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("yard_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function YardMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchYardMarks,
    queryKey: ["yard-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-yard-mark="board">
      <CatalogHeading
        title="Yard / waga / EIR"
        subtitle="G15 yard_mark · katalog HITL · nie live yard · nie kg"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <YardMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            yard_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj yard…"
          tableKey={BUSINESS_LISTS.yardMark.tableKey}
        />
      ) : null}
    </section>
  )
}
