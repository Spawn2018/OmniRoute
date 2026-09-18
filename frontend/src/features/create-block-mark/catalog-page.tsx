import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchCreateBlockMarks,
  type CreateBlockMarkRow,
} from "@/lib/create-block-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CreateBlockMarkSave } from "./mark-form"

const helper = createColumnHelper<CreateBlockMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("block_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CreateBlockMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCreateBlockMarks,
    queryKey: ["create-block-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-create-block-mark="board">
      <CatalogHeading
        title="Brama create zlecenia"
        subtitle="C8 create_block_mark · katalog HITL · nie live 409 na shipment · nie blocks_create egzekucja"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CreateBlockMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            block_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj bramy create…"
          tableKey={BUSINESS_LISTS.createBlockMark.tableKey}
        />
      ) : null}
    </section>
  )
}
