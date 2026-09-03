import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  fetchParties,
  sanctionsParties,
  screenPartySanctions,
} from "@/lib/parties-api"
import { getTenantContext } from "@/lib/tenant"

function SanctionsScreenForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [partyId, setPartyId] = useState("")
  const [listRef, setListRef] = useState("")
  const save = useMutation({
    mutationFn: () =>
      screenPartySanctions(partyId.trim(), { sanctions_list_ref: listRef.trim() }),
    onSuccess: () => {
      setPartyId("")
      setListRef("")
      void client.invalidateQueries({ queryKey: ["sanctions-parties", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        save.mutate()
      }}
    >
      <Input aria-label="Kontrahent do sprawdzenia listy" placeholder="party_id" value={partyId} onChange={(event) => setPartyId(event.target.value)} required />
      <Input aria-label="Wskazanie listy sankcji" placeholder="sanctions_list_ref" value={listRef} onChange={(event) => setListRef(event.target.value)} required />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz sprawdzenie
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function SanctionsPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const parties = useQuery({
    queryKey: ["sanctions-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const rows = sanctionsParties(parties.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-sanctions="board">
      <CatalogHeading
        title="Sankcje"
        subtitle="sanctions M-53 · sprawdzenie listy na party · nie auto-match"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {parties.isError ? <CatalogError error={parties.error} /> : null}
      <SanctionsScreenForm organizationId={ctx.organizationId} />
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.legal_name} {row.tax_id ?? "—"} {row.country_code}{" "}
            {row.sanctions_list_ref ?? "—"}{" "}
            <Link className="underline" to="/parties">
              kontrahent
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
