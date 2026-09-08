import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { WeightBandPanel } from "./band-form"

export function TariffDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tariff="desk">
      <CatalogHeading
        title="Cennik drobnicy"
        subtitle="D5 groupage_tariff · próg wagi na strefie · nie silnik P1"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <WeightBandPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
