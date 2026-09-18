import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchBlocksCreateEnforcementMarks,
  type BlocksCreateEnforcementMarkRow,
} from "@/lib/blocks-create-enforcement-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { BlocksCreateEnforcementMarkSave } from "./mark-form"

const helper = createColumnHelper<BlocksCreateEnforcementMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("enforcement_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function BlocksCreateEnforcementMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchBlocksCreateEnforcementMarks,
    queryKey: ["blocks-create-enforcement-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-blocks-create-enforcement-mark="board">
      <CatalogHeading
        title="Egzekucja bramy create"
        subtitle="C8 blocks_create_enforcement_mark · katalog HITL · nie live 409 na shipment · nie wiring create_block_mark"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <BlocksCreateEnforcementMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            enforcement_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj trybu egzekucji…"
          tableKey={BUSINESS_LISTS.blocksCreateEnforcementMark.tableKey}
        />
      ) : null}
    </section>
  )
}
