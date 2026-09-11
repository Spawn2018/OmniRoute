import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchOogMarks, type OogMarkRow } from "@/lib/oog-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OogMarkSave } from "./mark-form"

const helper = createColumnHelper<OogMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("escort_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function OogMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchOogMarks,
    queryKey: ["oog-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-oog-mark="board">
      <CatalogHeading
        title="Znacznik OOG"
        subtitle="G5 oog_mark · katalog HITL · nie wymiary · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <OogMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            escort_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika OOG…"
          tableKey={BUSINESS_LISTS.oogMark.tableKey}
        />
      ) : null}
    </section>
  )
}
