import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildSpendMarkWrite, saveSpendMark } from "@/lib/spend-marks-api"

const KINDS = ["invoice", "clause", "other"] as const

export function SpendMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("invoice_leak_01")
  const [kind, setKind] = useState<string>("invoice")
  const [origin, setOrigin] = useState("fixture://spend-mark/")
  const save = useMutation({
    mutationFn: () => saveSpendMark(buildSpendMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("invoice_leak_01")
      setKind("invoice")
      setOrigin("fixture://spend-mark/")
      void cache.invalidateQueries({ queryKey: ["spend-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-spend-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik wycieku spend jako katalog HITL. Rodzaj to dana, nie SQL FV vs charge i nie
        druga marża.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika wycieku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj wycieku</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="spend-leakage"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://spend-mark/…)"
        ariaLabel="Pochodzenie znacznika wycieku"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik wycieku
      </Button>
    </form>
  )
}
