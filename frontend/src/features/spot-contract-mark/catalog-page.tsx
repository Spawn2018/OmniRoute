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
  loadSpotContractMarks,
  type SpotContractMarkRow,
} from "@/lib/spot-contract-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SpotContractMarkComposer } from "./mark-form"

const helper = createColumnHelper<SpotContractMarkRow>()
const COLS = [
  helper.accessor("deal_kind", { header: "Transakcja" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function SpotContractMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadSpotContractMarks,
    queryKey: ["spot-contract-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-scm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Spot / contract"
          subtitle="EXP1 · spot|contract|other · bez FK quotation"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik spot/contract — tylko katalog danych.</li>
          <li>Bez FK quotation i bez cargo_value.</li>
          <li>Odrębny od spot_or_contract na wycenie.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow spot/contract.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              deal_kind: "Transakcja",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika spot/contract…"
            tableKey={BUSINESS_LISTS.spotContractMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <SpotContractMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
