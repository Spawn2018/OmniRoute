import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createOceanAllianceMark,
  makeOceanAllianceMarkPayload,
} from "@/lib/ocean-alliance-marks-api"

const OPTIONS = [
  { value: "alliance", label: "Alliance" },
  { value: "feeder", label: "Feeder" },
  { value: "slot", label: "Slot" },
  { value: "other", label: "Inne" },
] as const

export function OceanAllianceMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("oa_manual_01")
  const [kind, setKind] = useState("alliance")
  const [ref, setRef] = useState("fixture://ocean-alliance-mark/")
  const mutation = useMutation({
    mutationFn: () =>
      createOceanAllianceMark(makeOceanAllianceMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("oa_manual_01")
      setKind("alliance")
      setRef("fixture://ocean-alliance-mark/")
      void qc.invalidateQueries({
        queryKey: ["ocean-alliance-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="grid gap-3 rounded-md border border-cyan-900/25 bg-background p-3 md:grid-cols-2"
      data-oa="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <div className="md:col-span-2">
        <p className="text-sm font-semibold">Nowy znacznik ocean</p>
        <p className="text-[11px] text-muted-foreground">HITL — bez live API i scrape.</p>
      </div>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code ocean alliance"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        ocean_kind
        <select
          aria-label="ocean_kind ocean alliance"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <div className="md:col-span-2">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref ocean alliance"
          value={ref}
          onChange={setRef}
        />
      </div>
      {mutation.error ? (
        <div className="md:col-span-2">
          <CatalogError error={mutation.error} />
        </div>
      ) : null}
      <div className="md:col-span-2">
        <Button disabled={!props.organizationId || mutation.isPending} type="submit">
          Zapisz ocean alliance
        </Button>
      </div>
    </form>
  )
}
