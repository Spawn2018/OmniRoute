import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildSlaWrite, saveSlaClause } from "@/lib/sla-clauses-api"

const METRICS = ["otif", "delay", "damage", "other"] as const

export function SlaClauseSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [contractId, setContractId] = useState("")
  const [code, setCode] = useState("sla_otif_01")
  const [kind, setKind] = useState<string>("otif")
  const [threshold, setThreshold] = useState("OTIF >= 95%")
  const [origin, setOrigin] = useState("fixture://sla-clause/")
  const save = useMutation({
    mutationFn: () =>
      saveSlaClause(
        buildSlaWrite({
          contractId,
          code,
          kind,
          threshold,
          origin,
        }),
      ),
    onSuccess: () => {
      setContractId("")
      setCode("sla_otif_01")
      setKind("otif")
      setThreshold("OTIF >= 95%")
      setOrigin("fixture://sla-clause/")
      void cache.invalidateQueries({ queryKey: ["sla-clauses", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-sla-clause="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Klauzula SLA na istniejącej umowie. Bez extractu LLM, bez kary SQL i bez ciphertext.
      </p>
      <label className="grid gap-1 text-xs">
        Id umowy (customer_contract_id)
        <input
          aria-label="Identyfikator umowy klienta"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setContractId(change.target.value)}
          required
          value={contractId}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Kod klauzuli (snake 2–32)
        <input
          aria-label="Kod klauzuli SLA"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>Metryka</legend>
        <div className="flex flex-wrap gap-3">
          {METRICS.map((token) => (
            <label key={token} className="flex items-center gap-1">
              <input
                checked={kind === token}
                name="sla-metric"
                onChange={() => setKind(token)}
                type="radio"
                value={token}
              />
              {token}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="grid gap-1 text-xs">
        Próg (tekst, nie liczenie)
        <input
          aria-label="Próg klauzuli SLA"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setThreshold(change.target.value)}
          required
          value={threshold}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://sla-clause/…)"
        ariaLabel="Pochodzenie klauzuli SLA"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz klauzulę SLA
      </Button>
    </form>
  )
}
