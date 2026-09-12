import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadIsoNis2Marks,
  type IsoNis2MarkRow,
} from "@/lib/iso-nis2-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { IsoNis2Composer } from "./mark-form"

const col = createColumnHelper<IsoNis2MarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("ops_kind", { header: "Tryb ops" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function IsoNis2Board() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const marks = useQuery({
    enabled: ready,
    queryFn: loadIsoNis2Marks,
    queryKey: ["iso-nis2-marks", orgId],
    retry: false,
  })

  return (
    <div className="space-y-4" data-iso="board">
      <CatalogHeading
        title="ISO/NIS2 ops"
        subtitle="EXP2.26 · iso|nis2|policy · bez audytu live"
      />
      {!ready ? <TenantSessionNotice /> : <IsoNis2Composer organizationId={orgId} />}
      {marks.error ? <CatalogError error={marks.error} /> : null}
      {ready && marks.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            ops_kind: "Tryb ops",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={marks.data ?? []}
          globalFilterPlaceholder="Szukaj ISO/NIS2…"
          tableKey={BUSINESS_LISTS.isoNis2Mark.tableKey}
        />
      ) : null}
    </div>
  )
}
