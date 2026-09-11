import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchMakeOrBuyMarks, type MakeOrBuyMarkRow } from "@/lib/make-or-buy-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { MakeOrBuyMarkSave } from "./mark-form"

const helper = createColumnHelper<MakeOrBuyMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("buy_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function MakeOrBuyMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchMakeOrBuyMarks,
    queryKey: ["make-or-buy-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-make-or-buy-mark="board">
      <CatalogHeading
        title="Make-or-buy"
        subtitle="EXP2.2 make_or_buy_mark · katalog HITL · nie silnik kosztu · nie silnik kosztu"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <MakeOrBuyMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            buy_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj make-or-buy…"
          tableKey={BUSINESS_LISTS.makeOrBuyMark.tableKey}
        />
      ) : null}
    </section>
  )
}
