import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistSapConnector, sapConnectorBody } from "@/lib/sap-connectors-api"

type Draft = {
  connectorSlug: string
  systemKind: string
  originPointer: string
}

const EMPTY: Draft = {
  connectorSlug: "sap_pl_01",
  systemKind: "sap",
  originPointer: "fixture://sap-connector/",
}

export function SapConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY)
  const persist = useMutation({
    mutationFn: () => persistSapConnector(sapConnectorBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY })
      void cache.invalidateQueries({ queryKey: ["sap-connectors", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-sap-connector="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Konektor SAP/Oracle jako katalog. To nie jest live SOAP ani SQL do systemu klienta.
      </p>
      <label className="grid gap-1 text-xs">
        Kod konektora (snake 2–32)
        <input
          aria-label="Kod konektora SAP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, connectorSlug: change.target.value })}
          required
          value={draft.connectorSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        System (sap / oracle)
        <select
          aria-label="System SAP lub Oracle"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, systemKind: change.target.value })}
          value={draft.systemKind}
        >
          <option value="sap">sap</option>
          <option value="oracle">oracle</option>
        </select>
      </label>
      <label className="grid gap-1 text-xs">
        Pochodzenie (source_ref)
        <input
          aria-label="Pochodzenie konektora SAP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, originPointer: change.target.value })}
          required
          value={draft.originPointer}
        />
      </label>
      {persist.error ? <CatalogError error={persist.error} /> : null}
      <Button disabled={!args.organizationId || persist.isPending} type="submit">
        Zapisz konektor SAP/Oracle
      </Button>
    </form>
  )
}
