import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listKekMarks, type KekMarkRow } from "@/lib/tenant-contract-keks-api"
import { getTenantContext } from "@/lib/tenant"
import { TenantContractKekSave } from "./tenant-contract-kek-form"

const helper = createColumnHelper<KekMarkRow>()

const columns = [
  helper.accessor("kek_code", { header: "Kod" }),
  helper.accessor("wrap_kind", { header: "Owijka" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  kek_code: "Kod",
  wrap_kind: "Owijka",
  source_ref: "Pochodzenie",
}

function KekMarkRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listKekMarks,
    queryKey: ["kek-marks", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={COLUMN_LABELS}
      columns={columns}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj znacznik KEK…"
      tableKey={BUSINESS_LISTS.tenantContractKek.tableKey}
    />
  )
}

export function TenantContractKekDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-kek-mark="desk">
      <CatalogHeading
        title="Znacznik KEK"
        subtitle="CI9 tenant_contract_kek · wrap_kind jako dane · nie klucz · nie KMS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <TenantContractKekSave organizationId={ctx.organizationId} />
          <KekMarkRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
