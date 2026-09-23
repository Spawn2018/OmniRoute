import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildHandoverBindMarkWrite,
  saveHandoverBindMark,
} from "@/lib/handover-bind-marks-api"

const BIND_OPTIONS = ["note", "board", "shift", "other"] as const

export function HandoverBindMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bind_note_01")
  const [kind, setKind] = useState<string>("note")
  const [ref, setRef] = useState("fixture://handover-bind/")
  const save = useMutation({
    mutationFn: () =>
      saveHandoverBindMark(buildHandoverBindMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("bind_note_01")
      setKind("note")
      setRef("fixture://handover-bind/")
      void cache.invalidateQueries({
        queryKey: ["handover-bind-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-handover-bind-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance wiązania przekazania jako dana HITL — nie FK UUID i nie T6 live.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod wiązania przekazania"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>bind_kind</legend>
        {BIND_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="handover-bind-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://handover-bind/…)"
        ariaLabel="Pochodzenie wiązania przekazania"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wiązanie przekazania
      </Button>
    </form>
  )
}
