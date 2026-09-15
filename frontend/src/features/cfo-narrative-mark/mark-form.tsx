import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildCfoNarrativeMarkWrite,
  saveCfoNarrativeMark,
} from "@/lib/cfo-narrative-marks-api"

export function CfoNarrativeMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("cfo_anomaly_01")
  const [kind, setKind] = useState("anomaly")
  const [origin, setOrigin] = useState("fixture://cfo-narrative-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveCfoNarrativeMark(buildCfoNarrativeMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("cfo_anomaly_01")
      setKind("anomaly")
      setOrigin("fixture://cfo-narrative-mark/")
      void cache.invalidateQueries({
        queryKey: ["cfo-narrative-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-cfo-narrative-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL etykiety narracji CFO (anomaly/story/summary). Silnik narracji i
        druga marza zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://cfo-narrative-mark/…)"
        ariaLabel="Pochodzenie znacznika narracji CFO"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika narracji CFO"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj narracji</span>
        <select
          aria-label="Rodzaj narracji anomaly story summary other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="anomaly">anomaly — anomalia</option>
          <option value="story">story — opowiesc</option>
          <option value="summary">summary — podsumowanie</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz etykiete narracji CFO
      </Button>
    </form>
  )
}
