import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { ledgerWrite, listLedgerRows, persistLedgerRow } from "@/lib/pallet-ledgers-api"
import { getTenantContext } from "@/lib/tenant"

const KINDS = ["chep", "lpr", "epal"] as const

type Draft = {
  counterpartToken: string
  codeToken: string
  kindToken: string
  deltaToken: string
  originStamp: string
}

const EMPTY: Draft = {
  counterpartToken: "",
  codeToken: "issue_01",
  kindToken: "chep",
  deltaToken: "-1",
  originStamp: "fixture://pallet-ledger/",
}

function LedgerForm(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY)
  const persist = useMutation({
    mutationFn: () => persistLedgerRow(ledgerWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY })
      void cache.invalidateQueries({ queryKey: ["pallet-ledgers", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-pallet-ledger="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Ruch sztuk palet ze znakiem (wydanie ujemne, zwrot dodatni). Nie zmienia salda na
        `/pallet-balances` i nie jest giełdą.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Identyfikator kontrahenta
        <input
          aria-label="Identyfikator kontrahenta ruchu palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.counterpartToken}
          onChange={(change) => setDraft({ ...draft, counterpartToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod ruchu
        <input
          aria-label="Kod ruchu palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeToken}
          onChange={(change) => setDraft({ ...draft, codeToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj palety
        <select
          aria-label="Rodzaj palety ruchu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindToken}
          onChange={(change) => setDraft({ ...draft, kindToken: change.target.value })}
        >
          {KINDS.map((kind) => (
            <option key={kind} value={kind}>
              {kind}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Delta sztuk (ze znakiem)
        <input
          aria-label="Delta sztuk ruchu palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          inputMode="numeric"
          value={draft.deltaToken}
          onChange={(change) => setDraft({ ...draft, deltaToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu
        <input
          aria-label="Pochodzenie zapisu ruchu palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz ruch palet
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function LedgerList(args: { organizationId: string | null }) {
  const query = useQuery({
    queryKey: ["pallet-ledgers", args.organizationId],
    queryFn: listLedgerRows,
    enabled: Boolean(args.organizationId),
  })
  if (query.isLoading) return <p className="text-xs text-muted-foreground">Ładowanie…</p>
  if (query.isError) return <CatalogError error={query.error} />
  const rows = query.data ?? []
  if (rows.length === 0) {
    return <p className="text-xs text-muted-foreground">Brak ruchów palet.</p>
  }
  return (
    <ul className="flex flex-col gap-2 font-mono text-xs" data-pallet-ledger="list">
      {rows.map((row) => (
        <li key={row.id}>
          {row.movement_code} · {row.pallet_kind} · {row.delta_count} · {row.source_ref}
        </li>
      ))}
    </ul>
  )
}

export function PalletLedgerBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  return (
    <section className="flex flex-col gap-4" data-pallet-ledger="board">
      <CatalogHeading
        title="Ledger ruchu palet"
        subtitle="D7c pallet_ledger · delta ze znakiem · nie mutuje salda · nie giełda"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <>
          <LedgerForm organizationId={ctx.organizationId} />
          <LedgerList organizationId={ctx.organizationId} />
        </>
      ) : null}
    </section>
  )
}
