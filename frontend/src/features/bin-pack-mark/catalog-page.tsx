import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listBinPackMarks, type BinPackMarkRow } from "@/lib/bin-pack-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { BinPackEntry } from "./mark-form"

const helper = createColumnHelper<BinPackMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("pack_kind", { header: "Pack kind" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function BinPackDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const ready = Boolean(org && tenant.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: listBinPackMarks,
    queryKey: ["bin-pack-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-bin-pack="desk">
      <CatalogHeading
        title="Bin-pack (HITL)"
        subtitle="EXP2.16 · volume|weight|mixed · bez solvera OR / LLM-VRP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <BinPackEntry organizationId={org} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {ready && board.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            pack_kind: "Pack kind",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj znaczniki bin-pack…"
          tableKey={BUSINESS_LISTS.binPackMark.tableKey}
        />
      ) : null}
    </section>
  )
}
