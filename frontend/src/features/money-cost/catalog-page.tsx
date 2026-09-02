import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchCharges } from "@/lib/charges-api"
import { fetchNbpRates } from "@/lib/nbp-rates-api"
import { getTenantContext } from "@/lib/tenant"

export function MoneyCostPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rates = useQuery({
    queryKey: ["money-cost-nbp", ctx.organizationId],
    queryFn: fetchNbpRates,
    enabled: ready,
    retry: false,
  })
  const charges = useQuery({
    queryKey: ["money-cost-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-money-cost="board">
      <CatalogHeading
        title="Koszt pieniądza"
        subtitle="money_cost M-43 · NBP + buy z charge · nie odsetki · nie mnożenie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rates.isError ? <CatalogError error={rates.error} /> : null}
      {charges.isError ? <CatalogError error={charges.error} /> : null}
      <ul>
        {(rates.data ?? []).map((row) => (
          <li key={row.id} className="text-xs">
            {row.currency} {row.rate_date} {row.mid}{" "}
            <Link className="underline" to="/nbp-rates">
              kurs
            </Link>
          </li>
        ))}
      </ul>
      <dl>
        {(charges.data ?? []).map((charge) => (
          <div key={charge.id} className="text-xs">
            <dt>{charge.charge_code}</dt>
            <dd>
              <Money amount={charge.buy_amount} currency={charge.buy_currency} />{" "}
              <Link className="underline" to="/charges">
                kupno
              </Link>
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
