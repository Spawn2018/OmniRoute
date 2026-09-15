import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildImpactNodeMarkWrite, saveImpactNodeMark } from "@/lib/impact-node-marks-api"

const NODE_OPTIONS = [
  { value: "shipment", label: "shipment — zlecenie" },
  { value: "inventory", label: "inventory — zapas" },
  { value: "sku", label: "sku — SKU" },
  { value: "line", label: "line — linia produkcji" },
  { value: "order", label: "order — zamowienie klienta" },
  { value: "revenue", label: "revenue — przychod" },
  { value: "margin", label: "margin — marza (etykieta)" },
  { value: "cash", label: "cash — gotowka" },
  { value: "other", label: "other — inny" },
] as const

export function ImpactNodeMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("shipment_01")
  const [nodeKind, setNodeKind] = useState("shipment")
  const [sourceRef, setSourceRef] = useState("fixture://impact-node-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveImpactNodeMark(
        buildImpactNodeMarkWrite({ code: markCode, kind: nodeKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("shipment_01")
      setNodeKind("shipment")
      setSourceRef("fixture://impact-node-mark/")
      void cache.invalidateQueries({ queryKey: ["impact-node-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-impact-node-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog HITL wezla kaskady AI6. `node_kind` to etykieta operatora — nie silnik SQL
        ani EBITDA.
      </p>
      <label className="grid gap-1 text-xs">
        Kod znacznika (snake 2–32)
        <input
          aria-label="Kod znacznika impact node"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>Rodzaj wezla (`node_kind`)</legend>
        {NODE_OPTIONS.map((option) => (
          <label key={option.value} className="flex gap-2">
            <input
              checked={nodeKind === option.value}
              name="node_kind"
              onChange={() => setNodeKind(option.value)}
              type="radio"
              value={option.value}
            />
            {option.label}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        ariaLabel="source_ref impact node"
        label="source_ref"
        onChange={setSourceRef}
        value={sourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz wezel skutku
      </Button>
    </form>
  )
}
