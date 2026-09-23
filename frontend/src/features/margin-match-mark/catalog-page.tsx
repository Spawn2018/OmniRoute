import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchMarginMatchMarks,
  type MarginMatchMarkRow,
} from "@/lib/margin-match-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { MarginMatchMarkSave } from "./mark-form"

const bindCol = createColumnHelper<MarginMatchMarkRow>()

const BIND_COLUMNS = [
  bindCol.accessor("mark_code", { header: "Kod" }),
  bindCol.accessor("match_kind", { header: "Dopasowanie" }),
  bindCol.accessor("source_ref", { header: "source_ref" }),
]

export function MarginMatchMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchMarginMatchMarks,
    queryKey: ["margin-match-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col waive-4" data-margin-match-mark="desk">
      <CatalogHeading
        title="Dopasowanie podłogi"
        subtitle="N6 leftover matching margin_match_mark · HITL · nie matching SQL lane · nie auto charge"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <MarginMatchMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            match_kind: "Dopasowanie",
            source_ref: "source_ref",
          }}
          columns={BIND_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr wariancji…"
          tableKey={BUSINESS_LISTS.tripVarianceMark.tableKey}
        />
      ) : null}
    </section>
  )
}
