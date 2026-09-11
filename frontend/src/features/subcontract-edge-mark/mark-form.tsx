import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildSubcontractEdgeMarkWrite,
  saveSubcontractEdgeMark,
} from "@/lib/subcontract-edge-marks-api"

const EDGES = [
  { value: "prime", label: "prime — główny" },
  { value: "sub", label: "sub — podwykonawca" },
  { value: "broker", label: "broker" },
  { value: "other", label: "other" },
] as const

export function SubcontractEdgeMarkEditor(args: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("prime_01")
  const [edge, setEdge] = useState("prime")
  const [origin, setOrigin] = useState("fixture://subcontract-edge-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveSubcontractEdgeMark(
        buildSubcontractEdgeMarkWrite({ code, kind: edge, origin }),
      ),
    onSuccess: () => {
      setCode("prime_01")
      setEdge("prime")
      setOrigin("fixture://subcontract-edge-mark/")
      void qc.invalidateQueries({ queryKey: ["subcontract-edge-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-md gap-3"
      data-subcontract-edge-mark="editor"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rola w łańcuchu podwykonawstwa jako etykieta HITL. Bez grafu live.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika subcontract edge"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        edge_kind
        <select
          aria-label="Rodzaj krawędzi subcontract"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(e) => setEdge(e.target.value)}
          value={edge}
        >
          {EDGES.map((row) => (
            <option key={row.value} value={row.value}>
              {row.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://subcontract-edge-mark/…)"
        ariaLabel="Pochodzenie znacznika subcontract edge"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz subcontract edge
      </Button>
    </form>
  )
}
