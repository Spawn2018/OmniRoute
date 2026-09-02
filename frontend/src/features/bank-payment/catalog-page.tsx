import { useMutation, useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchCharges } from "@/lib/charges-api"
import {
  fetchBankAccounts,
  fetchParties,
  lookupIban,
  type IbanDraft,
} from "@/lib/parties-api"
import { getTenantContext } from "@/lib/tenant"

export function BankPaymentPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [partyId, setPartyId] = useState("")
  const [iban, setIban] = useState("")
  const [draft, setDraft] = useState<IbanDraft | null>(null)

  const parties = useQuery({
    queryKey: ["bank-payment-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const accounts = useQuery({
    queryKey: ["bank-payment-accounts", partyId],
    queryFn: () => fetchBankAccounts(partyId),
    enabled: ready && partyId !== "",
    retry: false,
  })
  const charges = useQuery({
    queryKey: ["bank-payment-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })
  const lookup = useMutation({
    mutationFn: () => lookupIban(iban),
    onSuccess: setDraft,
    onError: () => setDraft(null),
  })

  return (
    <section className="flex flex-col gap-3" data-bank-payment="board">
      <CatalogHeading
        title="Bank i płatności"
        subtitle="bank_payment M-42 · IBAN + sell z charge · nie tabela · nie SEPA"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {parties.isError ? <CatalogError error={parties.error} /> : null}
      {accounts.isError ? <CatalogError error={accounts.error} /> : null}
      {charges.isError ? <CatalogError error={charges.error} /> : null}
      {lookup.isError ? <CatalogError error={lookup.error} /> : null}
      <form
        className="flex flex-col gap-2"
        onSubmit={(event) => {
          event.preventDefault()
          lookup.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          iban-lookup
          <Input aria-label="IBAN do lookup" value={iban} onChange={(event) => setIban(event.target.value)} required />
        </label>
        <Button type="submit" disabled={!ready || lookup.isPending}>
          Sprawdź IBAN
        </Button>
      </form>
      {draft ? (
        <p className="text-xs">
          {draft.iban} {draft.whitelist_status}
        </p>
      ) : null}
      <fieldset className="text-xs">
        <legend>kontrahent</legend>
        <select
          aria-label="Kontrahent płatności"
          className="mt-1 w-full rounded border border-border bg-card px-2 py-1"
          value={partyId}
          onChange={(event) => setPartyId(event.currentTarget.value)}
        >
          <option value="">—</option>
          {(parties.data ?? []).map((party) => (
            <option key={party.id} value={party.id}>
              {party.legal_name}
            </option>
          ))}
        </select>
      </fieldset>
      <ul>
        {(accounts.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.iban} {row.currency} {row.whitelist_status}{" "}
            <Link className="underline" to="/parties">
              kontrahent
            </Link>
          </li>
        ))}
      </ul>
      <dl>
        {(charges.data ?? []).map((charge) => (
          <div key={charge.id} className="text-xs">
            <dt>{charge.charge_code}</dt>
            <dd>
              <Money amount={charge.sell_amount} currency={charge.sell_currency} />{" "}
              <Link className="underline" to="/invoices">
                faktura
              </Link>
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
