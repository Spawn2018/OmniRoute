import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createOutcomeLedger,
  makeOutcomeLedgerPayload,
} from "@/lib/outcome-ledgers-api"

const EXAMPLE_ENTITY = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
const EXAMPLE_SUGGESTION = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"

export function OutcomeLedgerComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [targetBc, setTargetBc] = useState("shipment")
  const [entityId, setEntityId] = useState(EXAMPLE_ENTITY)
  const [suggestionId, setSuggestionId] = useState(EXAMPLE_SUGGESTION)
  const [kind, setKind] = useState("eta")
  const [actualValue, setActualValue] = useState("45")
  const [ref, setRef] = useState("fixture://outcome-ledger/")
  const save = useMutation({
    mutationFn: () =>
      createOutcomeLedger(
        makeOutcomeLedgerPayload({
          targetBc,
          entityId,
          suggestionId,
          kind,
          actualValue,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://outcome-ledger/")
      void qc.invalidateQueries({
        queryKey: ["outcome-ledgers", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-outcome-ledger="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        target_bc
        <input
          aria-label="target_bc outcome ledger"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setTargetBc(e.target.value)}
          required
          value={targetBc}
        />
      </label>
      <label className="text-xs">
        entity_id
        <input
          aria-label="entity_id UUID"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setEntityId(e.target.value)}
          required
          value={entityId}
        />
      </label>
      <label className="text-xs">
        suggestion_id
        <input
          aria-label="suggestion_id UUID"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setSuggestionId(e.target.value)}
          required
          value={suggestionId}
        />
      </label>
      <label className="text-xs">
        outcome_kind
        <input
          aria-label="outcome_kind open dict"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setKind(e.target.value)}
          required
          value={kind}
        />
      </label>
      <label className="text-xs">
        actual_value
        <input
          aria-label="actual_value decimal"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setActualValue(e.target.value)}
          required
          value={actualValue}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref outcome ledger"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz ledger wyniku
      </Button>
    </form>
  )
}
