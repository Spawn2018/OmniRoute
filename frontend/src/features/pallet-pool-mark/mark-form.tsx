import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { packPalletPoolWrite, savePalletPoolMark } from "@/lib/pallet-pool-marks-api"

const KINDS = [
  { id: "chep", label: "Chep" },
  { id: "lpr", label: "LPR" },
  { id: "epal", label: "EPAL" },
  { id: "other", label: "inna pula" },
] as const

export function PalletPoolEntry(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("pool_chep_01")
  const [kind, setKind] = useState("chep")
  const [ref, setRef] = useState("fixture://pallet-pool-mark/")
  const save = useMutation({
    mutationFn: () => savePalletPoolMark(packPalletPoolWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("pool_chep_01")
      setKind("chep")
      setRef("fixture://pallet-pool-mark/")
      void qc.invalidateQueries({ queryKey: ["pallet-pool-marks", props.organizationId] })
    },
  })

  function submit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    save.mutate()
  }

  return (
    <div className="rounded-md bg-secondary/30 p-4" data-pallet-pool="entry">
      <form className="flex flex-col gap-3 sm:max-w-md" onSubmit={submit}>
        <header>
          <h2 className="text-sm font-semibold">Znacznik puli palet</h2>
          <p className="text-xs text-muted-foreground">
            HITL: Chep / LPR / EPAL. Bez giełdy i bez salda sztuk (patrz pallet_balance).
          </p>
        </header>
        <label className="grid gap-1 text-xs">
          Kod
          <input
            aria-label="Kod znacznika puli palet"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid gap-1 text-xs">
          Rodzaj (`pool_kind`)
          <select
            aria-label="Rodzaj pool_kind"
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
          ariaLabel="Pochodzenie znacznika puli"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik puli
        </Button>
      </form>
    </div>
  )
}
