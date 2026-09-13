import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  factoringConnectorWrite,
  persistFactoringConnector,
} from "@/lib/factoring-connectors-api"

type FactoringConnectorDraft = {
  codeStamp: string
  kindStamp: string
  originStamp: string
}

const KIND_OPTIONS = [
  { value: "smeo", label: "SMEO (partner osi Trade-Tech)" },
  { value: "other", label: "Inny partner (HITL)" },
] as const

const EMPTY_FACTORING: FactoringConnectorDraft = {
  codeStamp: "smeo_trade",
  kindStamp: "smeo",
  originStamp: "fixture://smeo/",
}

export function FactoringConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_FACTORING)
  const persist = useMutation({
    mutationFn: () => persistFactoringConnector(factoringConnectorWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_FACTORING })
      void cache.invalidateQueries({ queryKey: ["factoring-connectors", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-factoring-connector="factoring-connector-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog partnera faktoringowego jako dane: kod i kind SMEO albo other. Serwis nie woła
        live HTTP SMEO. Wypłata zostaje w leftover F7.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod konektora (snake 2–32)
        <input
          aria-label="Kod konektora faktoringu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Partner (system_kind)
        <select
          aria-label="Kind partnera faktoringowego"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        >
          {KIND_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://smeo/…)"
        ariaLabel="Pochodzenie konektora faktoringu"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz konektor faktoringu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
