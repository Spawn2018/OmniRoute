import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadIntegrationHubMarks,
  type IntegrationHubMarkRow,
} from "@/lib/integration-hub-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { HubProtocolComposer } from "./mark-form"

const col = createColumnHelper<IntegrationHubMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod protokołu" }),
  col.accessor("hub_kind", { header: "Protokół" }),
  col.accessor("source_ref", { header: "Źródło HITL" }),
]

export function HubProtocolBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const catalog = useQuery({
    enabled: ready,
    queryFn: loadIntegrationHubMarks,
    queryKey: ["integration-hub-marks", orgId],
    retry: false,
  })

  return (
    <section className="space-y-5" data-hub="protocol-board">
      <CatalogHeading
        title="Integration Hub"
        subtitle="EXP2.22 · rest|soap|edi|sftp · bez live HTTP"
      />
      {!ready ? <TenantSessionNotice /> : <HubProtocolComposer organizationId={orgId} />}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {ready && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod protokołu",
            hub_kind: "Protokół",
            source_ref: "Źródło HITL",
          }}
          columns={COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtruj protokół hubu…"
          tableKey={BUSINESS_LISTS.integrationHubMark.tableKey}
        />
      ) : null}
    </section>
  )
}
