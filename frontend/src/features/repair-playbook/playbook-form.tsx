import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildRepairPlaybookWrite, saveRepairPlaybook } from "@/lib/repair-playbooks-api"

const KINDS = ["contain", "reroute", "claim", "other"] as const

export function RepairPlaybookSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("contain_lane_01")
  const [kind, setKind] = useState<string>("contain")
  const [origin, setOrigin] = useState("fixture://repair-playbook/")
  const save = useMutation({
    mutationFn: () => saveRepairPlaybook(buildRepairPlaybookWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("contain_lane_01")
      setKind("contain")
      setOrigin("fixture://repair-playbook/")
      void cache.invalidateQueries({ queryKey: ["repair-playbooks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-repair-playbook="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Playbook naprawy jako katalog HITL. Postawa to dana, nie auto-send S11 i nie treść maila.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod playbooka naprawy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Postawa</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="repair-stance"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://repair-playbook/…)"
        ariaLabel="Pochodzenie playbooka naprawy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz playbook naprawy
      </Button>
    </form>
  )
}
