import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildImpactEdgeMarkWrite, saveImpactEdgeMark } from "@/lib/impact-edge-marks-api"

const KIND_OPTIONS = [
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

export function ImpactEdgeMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("ship_to_inv")
  const [fromKind, setFromKind] = useState("shipment")
  const [toKind, setToKind] = useState("inventory")
  const [sourceRef, setSourceRef] = useState("fixture://impact-edge-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveImpactEdgeMark(
        buildImpactEdgeMarkWrite({
          code: markCode,
          fromKind,
          toKind,
          origin: sourceRef,
        }),
      ),
    onSuccess: () => {
      setMarkCode("ship_to_inv")
      setFromKind("shipment")
      setToKind("inventory")
      setSourceRef("fixture://impact-edge-mark/")
      void cache.invalidateQueries({ queryKey: ["impact-edge-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-impact-edge-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog HITL krawedzi kaskady AI6. `from_kind` / `to_kind` to etykiety operatora —
        nie FK wezla, nie SQL grafu ani EBITDA.
      </p>
      <label className="grid gap-1 text-xs">
        Kod znacznika (snake 2–32)
        <input
          aria-label="Kod znacznika impact edge"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>Od (`from_kind`)</legend>
        {KIND_OPTIONS.map((option) => (
          <label key={`from-${option.value}`} className="flex gap-2">
            <input
              checked={fromKind === option.value}
              name="from_kind"
              onChange={() => setFromKind(option.value)}
              type="radio"
              value={option.value}
            />
            {option.label}
          </label>
        ))}
      </fieldset>
      <fieldset className="grid gap-1 text-xs">
        <legend>Do (`to_kind`)</legend>
        {KIND_OPTIONS.map((option) => (
          <label key={`to-${option.value}`} className="flex gap-2">
            <input
              checked={toKind === option.value}
              name="to_kind"
              onChange={() => setToKind(option.value)}
              type="radio"
              value={option.value}
            />
            {option.label}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        ariaLabel="source_ref impact edge"
        label="source_ref"
        onChange={setSourceRef}
        value={sourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz krawedz skutku
      </Button>
    </form>
  )
}
