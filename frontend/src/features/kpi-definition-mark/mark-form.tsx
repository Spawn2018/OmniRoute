import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildKpiDefinitionMarkWrite,
  saveKpiDefinitionMark,
} from "@/lib/kpi-definition-marks-api"

export function KpiDefinitionMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("kpi_otd_01")
  const [kind, setKind] = useState("otd")
  const [origin, setOrigin] = useState("fixture://kpi-definition-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveKpiDefinitionMark(buildKpiDefinitionMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("kpi_otd_01")
      setKind("otd")
      setOrigin("fixture://kpi-definition-mark/")
      void cache.invalidateQueries({
        queryKey: ["kpi-definition-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-kpi-definition-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL definicji KPI (otd/otif/custom). Wzór KPI i
        OTIF% SQL zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://kpi-definition-mark/…)"
        ariaLabel="Pochodzenie znacznika definicji KPI"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika definicji KPI"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj KPI</span>
        <select
          aria-label="Rodzaj KPI otd otif custom other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="otd">otd — on-time delivery</option>
          <option value="otif">otif — on-time in-full</option>
          <option value="custom">custom — wlasny KPI</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz definicje KPI
      </Button>
    </form>
  )
}
