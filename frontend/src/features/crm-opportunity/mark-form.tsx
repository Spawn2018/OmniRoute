import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCrmOpportunityWrite, saveCrmOpportunity } from "@/lib/crm-opportunities-api"

const KINDS = ["open", "won", "lost", "other"] as const

export function CrmOpportunitySave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("opp_acme_01")
  const [kind, setKind] = useState<string>("open")
  const [origin, setOrigin] = useState("fixture://crm-opportunity/")
  const save = useMutation({
    mutationFn: () => saveCrmOpportunity(buildCrmOpportunityWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("opp_acme_01")
      setKind("open")
      setOrigin("fixture://crm-opportunity/")
      void cache.invalidateQueries({ queryKey: ["crm-opportunities", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-crm-opportunity="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Okazja CRM jako katalog HITL. Etap to dana, nie silnik pipeline i nie activity.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod okazji CRM"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Etap okazji</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="crm-opportunity-stage"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://crm-opportunity/…)"
        ariaLabel="Pochodzenie okazji CRM"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz okazję CRM
      </Button>
    </form>
  )
}
