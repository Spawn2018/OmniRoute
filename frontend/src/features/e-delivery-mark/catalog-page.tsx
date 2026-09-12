import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listEDeliveryMarks, type EDeliveryMarkRow } from "@/lib/e-delivery-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { EDeliveryEntry } from "./mark-form"

const cols = createColumnHelper<EDeliveryMarkRow>()

const TABLE_COLS = [
  cols.accessor("mark_code", { header: "Kod kanału" }),
  cols.accessor("delivery_kind", { header: "Kanał" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

export function EDeliveryDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const sessionOk = Boolean(orgId && ctx.userId)
  const catalog = useQuery({
    enabled: sessionOk,
    queryFn: listEDeliveryMarks,
    queryKey: ["e-delivery-marks", orgId],
    retry: false,
  })

  return (
    <main className="space-y-8" data-edor="catalog">
      <CatalogHeading
        title="Katalog e-Doręczeń"
        subtitle="EXP2.19 · edor / registered / receipt · bez PUDO"
      />
      {sessionOk ? null : <TenantSessionNotice />}
      {sessionOk ? <EDeliveryEntry organizationId={orgId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionOk && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod kanału",
            delivery_kind: "Kanał",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Szukaj w e-Doręczeniach…"
          tableKey={BUSINESS_LISTS.eDeliveryMark.tableKey}
        />
      ) : null}
    </main>
  )
}
