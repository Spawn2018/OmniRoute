import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildImpactWrite, saveImpactScenario } from "@/lib/impact-scenarios-api"

export function ImpactScenarioSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("stock_to_sales_01")
  const [label, setLabel] = useState("stock to sales")
  const [origin, setOrigin] = useState("fixture://impact-scenario/")
  const save = useMutation({
    mutationFn: () => saveImpactScenario(buildImpactWrite({ code, label, origin })),
    onSuccess: () => {
      setCode("stock_to_sales_01")
      setLabel("stock to sales")
      setOrigin("fixture://impact-scenario/")
      void cache.invalidateQueries({ queryKey: ["impact-scenarios", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-impact-scenario="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Scenariusz skutku jako katalog HITL. Etykieta łańcucha to dana, nie EBITDA SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod scenariusza skutku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Etykieta łańcucha (1–64)
        <input
          aria-label="Etykieta łańcucha scenariusza"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setLabel(change.target.value)}
          required
          value={label}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://impact-scenario/…)"
        ariaLabel="Pochodzenie scenariusza skutku"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz scenariusz skutku
      </Button>
    </form>
  )
}
