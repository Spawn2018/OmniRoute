import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createSidImportMark,
  makeSidImportPayload,
} from "@/lib/sid-import-marks-api"

const SID_KINDS = [
  { key: "sid", tip: "pojedynczy SID" },
  { key: "batch", tip: "paczka SID" },
  { key: "manual", tip: "ręczny wpis" },
  { key: "other", tip: "inny" },
] as const

export function SidImportComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("sid_batch_01")
  const [kind, setKind] = useState("sid")
  const [ref, setRef] = useState("fixture://sid-import-mark/")
  const write = useMutation({
    mutationFn: () =>
      createSidImportMark(makeSidImportPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("sid_batch_01")
      setKind("sid")
      setRef("fixture://sid-import-mark/")
      void client.invalidateQueries({
        queryKey: ["sid-import-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="rounded border border-dashed p-3" data-sid="composer">
      <h2 className="text-sm font-semibold">Import SID (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Znacznik trybu importu. Bez SID HTTP i bez ICS2.
      </p>
      <form
        className="grid gap-2 sm:grid-cols-2"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) write.mutate()
        }}
      >
        <label className="text-xs sm:col-span-2">
          mark_code
          <input
            aria-label="mark_code SID"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          sid_kind
          <select
            aria-label="sid_kind"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {SID_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref SID"
            value={ref}
            onChange={setRef}
          />
        </div>
        {write.error ? (
          <div className="sm:col-span-2">
            <CatalogError error={write.error} />
          </div>
        ) : null}
        <Button
          className="sm:col-span-2"
          disabled={!props.organizationId || write.isPending}
          type="submit"
        >
          Zapisz znacznik SID
        </Button>
      </form>
    </div>
  )
}
