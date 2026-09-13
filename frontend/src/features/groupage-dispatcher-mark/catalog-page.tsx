import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchGroupageDispatcherMarks,
  type GroupageDispatcherMarkRow,
} from "@/lib/groupage-dispatcher-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { GroupageDispatcherMarkSave } from "./mark-form"

const helper = createColumnHelper<GroupageDispatcherMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("dispatcher_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function GroupageDispatcherMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchGroupageDispatcherMarks,
    queryKey: ["groupage-dispatcher-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-groupage-dispatcher-mark="board">
      <CatalogHeading
        title="Dyspozytor drobnicy"
        subtitle="BR3.2 groupage_dispatcher_mark · katalog HITL · nie silnik hubów · nie live"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <GroupageDispatcherMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            dispatcher_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj stance dyspozytora…"
          tableKey={BUSINESS_LISTS.groupageDispatcherMark.tableKey}
        />
      ) : null}
    </section>
  )
}
