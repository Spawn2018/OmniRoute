import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { CellPanel } from "./cell-form"

export function CellDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-matrix-cell="desk">
      <CatalogHeading
        title="Komórki matrycy"
        subtitle="G2.5 tender_matrix_cell · kwota Decimal z P · nie LLM"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CellPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
