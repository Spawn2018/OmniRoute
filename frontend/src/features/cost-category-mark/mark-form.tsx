import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCostCategoryMarkWrite, saveCostCategoryMark } from "@/lib/cost-category-marks-api"

const CATEGORY_OPTIONS = [
  { value: "direct", label: "direct — bezpośredni" },
  { value: "shared", label: "shared — wspólny" },
  { value: "allocated", label: "allocated — alokowany" },
  { value: "overhead", label: "overhead — narzut" },
  { value: "capital", label: "capital — kapitałowy" },
  { value: "risk", label: "risk — ryzyko" },
  { value: "other", label: "other — inny" },
] as const

export function CostCategoryMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("direct_01")
  const [categoryKind, setCategoryKind] = useState("direct")
  const [sourceRef, setSourceRef] = useState("fixture://cost-category-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveCostCategoryMark(
        buildCostCategoryMarkWrite({ code: markCode, kind: categoryKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("direct_01")
      setCategoryKind("direct")
      setSourceRef("fixture://cost-category-mark/")
      void cache.invalidateQueries({ queryKey: ["cost-category-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-cost-category-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog HITL kategorii kosztu PDF §13j. `category_kind` to etykieta operatora — nie silnik
        allocation SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod znacznika (snake 2–32)
        <input
          aria-label="Kod znacznika cost category"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>Rodzaj kategorii (`category_kind`)</legend>
        {CATEGORY_OPTIONS.map((option) => (
          <label key={option.value} className="flex gap-2">
            <input
              checked={categoryKind === option.value}
              name="category-kind"
              onChange={() => setCategoryKind(option.value)}
              type="radio"
              value={option.value}
            />
            {option.label}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://cost-category-mark/…)"
        ariaLabel="Pochodzenie znacznika cost category"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz cost category
      </Button>
    </form>
  )
}
