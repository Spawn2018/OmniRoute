import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildOogMarkWrite, saveOogMark } from "@/lib/oog-marks-api"

const KINDS = ["oog", "lashing", "escort", "other"] as const

export function OogMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("oog_escort_01")
  const [kind, setKind] = useState<string>("oog")
  const [origin, setOrigin] = useState("fixture://oog-mark/")
  const save = useMutation({
    mutationFn: () => saveOogMark(buildOogMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("oog_escort_01")
      setKind("oog")
      setOrigin("fixture://oog-mark/")
      void cache.invalidateQueries({ queryKey: ["oog-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-oog-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik OOG jako katalog HITL. Rodzaj eskorty to dana, nie wymiary i nie zezwolenie.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika OOG"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj eskorty</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="oog-escort"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://oog-mark/…)"
        ariaLabel="Pochodzenie znacznika OOG"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik OOG
      </Button>
    </form>
  )
}
