import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchCharges } from "@/lib/charges-api"
import { fetchNbpRates, nbpRatesForKnownCurrencies } from "@/lib/nbp-rates-api"
import { fetchQuotations } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_LANE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

export function FxDifferencePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rates = useQuery({
    queryKey: ["fx-difference-nbp", ctx.organizationId],
    queryFn: fetchNbpRates,
    enabled: ready,
    retry: false,
  })
  const charges = useQuery({
    queryKey: ["fx-difference-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })
  const quotations = useQuery({
    queryKey: ["fx-difference-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_LANE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const matched = nbpRatesForKnownCurrencies(
    rates.data ?? [],
    charges.data ?? [],
    quotations.data ?? [],
  )

  return (
    <section className="flex flex-col gap-3" data-fx-difference="board">
      <CatalogHeading
        title="Różnice kursowe"
        subtitle="fx_difference M-44 · NBP walut z charge/quotation · nie tabela · nie przeliczenie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rates.isError ? <CatalogError error={rates.error} /> : null}
      {charges.isError ? <CatalogError error={charges.error} /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      <ul>
        {matched.map((row) => (
          <li key={row.id} className="text-xs">
            {row.currency} {row.rate_date} {row.mid}{" "}
            <Link className="underline" to="/nbp-rates">
              NBP
            </Link>
            {" · "}
            <Link className="underline" to="/charges">
              opłata
            </Link>
            {" · "}
            <Link className="underline" to="/quotations">
              wycena
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
