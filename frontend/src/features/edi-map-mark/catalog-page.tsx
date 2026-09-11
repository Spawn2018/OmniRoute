import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchEdiMapMarks, type EdiMapMarkRow } from "@/lib/edi-map-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { EdiMapMarkSave } from "./mark-form"

const helper = createColumnHelper<EdiMapMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("map_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function EdiMapMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchEdiMapMarks,
    queryKey: ["edi-map-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-edi-map-mark="board">
      <CatalogHeading
        title="Mapa EDI"
        subtitle="G13 edi_map_mark · katalog HITL · nie silent write · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <EdiMapMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            map_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj mapy EDI…"
          tableKey={BUSINESS_LISTS.ediMapMark.tableKey}
        />
      ) : null}
    </section>
  )
}
