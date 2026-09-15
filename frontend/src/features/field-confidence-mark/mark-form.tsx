import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildFieldConfidenceMarkWrite,
  saveFieldConfidenceMark,
} from "@/lib/field-confidence-marks-api"

export function FieldConfidenceMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("fc_green_01")
  const [kind, setKind] = useState("green")
  const [origin, setOrigin] = useState("fixture://field-confidence/")
  const save = useMutation({
    mutationFn: () =>
      saveFieldConfidenceMark(buildFieldConfidenceMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("fc_green_01")
      setKind("green")
      setOrigin("fixture://field-confidence/")
      void cache.invalidateQueries({
        queryKey: ["field-confidence-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-md flex-col gap-3 border border-dashed border-slate-700/50 p-4"
      data-field-confidence-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL pasma pewności per pole (green / yellow / orange / hold). Przebudowa
        ui-04, float confidence i auto-accept zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://field-confidence/…)"
        ariaLabel="Pochodzenie pasma pewności per pole"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika pewności per pole"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Pasmo pewności</span>
        <select
          aria-label="Pasmo green yellow orange hold other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="green">green — ≥0,85</option>
          <option value="yellow">yellow — 0,70–0,85</option>
          <option value="orange">orange — poniżej 0,70</option>
          <option value="hold">hold — wstrzymaj</option>
          <option value="other">other — pozostałe</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz pasmo
      </Button>
    </form>
  )
}
