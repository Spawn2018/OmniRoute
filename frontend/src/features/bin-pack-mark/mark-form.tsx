import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { packBinPackWrite, saveBinPackMark } from "@/lib/bin-pack-marks-api"

const KINDS = [
  { id: "volume", label: "objętość" },
  { id: "weight", label: "masa" },
  { id: "mixed", label: "mieszany" },
  { id: "other", label: "inny" },
] as const

export function BinPackEntry(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("pack_vol_01")
  const [kind, setKind] = useState("volume")
  const [ref, setRef] = useState("fixture://bin-pack-mark/")
  const save = useMutation({
    mutationFn: () => saveBinPackMark(packBinPackWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("pack_vol_01")
      setKind("volume")
      setRef("fixture://bin-pack-mark/")
      void qc.invalidateQueries({ queryKey: ["bin-pack-marks", props.organizationId] })
    },
  })

  function submit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    save.mutate()
  }

  return (
    <div className="rounded-md bg-secondary/30 p-4" data-bin-pack="entry">
      <form className="flex flex-col gap-3 sm:max-w-md" onSubmit={submit}>
        <header>
          <h2 className="text-sm font-semibold">Znacznik bin-pack</h2>
          <p className="text-xs text-muted-foreground">
            HITL: objętość / masa / mieszany. Bez OR-Tools i bez LLM-VRP (patrz load_plan_mark).
          </p>
        </header>
        <label className="grid gap-1 text-xs">
          Kod
          <input
            aria-label="Kod znacznika bin-pack"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid gap-1 text-xs">
          Rodzaj (`pack_kind`)
          <select
            aria-label="Rodzaj pack_kind"
            className="h-9 rounded-md border bg-background px-2"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {KINDS.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id} — {row.label}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="Pochodzenie znacznika bin-pack"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik bin-pack
        </Button>
      </form>
    </div>
  )
}
