import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildBlankSailingMarkWrite,
  saveBlankSailingMark,
} from "@/lib/blank-sailing-marks-api"

const KINDS = ["blank", "congestion", "gate", "other"] as const

export function BlankSailingMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("blank_01")
  const [kind, setKind] = useState<string>("blank")
  const [origin, setOrigin] = useState("fixture://blank-sailing-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveBlankSailingMark(buildBlankSailingMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("blank_01")
      setKind("blank")
      setOrigin("fixture://blank-sailing-mark/")
      void cache.invalidateQueries({
        queryKey: ["blank-sailing-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-blank-sailing-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja blank sailing / congestion / Gate OS jako katalog HITL. Nie countdown i nie charge.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika blank sailing"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj stancji</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="sailing-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://blank-sailing-mark/…)"
        ariaLabel="Pochodzenie znacznika blank sailing"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik blank sailing
      </Button>
    </form>
  )
}
