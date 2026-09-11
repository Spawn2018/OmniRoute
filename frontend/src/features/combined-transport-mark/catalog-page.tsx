import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  listCombinedTransportMarks,
  type CombinedTransportMarkRow,
} from "@/lib/combined-transport-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CombinedTransportEditor } from "./mark-form"

const cols = createColumnHelper<CombinedTransportMarkRow>()

const COLUMNS = [
  cols.accessor("mark_code", { header: "Kod" }),
  cols.accessor("regime_kind", { header: "Reżim" }),
  cols.accessor("source_ref", { header: "Źródło" }),
]

export function CombinedTransportDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const ok = Boolean(org && tenant.userId)
  const query = useQuery({
    enabled: ok,
    queryFn: listCombinedTransportMarks,
    queryKey: ["combined-transport-marks", org],
    retry: false,
  })

  return (
    <main className="flex flex-col gap-6" data-ct="desk">
      <CatalogHeading
        title="Combined transport"
        subtitle="EXP2.12 · katalog HITL · combined/mobility/piggyback · bez silnika"
      />
      {!ok ? <TenantSessionNotice /> : null}
      {ok ? <CombinedTransportEditor organizationId={org} /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {ok && query.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            regime_kind: "Reżim",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={query.data ?? []}
          globalFilterPlaceholder="Filtruj reżimy…"
          tableKey={BUSINESS_LISTS.combinedTransportMark.tableKey}
        />
      ) : null}
    </main>
  )
}
