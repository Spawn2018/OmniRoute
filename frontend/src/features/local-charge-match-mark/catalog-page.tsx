import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchLocalChargeMatchMarks,
  type LocalChargeMatchMarkRow,
} from "@/lib/local-charge-match-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LocalChargeMatchMarkSave } from "./mark-form"

const bindCol = createColumnHelper<LocalChargeMatchMarkRow>()

const BIND_COLUMNS = [
  bindCol.accessor("mark_code", { header: "Kod" }),
  bindCol.accessor("match_kind", { header: "Dopasowanie" }),
  bindCol.accessor("source_ref", { header: "source_ref" }),
]

export function LocalChargeMatchMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchLocalChargeMatchMarks,
    queryKey: ["local-charge-match-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-local-charge-match-mark="desk">
      <CatalogHeading
        title="Dopasowanie dopłaty lokalnej"
        subtitle="P4c leftover matching local_charge_match_mark · HITL · nie matching SQL vs local_charge · nie warning-jako-fakt"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <LocalChargeMatchMarkSave organizationId={organizationId} /> : null}
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
