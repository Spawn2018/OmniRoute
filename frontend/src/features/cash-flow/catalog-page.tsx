import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { cashFlowLegs, fetchCharges } from "@/lib/charges-api"
import { getTenantContext } from "@/lib/tenant"

export function CashFlowPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const charges = useQuery({
    queryKey: ["cash-flow-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })
  const legs = cashFlowLegs(charges.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-cash-flow="board">
      <CatalogHeading
        title="Przepływy"
        subtitle="cash_flow M-45 · wypływ buy i wpływ sell z charge · nie księga · nie odejmowanie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {charges.isError ? <CatalogError error={charges.error} /> : null}
      <ol>
        {legs.map((leg) => (
          <li key={leg.id} className="text-xs">
            {leg.charge_code}
            {" · wypływ "}
            <Money amount={leg.outflow_amount} currency={leg.outflow_currency} />
            {" · wpływ "}
            <Money amount={leg.inflow_amount} currency={leg.inflow_currency} />{" "}
            <Link className="underline" to="/charges">
              opłata
            </Link>
          </li>
        ))}
      </ol>
    </section>
  )
}
