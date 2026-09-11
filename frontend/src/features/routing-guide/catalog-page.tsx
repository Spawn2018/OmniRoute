import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listRoutingGuides, type RoutingGuideRow } from "@/lib/routing-guides-api"
import { getTenantContext } from "@/lib/tenant"
import { RoutingGuideSave } from "./routing-guide-form"

const cols = createColumnHelper<RoutingGuideRow>()

const GUIDE_COLUMNS = [
  cols.accessor("guide_code", { header: "Kod" }),
  cols.accessor("lane_label", { header: "Korytarz" }),
  cols.accessor("mode_label", { header: "Tryb" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const GUIDE_LABELS = {
  guide_code: "Kod",
  lane_label: "Korytarz",
  mode_label: "Tryb",
  source_ref: "Pochodzenie",
}

function RoutingGuideTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listRoutingGuides,
    queryKey: ["routing-guides", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={GUIDE_LABELS}
      columns={GUIDE_COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj przewodnik routingu…"
      tableKey={BUSINESS_LISTS.routingGuide.tableKey}
    />
  )
}

export function RoutingGuideDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-routing-guide="board">
      <CatalogHeading
        title="Przewodnik routingu"
        subtitle="CT4 routing_guide · katalog HITL · nie 409 · nie mapa"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <RoutingGuideSave organizationId={ctx.organizationId} />
          <RoutingGuideTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
