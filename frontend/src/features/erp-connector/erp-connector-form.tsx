import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { erpConnectorWrite, persistErpConnector } from "@/lib/erp-connectors-api"

type ErpConnectorDraft = {
  codeStamp: string
  kindStamp: string
  originStamp: string
}

const EMPTY_ERP: ErpConnectorDraft = {
  codeStamp: "optima_biuro",
  kindStamp: "optima",
  originStamp: "fixture://optima/",
}

export function ErpConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_ERP)
  const persist = useMutation({
    mutationFn: () => persistErpConnector(erpConnectorWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_ERP })
      void cache.invalidateQueries({ queryKey: ["erp-connectors", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-erp-connector="erp-connector-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Konektor Comarch Optima jako dane: kod i kind `optima`. Serwis nie woła SOAP
        ani WebAPI. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod konektora (snake 2–32)
        <input
          aria-label="Kod konektora Optima"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        System (optima)
        <input
          aria-label="Kind systemu ERP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://optima/…)"
        ariaLabel="Pochodzenie konektora Optima"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz konektor Optima
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
