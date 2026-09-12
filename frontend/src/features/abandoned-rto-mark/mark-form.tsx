import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createAbandonedRtoMark,
  makeAbandonedRtoPayload,
} from "@/lib/abandoned-rto-marks-api"

const FATES = [
  { value: "abandoned", note: "porzucony cargo" },
  { value: "rto", note: "return to origin" },
  { value: "return", note: "zwrot" },
  { value: "other", note: "inne" },
] as const

const CODE0 = "aro_manual_01"
const REF0 = "fixture://abandoned-rto-mark/"

export function AbandonedRtoComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [markCode, setMarkCode] = useState(CODE0)
  const [fateKind, setFateKind] = useState("abandoned")
  const [sourceRef, setSourceRef] = useState(REF0)
  const create = useMutation({
    mutationFn: () =>
      createAbandonedRtoMark(makeAbandonedRtoPayload(markCode, fateKind, sourceRef)),
    onSuccess: () => {
      setMarkCode(CODE0)
      setFateKind("abandoned")
      setSourceRef(REF0)
      void client.invalidateQueries({
        queryKey: ["abandoned-rto-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="rounded-md border border-amber-700/30 bg-background p-3 shadow-sm">
      <form
        className="grid gap-2"
        data-aro="intake"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) create.mutate()
        }}
      >
        <p className="text-sm font-medium">Nowy los abandoned/RTO</p>
        <p className="text-[11px] text-muted-foreground">
          Tylko HITL — zakaz abandoned live i RTO scrape.
        </p>
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code abandoned"
            className="mt-1 h-8 w-full rounded border px-2 font-mono text-sm"
            onChange={(event) => setMarkCode(event.target.value)}
            required
            value={markCode}
          />
        </label>
        <label className="text-xs">
          fate_kind
          <select
            aria-label="fate_kind abandoned"
            className="mt-1 h-8 w-full rounded border px-2 text-sm"
            onChange={(event) => setFateKind(event.target.value)}
            value={fateKind}
          >
            {FATES.map((row) => (
              <option key={row.value} value={row.value}>
                {row.value} — {row.note}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref abandoned"
          value={sourceRef}
          onChange={setSourceRef}
        />
        {create.error ? <CatalogError error={create.error} /> : null}
        <Button disabled={!props.organizationId || create.isPending} type="submit">
          Zapisz los
        </Button>
      </form>
    </div>
  )
}
