import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildBillingMarkWrite, saveBillingMark } from "@/lib/billing-marks-api"

const KINDS = ["seat", "usage", "invoice", "other"] as const

export function BillingMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("seat_01")
  const [kind, setKind] = useState<string>("seat")
  const [origin, setOrigin] = useState("fixture://billing-mark/")
  const save = useMutation({
    mutationFn: () => saveBillingMark(buildBillingMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("seat_01")
      setKind("seat")
      setOrigin("fixture://billing-mark/")
      void cache.invalidateQueries({ queryKey: ["billing-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-billing-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Billing SaaS Omni jako katalog HITL. Rodzaj to dana, nie live Stripe i nie limity SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika billingu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj billingu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="yard-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://billing-mark/…)"
        ariaLabel="Pochodzenie znacznika billingu"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz billing
      </Button>
    </form>
  )
}
