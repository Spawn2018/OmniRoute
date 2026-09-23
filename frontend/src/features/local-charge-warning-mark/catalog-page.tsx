import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchLocalChargeWarningMarks,
  type LocalChargeWarningMarkRow,
} from "@/lib/local-charge-warning-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LocalChargeWarningMarkSave } from "./mark-form"

const warnCol = createColumnHelper<LocalChargeWarningMarkRow>()

const WARNING_COLUMNS = [
  warnCol.accessor("mark_code", { header: "Kod" }),
  warnCol.accessor("warning_kind", { header: "Ostrzeżenie" }),
  warnCol.accessor("source_ref", { header: "source_ref" }),
]

export function LocalChargeWarningMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchLocalChargeWarningMarks,
    queryKey: ["local-charge-warning-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-local-charge-warning-mark="desk">
      <CatalogHeading
        title="Ostrzeżenia dopłaty lokalnej"
        subtitle="P4c leftover local_charge_warning_mark · HITL · nie warning-jako-fakt · nie matching"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <LocalChargeWarningMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            warning_kind: "Ostrzeżenie",
            source_ref: "source_ref",
          }}
          columns={WARNING_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr ostrzeżeń…"
          tableKey={BUSINESS_LISTS.localChargeWarningMark.tableKey}
        />
      ) : null}
    </section>
  )
}
