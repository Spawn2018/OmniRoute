import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createBidDecisionMark,
  makeBidDecisionMarkPayload,
} from "@/lib/bid-decision-marks-api"

const DECISION_KINDS = [
  { value: "go", label: "Go" },
  { value: "no_go", label: "No-go" },
  { value: "hold", label: "Hold" },
  { value: "other", label: "Inne" },
] as const

export function BidDecisionMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("bdm_go_main")
  const [kind, setKind] = useState("go")
  const [ref, setRef] = useState("fixture://bid-decision-mark/")
  const save = useMutation({
    mutationFn: () =>
      createBidDecisionMark(makeBidDecisionMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("bdm_go_main")
      setKind("go")
      setRef("fixture://bid-decision-mark/")
      void qc.invalidateQueries({
        queryKey: ["bid-decision-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-bdm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code bid decision"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        decision_kind
        <select
          aria-label="decision_kind go no_go hold other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {DECISION_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref bid decision"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik bid decision
      </Button>
    </form>
  )
}
