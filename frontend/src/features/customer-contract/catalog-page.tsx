import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  listCustomerContractHeaders,
  type CustomerContractHeader,
} from "@/lib/customer-contracts-api"
import { getTenantContext } from "@/lib/tenant"
import { CustomerContractSave } from "./header-form"

const helper = createColumnHelper<CustomerContractHeader>()

const HEADER_COLUMNS = [
  helper.accessor("contract_code", { header: "Kod" }),
  helper.accessor("shipper_label", { header: "Załadowca" }),
  helper.accessor("their_customer_label", { header: "Odbiorca" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
  helper.accessor("has_ciphertext", {
    header: "Opakowanie",
    cell: (info) => (info.getValue() ? "Tak" : "Nie"),
  }),
]

const HEADER_LABELS = {
  contract_code: "Kod",
  shipper_label: "Załadowca",
  their_customer_label: "Odbiorca",
  source_ref: "Pochodzenie",
  has_ciphertext: "Opakowanie",
}

function PactHeaderRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: Boolean(args.organizationId),
    queryFn: listCustomerContractHeaders,
    queryKey: ["pact-headers", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columns={HEADER_COLUMNS}
      data={listed.data ?? []}
      tableKey={BUSINESS_LISTS.customerContract.tableKey}
      columnLabels={HEADER_LABELS}
      globalFilterPlaceholder="Filtruj nagłówek umowy…"
    />
  )
}

export function CustomerContractDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-customer-contract="header-desk">
      <CatalogHeading
        title="Umowa klienta"
        subtitle="CI9 customer_contract · nagłówek + opakowanie present/absent · nie szyfr"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <CustomerContractSave organizationId={ctx.organizationId} />
          <PactHeaderRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
