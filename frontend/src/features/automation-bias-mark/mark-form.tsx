import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildAutomationBiasMarkWrite,
  saveAutomationBiasMark,
} from "@/lib/automation-bias-marks-api"

const BIAS_KINDS = [
  { value: "confirm", label: "Potwierdzenie (confirm)" },
  { value: "delay", label: "Opóźnienie (delay)" },
  { value: "review", label: "Ponowny przegląd (review)" },
  { value: "other", label: "Inne" },
] as const

export function AutomationBiasMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ab_confirm_01")
  const [kind, setKind] = useState("confirm")
  const [origin, setOrigin] = useState("fixture://automation-bias/")
  const save = useMutation({
    mutationFn: () =>
      saveAutomationBiasMark(buildAutomationBiasMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("ab_confirm_01")
      setKind("confirm")
      setOrigin("fixture://automation-bias/")
      void cache.invalidateQueries({
        queryKey: ["automation-bias-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3 rounded-md border border-slate-600/25 bg-slate-50/30 p-3 dark:bg-slate-950/20"
      data-automation-bias-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL stancji mitygacji automation bias (confirm/delay/review). Przebudowa ui-04,
        scoring osoby i auto-accept zostają poza tym katalogiem.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika automation bias"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Rodzaj mitygacji
        <select
          aria-label="Rodzaj mitygacji confirm delay review other"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          {BIAS_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://automation-bias/…)"
        ariaLabel="Pochodzenie znacznika automation bias"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik bias
      </Button>
    </form>
  )
}
