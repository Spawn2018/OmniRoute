import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchRepairPlaybooks,
  type RepairPlaybookRow,
} from "@/lib/repair-playbooks-api"
import { getTenantContext } from "@/lib/tenant"
import { RepairPlaybookSave } from "./playbook-form"

const helper = createColumnHelper<RepairPlaybookRow>()

const COLUMNS = [
  helper.accessor("playbook_code", { header: "Kod" }),
  helper.accessor("stance_kind", { header: "Postawa" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function RepairPlaybookDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchRepairPlaybooks,
    queryKey: ["repair-playbooks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-repair-playbook="board">
      <CatalogHeading
        title="Playbook naprawy"
        subtitle="CI8 repair_playbook · katalog HITL · nie auto-send S11 · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RepairPlaybookSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            playbook_code: "Kod",
            stance_kind: "Postawa",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj playbooka naprawy…"
          tableKey={BUSINESS_LISTS.repairPlaybook.tableKey}
        />
      ) : null}
    </section>
  )
}
