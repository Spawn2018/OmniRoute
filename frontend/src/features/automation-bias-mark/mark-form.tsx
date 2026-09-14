import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildAutomationBiasMarkWrite,
  saveAutomationBiasMark,
} from "@/lib/automation-bias-marks-api"

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
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
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
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://automation-bias/…)"
        ariaLabel="Pochodzenie znacznika automation bias"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika automation bias"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Stancja mitygacji bias</span>
        <select
          aria-label="Rodzaj mitygacji confirm delay review other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="confirm">confirm — potwierdzenie</option>
          <option value="delay">delay — opóźnienie decyzji</option>
          <option value="review">review — ponowny przegląd</option>
          <option value="other">other — pozostałe</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stancję automation bias
      </Button>
    </form>
  )
}
