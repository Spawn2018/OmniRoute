import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildWorkingCapitalMarkWrite, saveWorkingCapitalMark } from "@/lib/working-capital-marks-api"

const KINDS = ["dso", "cash_at_risk", "aging", "other"] as const

export function WorkingCapitalMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("dso_01")
  const [kind, setKind] = useState<string>("dso")
  const [origin, setOrigin] = useState("fixture://working-capital-mark/")
  const save = useMutation({
    mutationFn: () => saveWorkingCapitalMark(buildWorkingCapitalMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("dso_01")
      setKind("dso")
      setOrigin("fixture://working-capital-mark/")
      void cache.invalidateQueries({ queryKey: ["working-capital-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-working-capital-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Working capital jako katalog HITL. Rodzaj to dana, nie druga marża i nie DSO SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika working capital"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj WC</legend>
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
        label="source_ref (tenant:manual albo fixture://working-capital-mark/…)"
        ariaLabel="Pochodzenie znacznika working capital"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz WC
      </Button>
    </form>
  )
}
