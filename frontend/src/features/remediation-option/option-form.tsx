import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildRemediationWrite, saveRemediationOption } from "@/lib/remediation-options-api"

const KINDS = ["rebook", "wait", "claim", "other"] as const

export function RemediationOptionSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("rebook_lane_01")
  const [kind, setKind] = useState<string>("rebook")
  const [origin, setOrigin] = useState("fixture://remediation-option/")
  const save = useMutation({
    mutationFn: () => saveRemediationOption(buildRemediationWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("rebook_lane_01")
      setKind("rebook")
      setOrigin("fixture://remediation-option/")
      void cache.invalidateQueries({ queryKey: ["remediation-options", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-remediation-option="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Opcja naprawy jako katalog HITL. Rodzaj to dana, nie kwota i nie auto-send S11.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod opcji naprawy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="remediation-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://remediation-option/…)"
        ariaLabel="Pochodzenie opcji naprawy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz opcję naprawy
      </Button>
    </form>
  )
}
