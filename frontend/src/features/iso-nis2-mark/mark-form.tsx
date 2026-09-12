import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createIsoNis2Mark,
  makeIsoNis2Payload,
} from "@/lib/iso-nis2-marks-api"

const OPS_KINDS = [
  { key: "iso", tip: "ISO" },
  { key: "nis2", tip: "NIS2" },
  { key: "policy", tip: "polityka" },
  { key: "other", tip: "inny" },
] as const

export function IsoNis2Composer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("iso_nis2_01")
  const [kind, setKind] = useState("iso")
  const [ref, setRef] = useState("fixture://iso-nis2-mark/")
  const save = useMutation({
    mutationFn: () => createIsoNis2Mark(makeIsoNis2Payload(code, kind, ref)),
    onSuccess: () => {
      setCode("iso_nis2_01")
      setKind("iso")
      setRef("fixture://iso-nis2-mark/")
      void client.invalidateQueries({
        queryKey: ["iso-nis2-marks", props.organizationId],
      })
    },
  })

  return (
    <section className="rounded border p-3" data-iso="composer">
      <h2 className="text-sm font-semibold">Znacznik ISO/NIS2 (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Ops compliance. Bez audytu live i bez certyfikatu HTTP.
      </p>
      <form
        className="flex flex-col gap-2 md:flex-row md:flex-wrap md:items-end"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="min-w-[10rem] flex-1 text-xs">
          mark_code
          <input
            aria-label="mark_code ISO"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="min-w-[8rem] text-xs">
          ops_kind
          <select
            aria-label="ops_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {OPS_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="min-w-[12rem] flex-1 text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref ISO"
            value={ref}
            onChange={setRef}
          />
        </div>
        {save.error ? <div className="w-full"><CatalogError error={save.error} /></div> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik ISO/NIS2
        </Button>
      </form>
    </section>
  )
}
