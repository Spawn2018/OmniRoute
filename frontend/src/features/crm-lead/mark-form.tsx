import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCrmLeadWrite, saveCrmLead } from "@/lib/crm-leads-api"

const KINDS = ["new", "qualified", "disqualified", "other"] as const

export function CrmLeadSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("lead_acme_01")
  const [kind, setKind] = useState<string>("new")
  const [origin, setOrigin] = useState("fixture://crm-lead/")
  const save = useMutation({
    mutationFn: () => saveCrmLead(buildCrmLeadWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("lead_acme_01")
      setKind("new")
      setOrigin("fixture://crm-lead/")
      void cache.invalidateQueries({ queryKey: ["crm-leads", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-crm-lead="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Lead CRM jako katalog HITL. Etap to dana, nie cold auto-send i nie szansa.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod leada CRM"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Etap leada</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="crm-stage"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://crm-lead/…)"
        ariaLabel="Pochodzenie leada CRM"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz leada CRM
      </Button>
    </form>
  )
}
