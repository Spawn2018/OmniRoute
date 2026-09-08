import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listPoolMarks, persistPoolMark, poolWrite } from "@/lib/pallet-balances-api"

const KINDS = ["chep", "lpr"] as const

type PoolDraft = {
  counterpartToken: string
  kindToken: string
  countToken: string
  originStamp: string
}

const EMPTY_POOL: PoolDraft = {
  counterpartToken: "",
  kindToken: "chep",
  countToken: "0",
  originStamp: "fixture://pallet-balance/",
}

function PoolSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_POOL)
  const persist = useMutation({
    mutationFn: () => persistPoolMark(poolWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_POOL })
      void cache.invalidateQueries({ queryKey: ["pool-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-pallet-balance="pool-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Saldo sztuk palet Chep albo LPR na kontrahencie. To nie giełda i nie depozyt na
        `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Identyfikator kontrahenta palet
        <input
          aria-label="Identyfikator kontrahenta palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.counterpartToken}
          onChange={(change) => setDraft({ ...draft, counterpartToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj palety
        <select
          aria-label="Rodzaj palety"
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
        Liczba sztuk
        <input
          aria-label="Liczba sztuk"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          inputMode="numeric"
          value={draft.countToken}
          onChange={(change) => setDraft({ ...draft, countToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu salda palet
        <input
          aria-label="Pochodzenie zapisu salda palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz saldo palet
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function PoolRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["pool-marks", args.organizationId],
    queryFn: listPoolMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-pallet-balance="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap gap-2 font-mono">
            <span>{row.pallet_kind}</span>
            <span>{row.unit_count}</span>
            <Link className="underline" to="/parties">
              kontrahent
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function PoolKindPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <PoolSave organizationId={args.organizationId} />
      <PoolRows organizationId={args.organizationId} />
    </>
  )
}
