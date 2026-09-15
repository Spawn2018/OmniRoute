import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchSalesBindMarks, type SalesBindMarkRow } from "@/lib/sales-bind-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SalesBindMarkSave } from "./mark-form"

const salesBindCol = createColumnHelper<SalesBindMarkRow>()

const SALES_BIND_COLUMNS = [
  salesBindCol.accessor("mark_code", { header: "Kod bind" }),
  salesBindCol.accessor("bind_kind", { header: "Rodzaj wiązania" }),
  salesBindCol.accessor("source_ref", { header: "source_ref" }),
]

export function SalesBindMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchSalesBindMarks,
    queryKey: ["sales-bind-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-sales-bind-mark="desk">
      <CatalogHeading
        title="Bind sprzedaży"
        subtitle="BR6.1 sales_bind_mark · HITL · nie HubSpot · nie FK UUID"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <SalesBindMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod bind",
            bind_kind: "Rodzaj wiązania",
            source_ref: "source_ref",
          }}
          columns={SALES_BIND_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr bind…"
          tableKey={BUSINESS_LISTS.salesBindMark.tableKey}
        />
      ) : null}
    </section>
  )
}
