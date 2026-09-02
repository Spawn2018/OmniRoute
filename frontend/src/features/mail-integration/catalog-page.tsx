import { useMutation, useQuery } from "@tanstack/react-query"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  fetchContacts,
  fetchEmailDomains,
  fetchParties,
  resolvePartyEmail,
  type Party,
} from "@/lib/parties-api"
import { getTenantContext } from "@/lib/tenant"

export function MailIntegrationPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [partyId, setPartyId] = useState("")
  const [email, setEmail] = useState("")
  const [resolved, setResolved] = useState<Party | null>(null)

  const parties = useQuery({
    queryKey: ["mail-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const domains = useQuery({
    queryKey: ["mail-domains", partyId],
    queryFn: () => fetchEmailDomains(partyId),
    enabled: ready && partyId !== "",
    retry: false,
  })
  const contacts = useQuery({
    queryKey: ["mail-contacts", partyId],
    queryFn: () => fetchContacts(partyId),
    enabled: ready && partyId !== "",
    retry: false,
  })
  const lookup = useMutation({
    mutationFn: () => resolvePartyEmail(email),
    onSuccess: (row) => {
      setResolved(row)
      setPartyId(row.id)
    },
    onError: () => {
      setResolved(null)
    },
  })

  return (
    <div className="flex flex-col gap-4" data-mail-integration="board">
      <CatalogHeading
        title="Poczta"
        subtitle="mail_integration M-32 · znane adresy · nie IMAP · nie skrzynka"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {parties.isError ? <CatalogError error={parties.error} /> : null}
      {domains.isError ? <CatalogError error={domains.error} /> : null}
      {contacts.isError ? <CatalogError error={contacts.error} /> : null}
      {lookup.isError ? <CatalogError error={lookup.error} /> : null}

      <form
        className="flex flex-col gap-2"
        onSubmit={(event) => {
          event.preventDefault()
          lookup.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          resolve_email
          <Input
            aria-label="Adres do resolve_email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <Button type="submit" disabled={!ready || lookup.isPending}>
          Sprawdź mail
        </Button>
      </form>
      {resolved ? <p className="text-xs">{resolved.legal_name}</p> : null}

      <label className="flex flex-col gap-1 text-xs">
        party.id
        <select
          aria-label="Kontrahent poczty"
          className="h-8 rounded-md border border-border bg-card px-2 text-sm"
          value={partyId}
          onChange={(event) => setPartyId(event.target.value)}
        >
          <option value="">Wybierz kontrahenta</option>
          {(parties.data ?? []).map((row) => (
            <option key={row.id} value={row.id}>
              {row.legal_name}
            </option>
          ))}
        </select>
      </label>

      <section className="space-y-1">
        <h2 className="text-sm font-medium">Domeny</h2>
        {(domains.data ?? []).map((row) => (
          <p key={row.id} className="font-mono text-xs">
            {row.domain}
          </p>
        ))}
      </section>
      <section className="space-y-1">
        <h2 className="text-sm font-medium">Kontakty</h2>
        {(contacts.data ?? []).map((row) =>
          row.email === null ? null : (
            <p key={row.id} className="text-xs">
              {row.name} {row.email}
            </p>
          ),
        )}
      </section>
    </div>
  )
}
