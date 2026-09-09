import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { edgeWrite, listMemoryEdges, persistEdgeMark } from "@/lib/memory-edges-api"

type LinkDraft = {
  linkKind: string
  originToken: string
}

const BLANK_LINK: LinkDraft = {
  linkKind: "recalls",
  originToken: "fixture://memory-edge/",
}

const LINKS = ["recalls", "follows", "blocks", "cites", "other"] as const

function EdgeComposer(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(BLANK_LINK)
  const persist = useMutation({
    mutationFn: () => persistEdgeMark(edgeWrite(draft)),
    onSuccess: () => {
      setDraft({ ...BLANK_LINK })
      void cache.invalidateQueries({ queryKey: ["memory-link-stamps", args.organizationId] })
    },
  })
  const idle = Boolean(args.organizationId) && !persist.isPending
  return (
    <form
      className="max-w-sm space-y-4"
      data-memory-edge="kind-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (idle) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Pięć rodzajów krawędzi (recalls, follows, blocks, cites, other).
        To nie jest graf na zdarzeniach i nie wyszukiwanie stawek. Marża zostaje na `/charges`.
      </p>
      <fieldset>
        <legend className="mb-2 text-xs">Rodzaj krawędzi (allowlista)</legend>
        <div className="flex flex-wrap gap-2">
          {LINKS.map((token) => (
            <label
              key={token}
              className="inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs font-mono"
            >
              <input
                type="radio"
                name="memory-edge-kind"
                aria-label={`Krawędź ${token}`}
                checked={draft.linkKind === token}
                onChange={() => setDraft({ ...draft, linkKind: token })}
                value={token}
              />
              {token}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="block space-y-1 text-xs">
        Pochodzenie zapisu
        <input
          aria-label="source_ref krawędzi pamięci"
          className="h-9 w-full rounded-md border bg-background px-2 font-mono"
          value={draft.originToken}
          onChange={(change) => setDraft({ ...draft, originToken: change.target.value })}
          placeholder="tenant:manual albo fixture://memory-edge/…"
          required
        />
      </label>
      <Button type="submit" disabled={!idle}>
        Zapisz krawędź pamięci
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function EdgeLedger(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["memory-link-stamps", args.organizationId],
    queryFn: listMemoryEdges,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <div>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ol data-memory-edge="rows" className="list-decimal space-y-1 pl-5 text-xs">
        {rows.map((row) => (
          <li key={row.id} className="font-mono" data-edge-kind={row.edge_kind}>
            {row.edge_kind} · {row.source_ref}
          </li>
        ))}
      </ol>
    </div>
  )
}

export function EdgeBoard(args: { organizationId: string | null }) {
  return (
    <aside className="flex flex-col gap-10 md:flex-row">
      <EdgeComposer organizationId={args.organizationId} />
      <EdgeLedger organizationId={args.organizationId} />
    </aside>
  )
}
