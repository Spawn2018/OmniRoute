import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchBillingMarks, type BillingMarkRow } from "@/lib/billing-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { BillingMarkSave } from "./mark-form"

const helper = createColumnHelper<BillingMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("billing_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function BillingMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchBillingMarks,
    queryKey: ["billing-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-billing-mark="board">
      <CatalogHeading
        title="Billing SaaS Omni"
        subtitle="G16 billing_mark · katalog HITL · nie live Stripe · nie limity SQL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <BillingMarkSave organizationId={orgId} /> : null}
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
          globalFilterPlaceholder="Szukaj billingu…"
          tableKey={BUSINESS_LISTS.billingMark.tableKey}
        />
      ) : null}
    </section>
  )
}
