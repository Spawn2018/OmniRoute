import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchChargeCodes } from "@/lib/charge-codes-api"
import { bookkeepingLines, fetchCharges } from "@/lib/charges-api"
import { getTenantContext } from "@/lib/tenant"

export function BookkeepingPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const codes = useQuery({
    queryKey: ["bookkeeping-codes", ctx.organizationId],
    queryFn: fetchChargeCodes,
    enabled: ready,
    retry: false,
  })
  const charges = useQuery({
    queryKey: ["bookkeeping-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })
  const lines = bookkeepingLines(charges.data ?? [], codes.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-bookkeeping="board">
      <CatalogHeading
        title="Księgowość"
        subtitle="bookkeeping M-47 · charge_code.name + buy/sell · nie JPK · nie ERP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {codes.isError ? <CatalogError error={codes.error} /> : null}
      {charges.isError ? <CatalogError error={charges.error} /> : null}
      {lines.map((line) => (
        <p key={line.id} className="text-xs">
          {line.charge_code} {line.code_name} kupno{" "}
          <Money amount={line.buy_amount} currency={line.buy_currency} /> sprzedaż{" "}
          <Money amount={line.sell_amount} currency={line.sell_currency} />{" "}
          <Link className="underline" to="/charge-codes">
            kod
          </Link>{" "}
          <Link className="underline" to="/charges">
            opłata
          </Link>
        </p>
      ))}
    </section>
  )
}
