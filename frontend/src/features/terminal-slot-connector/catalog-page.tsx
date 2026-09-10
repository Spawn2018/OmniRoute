import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadSlotConnectors, type SlotConnectorRecord } from "@/lib/terminal-slot-connectors-api"
import { getTenantContext } from "@/lib/tenant"
import { TerminalSlotSave } from "./terminal-slot-connector-form"

const helper = createColumnHelper<SlotConnectorRecord>()

const columns = [
  helper.accessor("connector_code", { header: "Kod" }),
  helper.accessor("terminal_code", { header: "Terminal" }),
  helper.accessor("mode", { header: "Tryb" }),
  helper.accessor("opens_local", { header: "Otwarcie" }),
  helper.accessor("closes_local", { header: "Zamknięcie" }),
  helper.accessor("cutoff_local", { header: "Odcięcie" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  connector_code: "Kod",
  terminal_code: "Terminal",
  mode: "Tryb",
  opens_local: "Otwarcie",
  closes_local: "Zamknięcie",
  cutoff_local: "Odcięcie",
  source_ref: "Pochodzenie",
}

function SlotConnectorRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: loadSlotConnectors,
    queryKey: ["terminal-slot-connectors", args.organizationId],
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
        globalFilterPlaceholder="Szukaj konektora slotu…"
        tableKey={BUSINESS_LISTS.terminalSlotConnector.tableKey}
      />
    </div>
  )
}

export function TerminalSlotConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-terminal-slot-connector="desk">
      <CatalogHeading
        title="Konektor slotu"
        subtitle="T8 terminal_slot_connector · mode + godziny N4 · nie live API · nie confirmed"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <TerminalSlotSave organizationId={ctx.organizationId} />
          <SlotConnectorRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
