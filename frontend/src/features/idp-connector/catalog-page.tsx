import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listIdpConnectors, type IdpConnectorRow } from "@/lib/idp-connectors-api"
import { getTenantContext } from "@/lib/tenant"
import { IdpConnectorSave } from "./idp-connector-form"

const helper = createColumnHelper<IdpConnectorRow>()

const columns = [
  helper.accessor("connector_code", { header: "Kod" }),
  helper.accessor("provider_code", { header: "Dostawca" }),
  helper.accessor("public_domain", { header: "Domena" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  connector_code: "Kod",
  provider_code: "Dostawca",
  public_domain: "Domena",
  source_ref: "Pochodzenie",
}

function Auth0FixtureRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listIdpConnectors,
    queryKey: ["idp-connectors", args.organizationId],
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <div className="min-w-0 flex-1">
      {listed.error ? <CatalogError error={listed.error} /> : null}
      <DataTableShell
        columnLabels={COLUMN_LABELS}
        columns={columns}
        data={rows}
        globalFilterPlaceholder="Szukaj konektora Auth0…"
        tableKey={BUSINESS_LISTS.idpConnector.tableKey}
      />
    </div>
  )
}

export function IdpConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-idp-connector="board">
      <CatalogHeading
        title="Konektor Auth0"
        subtitle="S53 idp_connector · token auth0 jako dane · nie login · nie live HTTP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <IdpConnectorSave organizationId={ctx.organizationId} />
          <Auth0FixtureRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
