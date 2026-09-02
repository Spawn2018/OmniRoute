import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { customerSopsForParty, fetchCustomerSops } from "@/lib/customer-sops-api"
import { fetchParties } from "@/lib/parties-api"
import { fetchQuotations } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

export function CostToServePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [partyId, setPartyId] = useState("")
  const parties = useQuery({
    queryKey: ["cost-to-serve-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const sops = useQuery({
    queryKey: ["cost-to-serve-sops", ctx.organizationId],
    queryFn: fetchCustomerSops,
    enabled: ready,
    retry: false,
  })
  const quotations = useQuery({
    queryKey: ["cost-to-serve-quotations", ctx.organizationId, partyId],
    queryFn: () =>
      fetchQuotations({ partyId, originPortId: "", destinationPortId: "" }),
    enabled: ready && partyId !== "",
    retry: false,
  })
  const matchedSops = customerSopsForParty(sops.data ?? [], partyId)

  return (
    <section className="flex flex-col gap-3" data-cost-to-serve="board">
      <CatalogHeading
        title="Koszt obsługi klienta"
        subtitle="cost_to_serve M-46 · SOP i wyceny kontrahenta · nie ABC · nie suma"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {parties.isError ? <CatalogError error={parties.error} /> : null}
      {sops.isError ? <CatalogError error={sops.error} /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      <p className="flex flex-wrap gap-1 text-xs">
        {(parties.data ?? []).map((party) => (
          <button
            key={party.id}
            className="rounded border border-border px-2 py-1"
            onClick={() => setPartyId(party.id)}
            type="button"
          >
            {party.legal_name}
          </button>
        ))}
      </p>
      <ul>
        {matchedSops.map((sop) => (
          <li key={sop.id} className="text-xs">
            {sop.code} {sop.title} {sop.status}{" "}
            <Link className="underline" to="/customer-sops">
              SOP
            </Link>
          </li>
        ))}
      </ul>
      <ol>
        {(quotations.data ?? []).map((row) => (
          <li key={row.id} className="text-xs">
            {row.charge_code}{" "}
            <Money amount={row.amount} currency={row.currency} />{" "}
            <Link className="underline" to="/quotations">
              wycena
            </Link>
          </li>
        ))}
      </ol>
    </section>
  )
}
