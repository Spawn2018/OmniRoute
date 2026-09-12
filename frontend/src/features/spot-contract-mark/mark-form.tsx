import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createSpotContractMark,
  makeSpotContractMarkPayload,
} from "@/lib/spot-contract-marks-api"

const DEAL_KINDS = [
  { value: "spot", label: "Spot" },
  { value: "contract", label: "Contract" },
  { value: "other", label: "Inne" },
] as const

export function SpotContractMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("scm_spot_main")
  const [kind, setKind] = useState("spot")
  const [ref, setRef] = useState("fixture://spot-contract-mark/")
  const save = useMutation({
    mutationFn: () =>
      createSpotContractMark(makeSpotContractMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("scm_spot_main")
      setKind("spot")
      setRef("fixture://spot-contract-mark/")
      void qc.invalidateQueries({
        queryKey: ["spot-contract-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-scm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code spot contract"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        deal_kind
        <select
          aria-label="deal_kind spot contract other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {DEAL_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref spot contract"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik spot/contract
      </Button>
    </form>
  )
}
