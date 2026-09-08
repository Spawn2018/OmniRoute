import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { PoolKindPanel } from "./pool-panel"

export function PalletBalanceBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-pallet-balance="board">
      <CatalogHeading
        title="Saldo palet"
        subtitle="D7 pallet_balance · Chep/LPR na kontrahencie · nie giełda · nie depozyt"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PoolKindPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
