import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildPostalEpoMarkWrite, savePostalEpoMark } from "@/lib/postal-epo-marks-api"

const KINDS = ["register", "label", "track", "other"] as const

export function PostalEpoMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("epo_01")
  const [kind, setKind] = useState<string>("register")
  const [origin, setOrigin] = useState("fixture://postal-epo-mark/")
  const save = useMutation({
    mutationFn: () => savePostalEpoMark(buildPostalEpoMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("epo_01")
      setKind("register")
      setOrigin("fixture://postal-epo-mark/")
      void cache.invalidateQueries({ queryKey: ["postal-epo-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-postal-epo-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja EPO/PP jako katalog HITL. Rodzaj to dana, nie live PP i nie e-Doręczenia.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika EPO"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj EPO</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="postal-epo-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://postal-epo-mark/…)"
        ariaLabel="Pochodzenie znacznika EPO"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz EPO
      </Button>
    </form>
  )
}
