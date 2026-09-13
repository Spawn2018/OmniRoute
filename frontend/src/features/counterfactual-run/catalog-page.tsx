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
  loadCounterfactualRuns,
  loadWhatIfReplays,
  type CounterfactualRunRow,
  type WhatIfReplayRow,
} from "@/lib/counterfactual-runs-api"
import { getTenantContext } from "@/lib/tenant"
import { CounterfactualRunComposer } from "./ledger-form"

const helper = createColumnHelper<CounterfactualRunRow>()
const COLS = [
  helper.accessor("run_code", { header: "Kod" }),
  helper.accessor("plan_snapshot_id", { header: "Migawka" }),
  helper.accessor("baseline_label", { header: "Punkt" }),
  helper.accessor("levers_label", { header: "Dźwignie" }),
  helper.accessor("result_label", { header: "Wynik" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

const replayHelper = createColumnHelper<WhatIfReplayRow>()
const REPLAY_COLS = [
  replayHelper.accessor("run_code", { header: "Kod" }),
  replayHelper.accessor("snapshot_code", { header: "Migawka" }),
  replayHelper.accessor("shipment_id", { header: "Zlecenie" }),
  replayHelper.accessor("trip_id", { header: "Przejazd" }),
  replayHelper.accessor("resource_id", { header: "Zasób" }),
]

export function CounterfactualRunBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadCounterfactualRuns,
    queryKey: ["counterfactual-runs", organizationId],
    retry: false,
  })
  const replayQuery = useQuery({
    enabled: sessionReady,
    queryFn: loadWhatIfReplays,
    queryKey: ["what-if-replays", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const replays = replayQuery.data ?? []
  const showTable = sessionReady && query.error == null
  const showReplays = sessionReady && replayQuery.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-counterfactual-run="desk"
    >
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Przebieg what-if"
          subtitle="AI4.1 · przebieg wskazuje istniejącą migawkę · powtórka nie liczy"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL zapis nazwanego przebiegu — tylko dane.</li>
          <li>UUID migawki musi istnieć u tenanta. Bez kwoty.</li>
          <li>Powtórka to ten sam SELECT, nie silnik liczb. Kółka 500k = AI4.2.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {replayQuery.error ? <CatalogError error={replayQuery.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak przebiegów what-if.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              run_code: "Kod",
              plan_snapshot_id: "Migawka",
              baseline_label: "Punkt",
              levers_label: "Dźwignie",
              result_label: "Wynik",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj przebiegu…"
            tableKey={BUSINESS_LISTS.counterfactualRun.tableKey}
          />
        ) : null}
        {showReplays && replays.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak powtórek what-if.</p>
        ) : null}
        {showReplays ? (
          <DataTableShell
            columnLabels={{
              run_code: "Kod",
              snapshot_code: "Migawka",
              shipment_id: "Zlecenie",
              trip_id: "Przejazd",
              resource_id: "Zasób",
            }}
            columns={REPLAY_COLS}
            data={replays}
            globalFilterPlaceholder="Szukaj powtórki…"
            tableKey={`${BUSINESS_LISTS.counterfactualRun.tableKey}-replay`}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <CounterfactualRunComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
