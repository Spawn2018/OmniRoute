import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildQualityDescentMarkWrite,
  saveQualityDescentMark,
} from "@/lib/quality-descent-marks-api"

export function QualityDescentMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("qd_mae_01")
  const [kind, setKind] = useState("mae")
  const [origin, setOrigin] = useState("fixture://quality-descent/")
  const save = useMutation({
    mutationFn: () =>
      saveQualityDescentMark(buildQualityDescentMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("qd_mae_01")
      setKind("mae")
      setOrigin("fixture://quality-descent/")
      void cache.invalidateQueries({
        queryKey: ["quality-descent-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-md flex-col gap-3 border border-dashed border-slate-700/50 p-4"
      data-quality-descent-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL powodu zejścia jakości (MAE / CRPS / Brier / ręcznie). Silnik auto-zejścia,
        L3 write i wyliczanie metryk zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://quality-descent/…)"
        ariaLabel="Pochodzenie powodu zejścia jakości"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika zejścia jakości"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Powód zejścia jakości</span>
        <select
          aria-label="Rodzaj zejścia mae crps brier manual other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="mae">mae — MAE</option>
          <option value="crps">crps — CRPS</option>
          <option value="brier">brier — Brier</option>
          <option value="manual">manual — ręcznie</option>
          <option value="other">other — pozostałe</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz powód zejścia
      </Button>
    </form>
  )
}
