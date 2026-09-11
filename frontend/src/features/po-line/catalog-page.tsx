import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listPoLines, type PoLineRow } from "@/lib/po-lines-api"
import { getTenantContext } from "@/lib/tenant"
import { PoLineSave } from "./po-line-form"

const cols = createColumnHelper<PoLineRow>()

const PO_LINE_COLUMNS = [
  cols.accessor("line_code", { header: "Linia" }),
  cols.accessor("sku_code", { header: "SKU" }),
  cols.accessor("qty", { header: "Ilość" }),
  cols.accessor("uom_code", { header: "JM" }),
  cols.accessor("plant_label", { header: "Zakład" }),
  cols.accessor("batch_label", { header: "Partia" }),
  cols.accessor("serial_label", { header: "Seria" }),
  cols.accessor("coo_label", { header: "Kraj" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const PO_LINE_LABELS = {
  line_code: "Linia",
  sku_code: "SKU",
  qty: "Ilość",
  uom_code: "JM",
  plant_label: "Zakład",
  batch_label: "Partia",
  serial_label: "Seria",
  coo_label: "Kraj",
  source_ref: "Pochodzenie",
}

function PoLineTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listPoLines,
    queryKey: ["po-lines", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={PO_LINE_LABELS}
      columns={PO_LINE_COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj linię zamówienia…"
      tableKey={BUSINESS_LISTS.poLine.tableKey}
    />
  )
}

export function PoLineDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-po-line="board">
      <CatalogHeading
        title="Linia zamówienia zakupu"
        subtitle="CT1 po_line · qty Decimal · nie ASN · nie zlecenie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <PoLineSave organizationId={ctx.organizationId} />
          <PoLineTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
