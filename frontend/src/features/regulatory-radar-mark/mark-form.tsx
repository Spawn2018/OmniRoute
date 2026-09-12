import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createRegulatoryRadarMark,
  makeRegulatoryRadarPayload,
} from "@/lib/regulatory-radar-marks-api"

const RADAR_KINDS = [
  { key: "notice", tip: "ogloszenie" },
  { key: "deadline", tip: "termin" },
  { key: "watch", tip: "obserwacja" },
  { key: "other", tip: "inny" },
] as const

export function RegulatoryRadarComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("rr_notice_01")
  const [kind, setKind] = useState("notice")
  const [ref, setRef] = useState("fixture://regulatory-radar-mark/")
  const write = useMutation({
    mutationFn: () =>
      createRegulatoryRadarMark(makeRegulatoryRadarPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("rr_notice_01")
      setKind("notice")
      setRef("fixture://regulatory-radar-mark/")
      void client.invalidateQueries({
        queryKey: ["regulatory-radar-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="border border-dashed p-4" data-rr="composer">
      <h2 className="text-sm font-semibold">Znacznik regulatory radar (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Tryb radaru regulacyjnego. Bez scrape urzedow i bez live feed.
      </p>
      <form
        className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) write.mutate()
        }}
      >
        <label className="text-xs lg:col-span-1">
          mark_code
          <input
            aria-label="mark_code radara"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          radar_kind
          <select
            aria-label="radar_kind"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {RADAR_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="text-xs sm:col-span-2 lg:col-span-2">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref radara"
            value={ref}
            onChange={setRef}
          />
        </div>
        {write.error ? (
          <div className="sm:col-span-2 lg:col-span-4">
            <CatalogError error={write.error} />
          </div>
        ) : null}
        <Button
          className="sm:col-span-2 lg:col-span-4"
          disabled={!props.organizationId || write.isPending}
          type="submit"
        >
          Zapisz znacznik radara
        </Button>
      </form>
    </div>
  )
}
