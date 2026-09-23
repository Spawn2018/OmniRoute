import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchNetworkPrintGateMarks,
  type NetworkPrintGateMarkRow,
} from "@/lib/network-print-gate-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { NetworkPrintGateMarkSave } from "./mark-form"

const gateCol = createColumnHelper<NetworkPrintGateMarkRow>()

const GATE_COLUMNS = [
  gateCol.accessor("mark_code", { header: "Kod" }),
  gateCol.accessor("gate_kind", { header: "Gate" }),
  gateCol.accessor("source_ref", { header: "source_ref" }),
]

export function NetworkPrintGateMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchNetworkPrintGateMarks,
    queryKey: ["network-print-gate-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-network-print-gate-mark="desk">
      <CatalogHeading
        title="Brama wydruku sieci"
        subtitle="D9c leftover network_print_gate_mark · HITL · nie live 409 · nie PDF"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <NetworkPrintGateMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            gate_kind: "Gate",
            source_ref: "source_ref",
          }}
          columns={GATE_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr bramy…"
          tableKey={BUSINESS_LISTS.networkPrintGateMark.tableKey}
        />
      ) : null}
    </section>
  )
}
