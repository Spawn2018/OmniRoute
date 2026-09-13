import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildGroupageDispatcherMarkWrite,
  saveGroupageDispatcherMark,
} from "@/lib/groupage-dispatcher-marks-api"

const KINDS = ["line", "hub", "cutoff", "consol", "other"] as const

export function GroupageDispatcherMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("gdp_line_01")
  const [kind, setKind] = useState<string>("line")
  const [origin, setOrigin] = useState("fixture://groupage-dispatcher-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveGroupageDispatcherMark(buildGroupageDispatcherMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("gdp_line_01")
      setKind("line")
      setOrigin("fixture://groupage-dispatcher-mark/")
      void cache.invalidateQueries({
        queryKey: ["groupage-dispatcher-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-groupage-dispatcher-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance dyspozytora drobnicy jako katalog HITL. Rodzaj to dana, nie silnik hubów.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika dyspozytora drobnicy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj dyspozytora</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="groupage-dispatcher-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://groupage-dispatcher-mark/…)"
        ariaLabel="Pochodzenie znacznika dyspozytora drobnicy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance dyspozytora
      </Button>
    </form>
  )
}
