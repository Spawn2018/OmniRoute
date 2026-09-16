import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildHandoverSbarMarkWrite,
  saveHandoverSbarMark,
} from "@/lib/handover-sbar-marks-api"

export function HandoverSbarMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("sbar_sit_01")
  const [kind, setKind] = useState("situation")
  const [origin, setOrigin] = useState("fixture://handover-sbar-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveHandoverSbarMark(buildHandoverSbarMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("sbar_sit_01")
      setKind("situation")
      setOrigin("fixture://handover-sbar-mark/")
      void cache.invalidateQueries({
        queryKey: ["handover-sbar-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-handover-sbar-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL znacznika przekazania zmiany (situation/background/assessment/recommendation/other).
        Notatka z czterema polami tekstu i auto SBAR zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://handover-sbar-mark/…)"
        ariaLabel="Pochodzenie znacznika SBAR"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika SBAR"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj SBAR</span>
        <select
          aria-label="Rodzaj SBAR situation background assessment recommendation other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="situation">situation — sytuacja</option>
          <option value="background">background — tlo</option>
          <option value="assessment">assessment — ocena</option>
          <option value="recommendation">recommendation — rekomendacja</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik SBAR
      </Button>
    </form>
  )
}
