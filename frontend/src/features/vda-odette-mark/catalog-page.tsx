import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadVdaOdetteMarks,
  type VdaOdetteMarkRow,
} from "@/lib/vda-odette-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { VdaOdetteComposer } from "./mark-form"

const col = createColumnHelper<VdaOdetteMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("edi_kind", { header: "Tryb EDI" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function VdaOdetteBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const rows = useQuery({
    enabled: ready,
    queryFn: loadVdaOdetteMarks,
    queryKey: ["vda-odette-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-vo="board">
      <CatalogHeading
        title="VDA/Odette"
        subtitle="EXP3.2 · vda|odette|label · bez live EDI"
      />
      {!ready ? <TenantSessionNotice /> : <VdaOdetteComposer organizationId={orgId} />}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {ready && rows.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            edi_kind: "Tryb EDI",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj VDA/Odette…"
          tableKey={BUSINESS_LISTS.vdaOdetteMark.tableKey}
        />
      ) : null}
    </section>
  )
}
