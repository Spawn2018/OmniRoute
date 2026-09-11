import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listFerryArt9Marks, type FerryArt9MarkRow } from "@/lib/ferry-art9-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FerryArt9Writer } from "./mark-form"

const helper = createColumnHelper<FerryArt9MarkRow>()

const COLS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("ferry_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function FerryArt9Screen() {
  const session = getTenantContext()
  const org = session.organizationId
  const ready = Boolean(org && session.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: listFerryArt9Marks,
    queryKey: ["ferry-art9-marks", org],
    retry: false,
  })

  return (
    <section className="grid gap-6 lg:grid-cols-[minmax(0,20rem)_1fr]" data-ferry="screen">
      <div className="space-y-4 lg:col-span-2">
        <CatalogHeading
          title="Ferry art. 9"
          subtitle="EXP2.13 · katalog HITL · rest/watchdog/crossing · bez tacho"
        />
        {!ready ? <TenantSessionNotice /> : null}
      </div>
      {ready ? <FerryArt9Writer organizationId={org} /> : null}
      <div className="min-w-0 space-y-3">
        {board.error ? <CatalogError error={board.error} /> : null}
        {ready && board.error == null ? (
          <DataTableShell
            columnLabels={{
              mark_code: "Kod",
              ferry_kind: "Rodzaj",
              source_ref: "Źródło",
            }}
            columns={COLS}
            data={board.data ?? []}
            globalFilterPlaceholder="Szukaj ferry art. 9…"
            tableKey={BUSINESS_LISTS.ferryArt9Mark.tableKey}
          />
        ) : null}
      </div>
    </section>
  )
}
