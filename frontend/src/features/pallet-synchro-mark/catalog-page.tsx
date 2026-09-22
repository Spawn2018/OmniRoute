import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchPalletSynchroMarks,
  type PalletSynchroMarkRow,
} from "@/lib/pallet-synchro-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PalletSynchroMarkSave } from "./mark-form"

const synchroCol = createColumnHelper<PalletSynchroMarkRow>()

const SYNCHRO_COLUMNS = [
  synchroCol.accessor("mark_code", { header: "Kod" }),
  synchroCol.accessor("synchro_kind", { header: "Synchro" }),
  synchroCol.accessor("source_ref", { header: "source_ref" }),
]

export function PalletSynchroMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchPalletSynchroMarks,
    queryKey: ["pallet-synchro-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-pallet-synchro-mark="desk">
      <CatalogHeading
        title="Synchro palet"
        subtitle="D7c pallet_synchro_mark · HITL · nie auto-UPDATE · nie giełda"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <PalletSynchroMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            synchro_kind: "Synchro",
            source_ref: "source_ref",
          }}
          columns={SYNCHRO_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr synchro…"
          tableKey={BUSINESS_LISTS.palletSynchroMark.tableKey}
        />
      ) : null}
    </section>
  )
}
