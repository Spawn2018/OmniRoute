import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createDemandSnapshotMark,
  makeDemandSnapshotMarkPayload,
} from "@/lib/demand-snapshot-marks-api"

const KINDS = [
  { value: "forecast", note: "prognoza" },
  { value: "booking", note: "booking" },
  { value: "actual", note: "rzeczywisty" },
  { value: "other", note: "inne" },
] as const

const CODE0 = "dsm_manual_01"
const REF0 = "fixture://demand-snapshot-mark/"

export function DemandSnapshotMarkComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [markCode, setMarkCode] = useState(CODE0)
  const [snapshotKind, setSnapshotKind] = useState("forecast")
  const [sourceRef, setSourceRef] = useState(REF0)
  const save = useMutation({
    mutationFn: () =>
      createDemandSnapshotMark(
        makeDemandSnapshotMarkPayload(markCode, snapshotKind, sourceRef),
      ),
    onSuccess: () => {
      setMarkCode(CODE0)
      setSnapshotKind("forecast")
      setSourceRef(REF0)
      void client.invalidateQueries({
        queryKey: ["demand-snapshot-marks", props.organizationId],
      })
    },
  })

  return (
    <aside className="border border-sky-800/30 bg-background p-3">
      <form
        className="grid gap-2 sm:grid-cols-2"
        data-dsm="form"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <div className="sm:col-span-2 space-y-1">
          <p className="text-sm font-semibold">Nowy znacznik snapshot</p>
          <p className="text-[11px] text-muted-foreground">
            HITL only — zakaz demand SQL i auto-forecast.
          </p>
        </div>
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code demand snapshot"
            className="mt-1 h-8 w-full rounded border px-2 font-mono text-sm"
            onChange={(event) => setMarkCode(event.target.value)}
            required
            value={markCode}
          />
        </label>
        <label className="text-xs">
          snapshot_kind
          <select
            aria-label="snapshot_kind demand snapshot"
            className="mt-1 h-8 w-full rounded border px-2 text-sm"
            onChange={(event) => setSnapshotKind(event.target.value)}
            value={snapshotKind}
          >
            {KINDS.map((row) => (
              <option key={row.value} value={row.value}>
                {row.value} — {row.note}
              </option>
            ))}
          </select>
        </label>
        <div className="sm:col-span-2">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref demand snapshot"
            value={sourceRef}
            onChange={setSourceRef}
          />
        </div>
        {save.error ? (
          <div className="sm:col-span-2">
            <CatalogError error={save.error} />
          </div>
        ) : null}
        <div className="sm:col-span-2">
          <Button disabled={!props.organizationId || save.isPending} type="submit">
            Zapisz znacznik snapshot
          </Button>
        </div>
      </form>
    </aside>
  )
}
