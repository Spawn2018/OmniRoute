import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildModelFeatureMarkWrite,
  saveModelFeatureMark,
} from "@/lib/model-feature-marks-api"

export function ModelFeatureMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("mf_numeric_01")
  const [kind, setKind] = useState("numeric")
  const [origin, setOrigin] = useState("fixture://model-feature-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveModelFeatureMark(buildModelFeatureMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("mf_numeric_01")
      setKind("numeric")
      setOrigin("fixture://model-feature-mark/")
      void cache.invalidateQueries({
        queryKey: ["model-feature-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-model-feature-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL etykiety cechy modelu (numeric/categorical/derived). Live train
        zostaje poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://model-feature-mark/…)"
        ariaLabel="Pochodzenie znacznika cechy modelu"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika cechy modelu"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj cechy</span>
        <select
          aria-label="Rodzaj cechy numeric categorical derived other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="numeric">numeric — liczba</option>
          <option value="categorical">categorical — kategoria</option>
          <option value="derived">derived — wyprowadzona</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz etykiete cechy modelu
      </Button>
    </form>
  )
}
