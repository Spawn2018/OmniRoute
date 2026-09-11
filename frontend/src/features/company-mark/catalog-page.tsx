import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCompanyMarks, type CompanyMarkRow } from "@/lib/company-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CompanyMarkSave } from "./mark-form"

const helper = createColumnHelper<CompanyMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("seat_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CompanyMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCompanyMarks,
    queryKey: ["company-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-company-mark="board">
      <CatalogHeading
        title="Znacznik spółki"
        subtitle="G10 company_mark · katalog HITL · nie drugi tenant · nie ledger"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CompanyMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            seat_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika spółki…"
          tableKey={BUSINESS_LISTS.companyMark.tableKey}
        />
      ) : null}
    </section>
  )
}
