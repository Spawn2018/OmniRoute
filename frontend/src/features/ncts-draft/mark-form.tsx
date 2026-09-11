import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildNctsDraftWrite, saveNctsDraft } from "@/lib/ncts-drafts-api"

const KINDS = ["t1", "t2", "other"] as const

export function NctsDraftSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ncts_t1_01")
  const [kind, setKind] = useState<string>("t1")
  const [origin, setOrigin] = useState("fixture://ncts-draft/")
  const save = useMutation({
    mutationFn: () => saveNctsDraft(buildNctsDraftWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("ncts_t1_01")
      setKind("t1")
      setOrigin("fixture://ncts-draft/")
      void cache.invalidateQueries({ queryKey: ["ncts-drafts", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-ncts-draft="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Szkic NCTS jako katalog HITL. Rodzaj tranzytu to dana, nie PUESC live i nie XML.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod szkicu NCTS"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj tranzytu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="ncts-transit"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://ncts-draft/…)"
        ariaLabel="Pochodzenie szkicu NCTS"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz szkic NCTS
      </Button>
    </form>
  )
}
