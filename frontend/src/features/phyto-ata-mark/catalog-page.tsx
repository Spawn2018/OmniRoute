import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadPhytoAtaMarks,
  type PhytoAtaMarkRow,
} from "@/lib/phyto-ata-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PhytoAtaComposer } from "./mark-form"

const helper = createColumnHelper<PhytoAtaMarkRow>()
const PHYTO_COLS = [
  helper.accessor("mark_code", { header: "Kod pozwolenia" }),
  helper.accessor("permit_kind", { header: "Rodzaj pozwolenia" }),
  helper.accessor("source_ref", { header: "Zrodlo HITL" }),
]

export function PhytoAtaBoard() {
  const ctx = getTenantContext()
  const organizationId = ctx.organizationId
  const hasSession = Boolean(organizationId && ctx.userId)
  const list = useQuery({
    enabled: hasSession,
    queryFn: loadPhytoAtaMarks,
    queryKey: ["phyto-ata-marks", organizationId],
    retry: false,
  })

  return (
    <div className="space-y-6 border-l-4 border-emerald-700/40 pl-4" data-phyto="desk">
      <CatalogHeading
        title="Pozwolenia phyto i ATA"
        subtitle="EXP3.8 · HITL phyto|ata|plant|other · bez live i scrape"
      />
      {hasSession ? (
        <PhytoAtaComposer organizationId={organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
      {list.error ? <CatalogError error={list.error} /> : null}
      {hasSession && list.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod pozwolenia",
            permit_kind: "Rodzaj pozwolenia",
            source_ref: "Zrodlo HITL",
          }}
          columns={PHYTO_COLS}
          data={list.data ?? []}
          globalFilterPlaceholder="Szukaj pozwolen phyto/ATA…"
          tableKey={BUSINESS_LISTS.phytoAtaMark.tableKey}
        />
      ) : null}
    </div>
  )
}
