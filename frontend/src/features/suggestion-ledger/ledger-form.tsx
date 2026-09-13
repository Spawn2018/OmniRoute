import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createSuggestionLedger,
  makeSuggestionLedgerPayload,
} from "@/lib/suggestion-ledgers-api"

const KINDS = [
  { value: "eta", label: "ETA" },
  { value: "rate", label: "Stawka" },
  { value: "route", label: "Trasa" },
  { value: "other", label: "Inne" },
] as const

const REACTIONS = [
  { value: "accept", label: "Accept" },
  { value: "modify", label: "Modify" },
  { value: "reject", label: "Reject" },
] as const

const EXAMPLE_ENTITY = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"

export function SuggestionLedgerComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [targetBc, setTargetBc] = useState("shipment")
  const [entityId, setEntityId] = useState(EXAMPLE_ENTITY)
  const [kind, setKind] = useState("eta")
  const [intervalLow, setIntervalLow] = useState("30")
  const [intervalHigh, setIntervalHigh] = useState("90")
  const [modelVersion, setModelVersion] = useState("hist_eta")
  const [promptVersion, setPromptVersion] = useState("prompt_v1")
  const [reaction, setReaction] = useState("accept")
  const [changedTo, setChangedTo] = useState("none")
  const [ref, setRef] = useState("fixture://suggestion-ledger/")
  const save = useMutation({
    mutationFn: () =>
      createSuggestionLedger(
        makeSuggestionLedgerPayload({
          targetBc,
          entityId,
          kind,
          intervalLow,
          intervalHigh,
          modelVersion,
          promptVersion,
          reaction,
          changedTo,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setChangedTo("none")
      setReaction("accept")
      setRef("fixture://suggestion-ledger/")
      void qc.invalidateQueries({
        queryKey: ["suggestion-ledgers", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-suggestion-ledger="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        target_bc
        <input
          aria-label="target_bc suggestion ledger"
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
        suggestion_kind
        <select
          aria-label="suggestion_kind eta rate route other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <label className="text-xs">
        interval_low
        <input
          aria-label="interval_low decimal"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setIntervalLow(e.target.value)}
          required
          value={intervalLow}
        />
      </label>
      <label className="text-xs">
        interval_high
        <input
          aria-label="interval_high decimal"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setIntervalHigh(e.target.value)}
          required
          value={intervalHigh}
        />
      </label>
      <label className="text-xs">
        model_version
        <input
          aria-label="model_version"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setModelVersion(e.target.value)}
          required
          value={modelVersion}
        />
      </label>
      <label className="text-xs">
        prompt_version
        <input
          aria-label="prompt_version"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setPromptVersion(e.target.value)}
          required
          value={promptVersion}
        />
      </label>
      <label className="text-xs">
        reaction
        <select
          aria-label="reaction accept modify reject"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setReaction(e.target.value)}
          value={reaction}
        >
          {REACTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <label className="text-xs">
        changed_to
        <input
          aria-label="changed_to none or text"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setChangedTo(e.target.value)}
          required
          value={changedTo}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref suggestion ledger"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz ledger podpowiedzi
      </Button>
    </form>
  )
}
