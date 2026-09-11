import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  listScheduleExceptionMarks,
  type ScheduleExceptionMarkRow,
} from "@/lib/schedule-exception-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ScheduleExceptionMarkEditor } from "./mark-form"

const helper = createColumnHelper<ScheduleExceptionMarkRow>()
const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("exception_kind", { header: "Wyjątek" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function ScheduleExceptionMarkDesk() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const list = useQuery({
    enabled: ready,
    queryFn: listScheduleExceptionMarks,
    queryKey: ["schedule-exception-marks", orgId],
    retry: false,
  })
  return (
    <section className="flex flex-col gap-5" data-schedule-exception-mark="desk">
      <CatalogHeading
        title="Schedule exception"
        subtitle="EXP2.7 · HITL schedule_exception_mark · bez silnika schedule"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ScheduleExceptionMarkEditor organizationId={orgId} /> : null}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ready && !list.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            exception_kind: "Wyjątek",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={list.data ?? []}
          globalFilterPlaceholder="Filtruj wyjątki…"
          tableKey={BUSINESS_LISTS.scheduleExceptionMark.tableKey}
        />
      ) : null}
    </section>
  )
}
