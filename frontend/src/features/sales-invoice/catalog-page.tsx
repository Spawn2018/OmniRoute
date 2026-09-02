import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchCharges } from "@/lib/charges-api"
import { getTenantContext } from "@/lib/tenant"

export function SalesInvoicePage() {
  const ctx = getTenantContext()
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)
  const catalog = useQuery({
    queryKey: ["sales-invoice-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: sessionReady,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-sales-invoice="board">
      <CatalogHeading
        title="Faktury"
        subtitle="sales_invoice M-40 · sell z charge · nie KSeF · nie nowa tabela"
      />
      {!sessionReady ? <TenantSessionNotice /> : null}
      {catalog.isError ? <CatalogError error={catalog.error} /> : null}
      <dl>
        {(catalog.data ?? []).map((charge) => (
          <div key={charge.id} className="text-xs">
            <dt>
              <Link className="underline" to="/charges">
                {charge.charge_code}
              </Link>
            </dt>
            <dd>
              <Money amount={charge.sell_amount} currency={charge.sell_currency} />{" "}
              <Link className="underline" to="/finance">
                finance
              </Link>
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
