import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createVdaOdetteMark,
  makeVdaOdettePayload,
} from "@/lib/vda-odette-marks-api"

const EDI_KINDS = [
  { key: "vda", tip: "VDA" },
  { key: "odette", tip: "Odette" },
  { key: "label", tip: "etykieta" },
  { key: "other", tip: "inny" },
] as const

export function VdaOdetteComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("vo_vda_01")
  const [kind, setKind] = useState("vda")
  const [ref, setRef] = useState("fixture://vda-odette-mark/")
  const save = useMutation({
    mutationFn: () =>
      createVdaOdetteMark(makeVdaOdettePayload(code, kind, ref)),
    onSuccess: () => {
      setCode("vo_vda_01")
      setKind("vda")
      setRef("fixture://vda-odette-mark/")
      void client.invalidateQueries({
        queryKey: ["vda-odette-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="border-b pb-4" data-vo="composer">
      <h2 className="text-sm font-semibold">Znacznik VDA/Odette (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Standard EDI. Bez live EDI VDA i bez etykiety ZPL.
      </p>
      <form
        className="grid gap-2 md:grid-cols-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code VDA"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          edi_kind
          <select
            aria-label="edi_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {EDI_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref VDA"
            value={ref}
            onChange={setRef}
          />
        </div>
        {save.error ? (
          <div className="md:col-span-3">
            <CatalogError error={save.error} />
          </div>
        ) : null}
        <Button
          className="md:col-span-3"
          disabled={!props.organizationId || save.isPending}
          type="submit"
        >
          Zapisz znacznik VDA/Odette
        </Button>
      </form>
    </div>
  )
}
