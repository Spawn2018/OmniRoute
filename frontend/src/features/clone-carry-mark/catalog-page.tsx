import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchCloneCarryMarks,
  type CloneCarryMarkRow,
} from "@/lib/clone-carry-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CloneCarryMarkSave } from "./mark-form"

const carryCol = createColumnHelper<CloneCarryMarkRow>()

const CARRY_COLUMNS = [
  carryCol.accessor("mark_code", { header: "Kod" }),
  carryCol.accessor("carry_kind", { header: "Carry" }),
  carryCol.accessor("source_ref", { header: "source_ref" }),
]

export function CloneCarryMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchCloneCarryMarks,
    queryKey: ["clone-carry-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-clone-carry-mark="desk">
      <CatalogHeading
        title="Carry przy klonie"
        subtitle="leftover 528 clone_carry_mark · HITL · nie auto-copy · nie similar SQL"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <CloneCarryMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            carry_kind: "Carry",
            source_ref: "source_ref",
          }}
          columns={CARRY_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr carry…"
          tableKey={BUSINESS_LISTS.cloneCarryMark.tableKey}
        />
      ) : null}
    </section>
  )
}
