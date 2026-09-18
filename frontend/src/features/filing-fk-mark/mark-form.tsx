import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildFilingFkMarkWrite,
  saveFilingFkMark,
} from "@/lib/filing-fk-marks-api"

const KINDS = ["shipment", "scheme", "other"] as const

export function FilingFkMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("fk_01")
  const [kind, setKind] = useState<string>("shipment")
  const [origin, setOrigin] = useState("fixture://filing-fk-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveFilingFkMark(buildFilingFkMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("fk_01")
      setKind("shipment")
      setOrigin("fixture://filing-fk-mark/")
      void cache.invalidateQueries({
        queryKey: ["filing-fk-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-filing-fk-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Cel FK zgłoszenia jako katalog HITL. Rodzaj to dana, nie live UUID i nie PUESC.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika celu FK zgłoszenia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj celu FK</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="filing-fk-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://filing-fk-mark/…)"
        ariaLabel="Pochodzenie znacznika celu FK"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz cel FK
      </Button>
    </form>
  )
}
