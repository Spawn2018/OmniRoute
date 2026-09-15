import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildIngestGateMarkWrite,
  saveIngestGateMark,
} from "@/lib/ingest-gate-marks-api"

export function IngestGateMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ig_truth_01")
  const [kind, setKind] = useState("truth")
  const [origin, setOrigin] = useState("fixture://ingest-gate-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveIngestGateMark(buildIngestGateMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("ig_truth_01")
      setKind("truth")
      setOrigin("fixture://ingest-gate-mark/")
      void cache.invalidateQueries({
        queryKey: ["ingest-gate-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-ingest-gate-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL bramy ingest (truth/owner/exception). Live ingest i 22 dostepy bez
        bramy zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://ingest-gate-mark/…)"
        ariaLabel="Pochodzenie znacznika brama ingest"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika brama ingest"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj etykiety</span>
        <select
          aria-label="Rodzaj etykiety truth owner exception other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="truth">truth — zrodlo prawdy</option>
          <option value="owner">owner — wlasciciel</option>
          <option value="exception">exception — wyjatek</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz etykiete brama ingest
      </Button>
    </form>
  )
}
