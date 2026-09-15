import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCrmActivityWrite, saveCrmActivity } from "@/lib/crm-activities-api"

const KINDS = ["call", "meeting", "email", "note", "other"] as const

export function CrmActivitySave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("act_call_01")
  const [kind, setKind] = useState<string>("call")
  const [origin, setOrigin] = useState("fixture://crm-activity/")
  const save = useMutation({
    mutationFn: () => saveCrmActivity(buildCrmActivityWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("act_call_01")
      setKind("call")
      setOrigin("fixture://crm-activity/")
      void cache.invalidateQueries({ queryKey: ["crm-activities", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-crm-activity="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Aktywność CRM jako katalog HITL. Rodzaj to dana, nie silnik pipeline i nie FK okazji.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod aktywności CRM"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj aktywności</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="crm-activity-stage"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://crm-activity/…)"
        ariaLabel="Pochodzenie aktywności CRM"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz aktywność CRM
      </Button>
    </form>
  )
}
