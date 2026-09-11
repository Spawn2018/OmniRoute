import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchDelayForecasts, type DelayForecastRow } from "@/lib/delay-forecasts-api"
import { getTenantContext } from "@/lib/tenant"
import { DelayForecastSave } from "./forecast-form"

const helper = createColumnHelper<DelayForecastRow>()

const COLUMNS = [
  helper.accessor("forecast_code", { header: "Kod" }),
  helper.accessor("horizon_hours", { header: "Horyzont h" }),
  helper.accessor("p_late", { header: "p_late" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function DelayForecastDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchDelayForecasts,
    queryKey: ["delay-forecasts", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-delay-forecast="board">
      <CatalogHeading
        title="Prognoza opóźnienia"
        subtitle="CI4 delay_forecast · katalog HITL · nie wróżba · nie GPS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <DelayForecastSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            forecast_code: "Kod",
            horizon_hours: "Horyzont h",
            p_late: "p_late",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj prognoz…"
          tableKey={BUSINESS_LISTS.delayForecast.tableKey}
        />
      ) : null}
    </section>
  )
}
