import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCostAllocationMarkWrite, saveCostAllocationMark } from "@/lib/cost-allocation-marks-api"

const ALLOC_OPTIONS = [
  { value: "direct", label: "direct — bezpośredni" },
  { value: "abc", label: "abc — Activity-Based Costing" },
  { value: "shared", label: "shared — wspólny" },
  { value: "other", label: "other — inny" },
] as const

export function CostAllocationMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("direct_01")
  const [allocKind, setAllocKind] = useState("direct")
  const [sourceRef, setSourceRef] = useState("fixture://cost-allocation-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveCostAllocationMark(
        buildCostAllocationMarkWrite({ code: markCode, kind: allocKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("direct_01")
      setAllocKind("direct")
      setSourceRef("fixture://cost-allocation-mark/")
      void cache.invalidateQueries({ queryKey: ["cost-allocation-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-cost-allocation-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog HITL podziału kosztów. `alloc_kind` to etykieta operatora — nie silnik allocation SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod znacznika (snake 2–32)
        <input
          aria-label="Kod znacznika cost allocation"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Rodzaj podziału (`alloc_kind`)
        <select
          aria-label="Rodzaj cost allocation"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setAllocKind(change.target.value)}
          value={allocKind}
        >
          {ALLOC_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://cost-allocation-mark/…)"
        ariaLabel="Pochodzenie znacznika cost allocation"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz cost allocation
      </Button>
    </form>
  )
}
