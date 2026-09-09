import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { WeatherPanel } from "./weather-form"

export function WeatherDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-weather-observation="desk">
      <CatalogHeading
        title="Pogoda"
        subtitle="V2 weather_observation · warunek + UN/LOCODE + czas · nie Open-Meteo"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <WeatherPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
