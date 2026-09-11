import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildMakeOrBuyMarkWrite, saveMakeOrBuyMark } from "@/lib/make-or-buy-marks-api"

const KINDS = ["make", "buy", "hybrid", "other"] as const

export function MakeOrBuyMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("make_01")
  const [kind, setKind] = useState<string>("dso")
  const [origin, setOrigin] = useState("fixture://make-or-buy-mark/")
  const save = useMutation({
    mutationFn: () => saveMakeOrBuyMark(buildMakeOrBuyMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("make_01")
      setKind("dso")
      setOrigin("fixture://make-or-buy-mark/")
      void cache.invalidateQueries({ queryKey: ["make-or-buy-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-make-or-buy-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Make-or-buy jako katalog HITL. Rodzaj to dana, nie silnik kosztu i nie silnik kosztu.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika make-or-buy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj make-or-buy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="yard-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://make-or-buy-mark/…)"
        ariaLabel="Pochodzenie znacznika make-or-buy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz make-or-buy
      </Button>
    </form>
  )
}
