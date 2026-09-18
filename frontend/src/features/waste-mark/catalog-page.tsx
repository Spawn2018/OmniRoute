import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchWasteMarks, type WasteMarkRow } from "@/lib/waste-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { WasteMarkSave } from "./mark-form"

const helper = createColumnHelper<WasteMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("waste_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function WasteMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchWasteMarks,
    queryKey: ["waste-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-waste-mark="board">
      <CatalogHeading
        title="Odpady BDO / KPO / WSR"
        subtitle="C6 waste_mark · katalog HITL · nie MOS live · nie shipment.is_waste"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <WasteMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            waste_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika odpadów…"
          tableKey={BUSINESS_LISTS.wasteMark.tableKey}
        />
      ) : null}
    </section>
  )
}
