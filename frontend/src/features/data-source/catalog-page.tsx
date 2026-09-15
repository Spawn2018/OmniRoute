import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchDataSources,
  type DataSourceRow,
} from "@/lib/data-sources-api"
import { getTenantContext } from "@/lib/tenant"
import { DataSourceSave } from "./mark-form"

const helper = createColumnHelper<DataSourceRow>()

const COLUMNS = [
  helper.accessor("source_code", { header: "Oznaczenie" }),
  helper.accessor("license_label", { header: "Licencja" }),
  helper.accessor("rights_scope", { header: "Zakres" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function DataSourceDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchDataSources,
    queryKey: ["data-sources", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-data-source="board">
      <CatalogHeading
        title="Zrodla danych"
        subtitle="AI5.0 data_source · HITL licencja + zakres praw · nie live ingest"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <DataSourceSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            source_code: "Oznaczenie",
            license_label: "Licencja",
            rights_scope: "Zakres",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj zrodla…"
          tableKey={BUSINESS_LISTS.dataSource.tableKey}
        />
      ) : null}
    </section>
  )
}
