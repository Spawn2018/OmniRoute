import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createCabotageMark, toCabotagePayload } from "@/lib/cabotage-marks-api"

const KINDS = [
  ["counter", "licznik"],
  ["driver_return", "powrót kierowcy"],
  ["vehicle_return", "powrót pojazdu"],
  ["other", "inny"],
] as const

export function CabotageMarkForm(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("counter_01")
  const [kind, setKind] = useState<string>("counter")
  const [ref, setRef] = useState("fixture://cabotage-mark/")
  const write = useMutation({
    mutationFn: () => createCabotageMark(toCabotagePayload(code, kind, ref)),
    onSuccess: () => {
      setCode("counter_01")
      setKind("counter")
      setRef("fixture://cabotage-mark/")
      void client.invalidateQueries({ queryKey: ["cabotage-marks", props.organizationId] })
    },
  })

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    write.mutate()
  }

  return (
    <form
      className="flex max-w-2xl flex-col gap-2 border-b pb-4"
      data-cabotage="form"
      onSubmit={handleSubmit}
    >
      <h2 className="text-sm font-semibold tracking-wide">Znacznik kabotażu</h2>
      <p className="text-xs text-muted-foreground">
        HITL: licznik / powrót kierowcy / powrót pojazdu. Bez silnika RTPD i bez tacho.
      </p>
      <div className="flex flex-wrap items-end gap-3">
        <label className="grid min-w-[10rem] flex-1 gap-1 text-xs">
          Kod znacznika
          <input
            aria-label="Kod znacznika kabotażu"
            className="h-9 rounded-md border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid min-w-[12rem] gap-1 text-xs">
          Rodzaj
          <select
            aria-label="Rodzaj kabotażu"
            className="h-9 rounded-md border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {KINDS.map(([id, label]) => (
              <option key={id} value={id}>
                {id} — {label}
              </option>
            ))}
          </select>
        </label>
        <Button
          className="h-9"
          disabled={!props.organizationId || write.isPending}
          type="submit"
        >
          Zapisz kabotaż
        </Button>
      </div>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie kabotażu"
        value={ref}
        onChange={setRef}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
    </form>
  )
}
