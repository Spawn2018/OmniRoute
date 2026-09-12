import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listECmrMarks, type ECmrMarkRow } from "@/lib/e-cmr-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ECmrEntry } from "./mark-form"

const helper = createColumnHelper<ECmrMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("cmr_kind", { header: "Dokument" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function ECmrDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const ready = Boolean(org && tenant.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: listECmrMarks,
    queryKey: ["e-cmr-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-e-cmr="desk">
      <CatalogHeading
        title="E-CMR / eFTI (HITL)"
        subtitle="EXP2.18 · ecmr|efti|paper · bez filera live"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ECmrEntry organizationId={org} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {ready && board.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            cmr_kind: "Dokument",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj znaczniki e-CMR…"
          tableKey={BUSINESS_LISTS.eCmrMark.tableKey}
        />
      ) : null}
    </section>
  )
}
