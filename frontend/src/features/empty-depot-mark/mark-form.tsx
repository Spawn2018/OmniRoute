import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createEmptyDepotMark,
  makeEmptyDepotMarkPayload,
} from "@/lib/empty-depot-marks-api"

const OPTIONS = [
  { value: "empty", label: "Empty" },
  { value: "depot", label: "Depot" },
  { value: "chassis", label: "Chassis" },
  { value: "other", label: "Inne" },
] as const

export function EmptyDepotMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("ed_manual_01")
  const [kind, setKind] = useState("empty")
  const [ref, setRef] = useState("fixture://empty-depot-mark/")
  const mutation = useMutation({
    mutationFn: () =>
      createEmptyDepotMark(makeEmptyDepotMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ed_manual_01")
      setKind("empty")
      setRef("fixture://empty-depot-mark/")
      void qc.invalidateQueries({
        queryKey: ["empty-depot-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="grid gap-3 rounded-md border border-stone-800/30 bg-background p-3 sm:grid-cols-2"
      data-ed="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <div className="sm:col-span-2">
        <p className="text-sm font-semibold">Nowy znacznik depot</p>
        <p className="text-[11px] text-muted-foreground">HITL — bez live API i scrape.</p>
      </div>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code empty depot"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        depot_kind
        <select
          aria-label="depot_kind empty depot"
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
      <div className="sm:col-span-2">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref empty depot"
          value={ref}
          onChange={setRef}
        />
      </div>
      {mutation.error ? (
        <div className="sm:col-span-2">
          <CatalogError error={mutation.error} />
        </div>
      ) : null}
      <div className="sm:col-span-2">
        <Button disabled={!props.organizationId || mutation.isPending} type="submit">
          Zapisz empty/depot
        </Button>
      </div>
    </form>
  )
}
