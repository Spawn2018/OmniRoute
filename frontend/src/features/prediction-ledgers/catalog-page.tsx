import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { LedgerPanel } from "./ledger-form"

export function LedgerDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-prediction-ledger="desk">
      <CatalogHeading
        title="Ledger predykcji"
        subtitle="B0b/V1 prediction_ledger · przedział + CRPS/MAE · nie silnik"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LedgerPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
