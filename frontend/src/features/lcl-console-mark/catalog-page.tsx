import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchLclConsoleMarks, type LclConsoleMarkRow } from "@/lib/lcl-console-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LclConsoleMarkSave } from "./mark-form"

const helper = createColumnHelper<LclConsoleMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("console_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function LclConsoleMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchLclConsoleMarks,
    queryKey: ["lcl-console-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-lcl-console-mark="board">
      <CatalogHeading
        title="Konsola LCL"
        subtitle="BR4.2 lcl_console_mark · katalog HITL · nie live CFS · nie CBM"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LclConsoleMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            console_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj stance konsoli LCL…"
          tableKey={BUSINESS_LISTS.lclConsoleMark.tableKey}
        />
      ) : null}
    </section>
  )
}
