import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createPhytoAtaMark, makePhytoAtaPayload } from "@/lib/phyto-ata-marks-api"

const PERMITS: ReadonlyArray<{ code: string; caption: string }> = [
  { code: "phyto", caption: "fitosanitarne" },
  { code: "ata", caption: "carnet ATA" },
  { code: "plant", caption: "roslinne" },
  { code: "other", caption: "inne" },
]

const DEFAULT_CODE = "phyto_desk_01"
const DEFAULT_REF = "fixture://phyto-ata-mark/"

export function PhytoAtaComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [markCode, setMarkCode] = useState(DEFAULT_CODE)
  const [permitKind, setPermitKind] = useState("phyto")
  const [sourceRef, setSourceRef] = useState(DEFAULT_REF)
  const create = useMutation({
    mutationFn: () =>
      createPhytoAtaMark(makePhytoAtaPayload(markCode, permitKind, sourceRef)),
    onSuccess: () => {
      setMarkCode(DEFAULT_CODE)
      setPermitKind("phyto")
      setSourceRef(DEFAULT_REF)
      void client.invalidateQueries({
        queryKey: ["phyto-ata-marks", props.organizationId],
      })
    },
  })

  return (
    <aside className="rounded-xl bg-emerald-950/5 p-4 ring-1 ring-emerald-800/20">
      <form
        className="flex flex-wrap items-end gap-3"
        data-phyto="intake"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) create.mutate()
        }}
      >
        <div className="min-w-[12rem] flex-1 space-y-1">
          <p className="text-sm font-semibold tracking-tight">Wpis phyto/ATA</p>
          <p className="text-[11px] text-muted-foreground">
            Tylko HITL — bez phyto live i bez ATA scrape.
          </p>
        </div>
        <label className="min-w-[10rem] flex-1 text-[11px]">
          mark_code
          <input
            aria-label="mark_code phyto"
            className="mt-1 block h-9 w-full rounded-md border px-2 font-mono text-sm"
            onChange={(event) => setMarkCode(event.target.value)}
            required
            value={markCode}
          />
        </label>
        <label className="min-w-[10rem] flex-1 text-[11px]">
          permit_kind
          <select
            aria-label="permit_kind phyto"
            className="mt-1 block h-9 w-full rounded-md border px-2 text-sm"
            onChange={(event) => setPermitKind(event.target.value)}
            value={permitKind}
          >
            {PERMITS.map((row) => (
              <option key={row.code} value={row.code}>
                {row.code} — {row.caption}
              </option>
            ))}
          </select>
        </label>
        <div className="min-w-[14rem] flex-[2]">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref phyto"
            value={sourceRef}
            onChange={setSourceRef}
          />
        </div>
        {create.error ? <CatalogError error={create.error} /> : null}
        <Button disabled={!props.organizationId || create.isPending} type="submit">
          Zapisz pozwolenie
        </Button>
      </form>
    </aside>
  )
}
