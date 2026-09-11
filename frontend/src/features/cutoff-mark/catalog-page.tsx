import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listCutoffMarks, type CutoffMarkRow } from "@/lib/cutoff-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CutoffMarkEditor } from "./mark-form"

const helper = createColumnHelper<CutoffMarkRow>()
const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("cutoff_kind", { header: "Cutoff" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function CutoffMarkDesk() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const list = useQuery({
    enabled: ready,
    queryFn: listCutoffMarks,
    queryKey: ["cutoff-marks", orgId],
    retry: false,
  })
  return (
    <section className="flex flex-col gap-5" data-cutoff-mark="desk">
      <CatalogHeading
        title="Cutoff"
        subtitle="EXP2.8 · HITL cutoff_mark · cutoffy rozdzielone · bez silnika"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CutoffMarkEditor organizationId={orgId} /> : null}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ready && !list.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            cutoff_kind: "Cutoff",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={list.data ?? []}
          globalFilterPlaceholder="Filtruj cutoff…"
          tableKey={BUSINESS_LISTS.cutoffMark.tableKey}
        />
      ) : null}
    </section>
  )
}
