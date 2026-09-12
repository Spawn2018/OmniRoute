import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadSidImportMarks, type SidImportMarkRow } from "@/lib/sid-import-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SidImportComposer } from "./mark-form"

const col = createColumnHelper<SidImportMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("sid_kind", { header: "Tryb" }),
  col.accessor("source_ref", { header: "Źródło" }),
]

export function SidImportBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const list = useQuery({
    enabled: ready,
    queryFn: loadSidImportMarks,
    queryKey: ["sid-import-marks", orgId],
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-sid="board">
      <CatalogHeading
        title="Import SID"
        subtitle="EXP2.21 · sid|batch|manual · bez SID HTTP"
      />
      {!ready ? <TenantSessionNotice /> : <SidImportComposer organizationId={orgId} />}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ready && list.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            sid_kind: "Tryb",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={list.data ?? []}
          globalFilterPlaceholder="Szukaj SID…"
          tableKey={BUSINESS_LISTS.sidImportMark.tableKey}
        />
      ) : null}
    </div>
  )
}
