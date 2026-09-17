import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildSelfBillingMarkWrite,
  saveSelfBillingMark,
} from "@/lib/self-billing-marks-api"

const KINDS = ["self", "subcontractor", "other"] as const

export function SelfBillingMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("self_01")
  const [kind, setKind] = useState<string>("self")
  const [origin, setOrigin] = useState("fixture://self-billing-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveSelfBillingMark(buildSelfBillingMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("self_01")
      setKind("self")
      setOrigin("fixture://self-billing-mark/")
      void cache.invalidateQueries({
        queryKey: ["self-billing-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-self-billing-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Self-billing podwykonawcy jako katalog HITL. Rodzaj to dana, nie live JPK
        i nie auto FV.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika self-billing"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj self-billing</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="self-billing-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://self-billing-mark/…)"
        ariaLabel="Pochodzenie znacznika self-billing"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz self-billing
      </Button>
    </form>
  )
}
