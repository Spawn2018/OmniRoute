import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildPostalDispatchMarkWrite,
  savePostalDispatchMark,
} from "@/lib/postal-dispatch-marks-api"

const KINDS = ["en", "uss", "epo", "other"] as const

export function PostalDispatchMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("postal_01")
  const [kind, setKind] = useState<string>("en")
  const [origin, setOrigin] = useState("fixture://postal-dispatch-mark/")
  const save = useMutation({
    mutationFn: () =>
      savePostalDispatchMark(buildPostalDispatchMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("postal_01")
      setKind("en")
      setOrigin("fixture://postal-dispatch-mark/")
      void cache.invalidateQueries({
        queryKey: ["postal-dispatch-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-postal-dispatch-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja ksiazki PP (EN/USS/EPO) jako katalog HITL. Rodzaj to dana, nie
        live Poczta Polska i nie e-Doreczenia.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika ksiazki PP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj wysylki PP</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="postal-dispatch-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://postal-dispatch-mark/…)"
        ariaLabel="Pochodzenie znacznika ksiazki PP"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik PP
      </Button>
    </form>
  )
}
