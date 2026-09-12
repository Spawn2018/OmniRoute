import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listPalletPoolMarks, type PalletPoolMarkRow } from "@/lib/pallet-pool-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PalletPoolEntry } from "./mark-form"

const helper = createColumnHelper<PalletPoolMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("pool_kind", { header: "Pula" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function PalletPoolDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const ready = Boolean(org && tenant.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: listPalletPoolMarks,
    queryKey: ["pallet-pool-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-pallet-pool="desk">
      <CatalogHeading
        title="Pula palet (HITL)"
        subtitle="EXP2.17 · chep|lpr|epal · bez giełdy / salda sztuk"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PalletPoolEntry organizationId={org} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {ready && board.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            pool_kind: "Pula",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj znaczniki puli…"
          tableKey={BUSINESS_LISTS.palletPoolMark.tableKey}
        />
      ) : null}
    </section>
  )
}
