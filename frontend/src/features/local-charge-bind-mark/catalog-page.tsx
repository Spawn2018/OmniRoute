import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchLocalChargeBindMarks,
  type LocalChargeBindMarkRow,
} from "@/lib/local-charge-bind-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LocalChargeBindMarkSave } from "./mark-form"

const bindCol = createColumnHelper<LocalChargeBindMarkRow>()

const BIND_COLUMNS = [
  bindCol.accessor("mark_code", { header: "Kod" }),
  bindCol.accessor("bind_kind", { header: "Wiązanie" }),
  bindCol.accessor("source_ref", { header: "source_ref" }),
]

export function LocalChargeBindMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchLocalChargeBindMarks,
    queryKey: ["local-charge-bind-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-local-charge-bind-mark="desk">
      <CatalogHeading
        title="Wiązanie dopłaty lokalnej"
        subtitle="P4c leftover bind local_charge_bind_mark · HITL · nie FK UUID · nie matching SQL · nie warning-jako-fakt"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <LocalChargeBindMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            bind_kind: "Wiązanie",
            source_ref: "source_ref",
          }}
          columns={BIND_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr wiązań…"
          tableKey={BUSINESS_LISTS.localChargeBindMark.tableKey}
        />
      ) : null}
    </section>
  )
}
