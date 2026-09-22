import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchNetworkPrintRequirements,
  type NetworkPrintRequirementRow,
} from "@/lib/network-print-requirements-api"
import { getTenantContext } from "@/lib/tenant"
import { NetworkPrintRequirementSave } from "./requirement-form"

const helper = createColumnHelper<NetworkPrintRequirementRow>()

const COLUMNS = [
  helper.accessor("requirement_code", { header: "Kod" }),
  helper.accessor("network_label", { header: "Etykieta sieci" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function NetworkPrintRequirementDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchNetworkPrintRequirements,
    queryKey: ["network-print-requirements", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-network-print-requirement="board">
      <CatalogHeading
        title="Wymóg wydruku sieci"
        subtitle="D9c network_print_requirement · katalog HITL · nie 409 · nie PDF"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <NetworkPrintRequirementSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            requirement_code: "Kod",
            network_label: "Etykieta sieci",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj wymogu wydruku…"
          tableKey={BUSINESS_LISTS.networkPrintRequirement.tableKey}
        />
      ) : null}
    </section>
  )
}
