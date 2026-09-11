import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  listRoutingGuideMatches,
  type RoutingGuideMatchRow,
} from "@/lib/routing-guide-matches-api"
import { getTenantContext } from "@/lib/tenant"
import { MatchKindWriter } from "./match-form"

const cols = createColumnHelper<RoutingGuideMatchRow>()
const COLUMNS = [
  cols.accessor("mark_code", { header: "Kod" }),
  cols.accessor("match_kind", { header: "Tryb" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

export function MatchKindBoard() {
  const session = getTenantContext()
  const org = session.organizationId
  const online = Boolean(org && session.userId)
  const query = useQuery({
    enabled: online,
    queryFn: listRoutingGuideMatches,
    queryKey: ["routing-guide-matches", org],
    retry: false,
  })
  return (
    <div className="space-y-6" data-routing-guide-match="board">
      <CatalogHeading
        title="Dopasowanie przewodnika"
        subtitle="CT4 routing_guide_match · katalog HITL · nie silnik"
      />
      {!online ? <TenantSessionNotice /> : null}
      {online ? <MatchKindWriter organizationId={org} /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {online && !query.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            match_kind: "Tryb",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={query.data ?? []}
          globalFilterPlaceholder="Szukaj trybu…"
          tableKey={BUSINESS_LISTS.routingGuideMatch.tableKey}
        />
      ) : null}
    </div>
  )
}
