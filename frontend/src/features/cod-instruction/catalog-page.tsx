import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { CollectionMarkPanel } from "./collection-form"

export function CodBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-cod="board">
      <CatalogHeading
        title="Pobranie COD"
        subtitle="D4 cod_instruction · znacznik na zleceniu · nie kwota · nie Fala F"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CollectionMarkPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
