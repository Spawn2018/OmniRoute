import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchInventoryCollateralMarks,
  type InventoryCollateralMarkRow,
} from "@/lib/inventory-collateral-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { InventoryCollateralMarkSave } from "./mark-form"

const helper = createColumnHelper<InventoryCollateralMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("collateral_kind", { header: "Zabezpieczenie" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function InventoryCollateralMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchInventoryCollateralMarks,
    queryKey: ["inventory-collateral-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-inventory-collateral-mark="board">
      <CatalogHeading
        title="Zabezpieczenie na towarze"
        subtitle="BR1.3 inventory_collateral_mark · HITL pledge/lien/hold · nie FK pozycji · nie live zastaw"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <InventoryCollateralMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            collateral_kind: "Zabezpieczenie",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj zabezpieczenia…"
          tableKey={BUSINESS_LISTS.inventoryCollateralMark.tableKey}
        />
      ) : null}
    </section>
  )
}
