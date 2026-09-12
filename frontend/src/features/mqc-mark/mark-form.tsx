import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createMqcMark, makeMqcPayload } from "@/lib/mqc-marks-api"

const KINDS = [
  { id: "mqc", label: "kontrakt" },
  { id: "actual", label: "wykonanie" },
  { id: "gap", label: "odchylenie" },
  { id: "other", label: "inne" },
] as const

export function MqcComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("mqc_act_01")
  const [kind, setKind] = useState("mqc")
  const [ref, setRef] = useState("fixture://mqc-mark/")
  const mut = useMutation({
    mutationFn: () => createMqcMark(makeMqcPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("mqc_act_01")
      setKind("mqc")
      setRef("fixture://mqc-mark/")
      void qc.invalidateQueries({ queryKey: ["mqc-marks", props.organizationId] })
    },
  })
  return (
    <section className="bg-muted/30 p-3" data-mqc="form">
      <h2 className="mb-1 text-sm font-semibold">MQC vs actual (HITL)</h2>
      <p className="mb-2 text-xs text-muted-foreground">Bez MQC SQL i bez qty float.</p>
      <form
        className="flex flex-wrap items-end gap-2"
        onSubmit={(e: FormEvent) => {
          e.preventDefault()
          if (props.organizationId) mut.mutate()
        }}
      >
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code MQC"
            className="mt-1 block h-8 w-40 rounded border px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          mqc_kind
          <select
            aria-label="mqc_kind"
            className="mt-1 block h-8 rounded border px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {KINDS.map((k) => (
              <option key={k.id} value={k.id}>
                {k.id} / {k.label}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref MQC"
          value={ref}
          onChange={setRef}
        />
        {mut.error ? <CatalogError error={mut.error} /> : null}
        <Button disabled={!props.organizationId || mut.isPending} type="submit">
          Zapisz znacznik MQC
        </Button>
      </form>
    </section>
  )
}
