import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { listAsns, type AsnRow } from "@/lib/asns-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"
import { AsnSave } from "./asn-form"

const cols = createColumnHelper<AsnRow>()

const ASN_COLUMNS = [
  cols.accessor("asn_code", { header: "Awizo" }),
  cols.accessor("guide_code", { header: "Przewodnik" }),
  cols.accessor("plant_label", { header: "Zakład" }),
  cols.accessor("carrier_label", { header: "Przewoźnik" }),
  cols.accessor("ship_ref_label", { header: "Referencja" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const ASN_LABELS = {
  asn_code: "Awizo",
  guide_code: "Przewodnik",
  plant_label: "Zakład",
  carrier_label: "Przewoźnik",
  ship_ref_label: "Referencja",
  source_ref: "Pochodzenie",
}

function AsnTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listAsns,
    queryKey: ["asns", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={ASN_LABELS}
      columns={ASN_COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj awizo wysyłki…"
      tableKey={BUSINESS_LISTS.asn.tableKey}
    />
  )
}

export function AsnDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-asn="board">
      <CatalogHeading
        title="Awizo wysyłki"
        subtitle="CT1 asn · HITL na PO · nie live EDI · nie zlecenie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <AsnSave organizationId={ctx.organizationId} />
          <AsnTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
