import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createOceanFeederMark,
  makeOceanFeederMarkPayload,
} from "@/lib/ocean-feeder-marks-api"

const FEEDER_KINDS = [
  { value: "feeder", label: "Feeder" },
  { value: "short_sea", label: "Short-sea" },
  { value: "other", label: "Inne" },
] as const

export function OceanFeederMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("ofm_feeder_01")
  const [kind, setKind] = useState("feeder")
  const [ref, setRef] = useState("fixture://ocean-feeder-mark/")
  const save = useMutation({
    mutationFn: () =>
      createOceanFeederMark(makeOceanFeederMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ofm_feeder_01")
      setKind("feeder")
      setRef("fixture://ocean-feeder-mark/")
      void qc.invalidateQueries({
        queryKey: ["ocean-feeder-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-ofm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code ocean-feeder"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        feeder_kind
        <select
          aria-label="feeder_kind feeder short_sea"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {FEEDER_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref ocean-feeder"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik feeder/short-sea
      </Button>
    </form>
  )
}
