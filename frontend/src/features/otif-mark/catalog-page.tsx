import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listOtifMarks, type OtifMarkRow } from "@/lib/otif-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OtifMarkSave } from "./otif-mark-form"

const cols = createColumnHelper<OtifMarkRow>()

const MARK_COLUMNS = [
  cols.accessor("mark_code", { header: "Kod" }),
  cols.accessor("scope_kind", { header: "Zakres" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const MARK_LABELS = {
  mark_code: "Kod",
  scope_kind: "Zakres",
  source_ref: "Pochodzenie",
}

function OtifMarkTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listOtifMarks,
    queryKey: ["otif-marks", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={MARK_LABELS}
      columns={MARK_COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj znacznik OTIF…"
      tableKey={BUSINESS_LISTS.otifMark.tableKey}
    />
  )
}

export function OtifMarkDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-otif-mark="board">
      <CatalogHeading
        title="Znacznik OTIF"
        subtitle="CT3 otif_mark · katalog HITL · nie OTIF% · nie scoring"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <OtifMarkSave organizationId={ctx.organizationId} />
          <OtifMarkTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
