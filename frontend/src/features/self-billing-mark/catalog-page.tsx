import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchSelfBillingMarks,
  type SelfBillingMarkRow,
} from "@/lib/self-billing-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SelfBillingMarkSave } from "./mark-form"

const helper = createColumnHelper<SelfBillingMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("billing_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function SelfBillingMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchSelfBillingMarks,
    queryKey: ["self-billing-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-self-billing-mark="board">
      <CatalogHeading
        title="Self-billing podwykonawcy"
        subtitle="N14 self_billing_mark · katalog HITL · nie live · nie JPK"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SelfBillingMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            billing_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj self-billing…"
          tableKey={BUSINESS_LISTS.selfBillingMark.tableKey}
        />
      ) : null}
    </section>
  )
}
