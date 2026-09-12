import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { packECmrWrite, saveECmrMark } from "@/lib/e-cmr-marks-api"

const KINDS = [
  { id: "ecmr", label: "e-CMR" },
  { id: "efti", label: "eFTI" },
  { id: "paper", label: "papier" },
  { id: "other", label: "inny" },
] as const

export function ECmrEntry(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("ecmr_01")
  const [kind, setKind] = useState("ecmr")
  const [ref, setRef] = useState("fixture://e-cmr-mark/")
  const save = useMutation({
    mutationFn: () => saveECmrMark(packECmrWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("ecmr_01")
      setKind("ecmr")
      setRef("fixture://e-cmr-mark/")
      void qc.invalidateQueries({ queryKey: ["e-cmr-marks", props.organizationId] })
    },
  })

  function submit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    save.mutate()
  }

  return (
    <div className="rounded-md bg-secondary/30 p-4" data-e-cmr="entry">
      <form className="flex flex-col gap-3 sm:max-w-md" onSubmit={submit}>
        <header>
          <h2 className="text-sm font-semibold">Znacznik e-CMR / eFTI</h2>
          <p className="text-xs text-muted-foreground">
            HITL: e-CMR / eFTI / papier. Bez filera live (patrz filing_scheme_mark).
          </p>
        </header>
        <label className="grid gap-1 text-xs">
          Kod
          <input
            aria-label="Kod znacznika e-CMR"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid gap-1 text-xs">
          Rodzaj (`cmr_kind`)
          <select
            aria-label="Rodzaj cmr_kind"
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
          ariaLabel="Pochodzenie znacznika e-CMR"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik e-CMR
        </Button>
      </form>
    </div>
  )
}
