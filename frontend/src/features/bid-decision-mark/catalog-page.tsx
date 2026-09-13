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
  loadBidDecisionMarks,
  type BidDecisionMarkRow,
} from "@/lib/bid-decision-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { BidDecisionMarkComposer } from "./mark-form"

const helper = createColumnHelper<BidDecisionMarkRow>()
const COLS = [
  helper.accessor("decision_kind", { header: "Decyzja" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function BidDecisionMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadBidDecisionMarks,
    queryKey: ["bid-decision-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-bdm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Bid decision"
          subtitle="EXP1 · go|no_go|hold|other · bez kolumny quotation"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik bid decision — tylko katalog danych.</li>
          <li>Bez kolumny na wycenie i bez auto-award.</li>
          <li>Odrębny od spot_contract_mark.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow bid decision.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              decision_kind: "Decyzja",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika bid decision…"
            tableKey={BUSINESS_LISTS.bidDecisionMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <BidDecisionMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
