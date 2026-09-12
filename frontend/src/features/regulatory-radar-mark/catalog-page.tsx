import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadRegulatoryRadarMarks,
  type RegulatoryRadarMarkRow,
} from "@/lib/regulatory-radar-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RegulatoryRadarComposer } from "./mark-form"

const col = createColumnHelper<RegulatoryRadarMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("radar_kind", { header: "Tryb radara" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function RegulatoryRadarBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const radar = useQuery({
    enabled: ready,
    queryFn: loadRegulatoryRadarMarks,
    queryKey: ["regulatory-radar-marks", orgId],
    retry: false,
  })

  return (
    <article className="flex flex-col gap-5" data-rr="board">
      <CatalogHeading
        title="Regulatory radar"
        subtitle="EXP2.25 · notice|deadline|watch · bez scrape urzedow"
      />
      {!ready ? <TenantSessionNotice /> : <RegulatoryRadarComposer organizationId={orgId} />}
      {radar.error ? <CatalogError error={radar.error} /> : null}
      {ready && radar.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            radar_kind: "Tryb radara",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={radar.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika radara…"
          tableKey={BUSINESS_LISTS.regulatoryRadarMark.tableKey}
        />
      ) : null}
    </article>
  )
}
