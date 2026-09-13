import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchPositionEvents, type PositionEventRow } from "@/lib/position-events-api"
import { getTenantContext } from "@/lib/tenant"
import { PositionEventSave } from "./mark-form"

const helper = createColumnHelper<PositionEventRow>()

const COLUMNS = [
  helper.accessor("event_code", { header: "Kod" }),
  helper.accessor("source_kind", { header: "Źródło" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function PositionEventDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchPositionEvents,
    queryKey: ["position-events", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-position-event="board">
      <CatalogHeading
        title="Zdarzenie pozycji"
        subtitle="BR2.0 position_event · katalog HITL · nie live GPS · nie tracking_event"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PositionEventSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            event_code: "Kod",
            source_kind: "Źródło",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj zdarzenia pozycji…"
          tableKey={BUSINESS_LISTS.positionEvent.tableKey}
        />
      ) : null}
    </section>
  )
}
