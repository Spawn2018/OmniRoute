import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchSpendMarks, type SpendMarkRow } from "@/lib/spend-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SpendMarkSave } from "./mark-form"

const helper = createColumnHelper<SpendMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("leakage_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function SpendMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchSpendMarks,
    queryKey: ["spend-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-spend-mark="board">
      <CatalogHeading
        title="Znacznik wycieku"
        subtitle="CI2 spend_mark · katalog HITL · nie SQL FV vs charge · nie marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SpendMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            leakage_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika wycieku…"
          tableKey={BUSINESS_LISTS.spendMark.tableKey}
        />
      ) : null}
    </section>
  )
}
