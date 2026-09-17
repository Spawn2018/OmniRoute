import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildShipmentMonitoringFilingWrite,
  saveShipmentMonitoringFiling,
} from "@/lib/shipment-monitoring-filings-api"

const KINDS = ["open", "filed", "closed", "other"] as const

export function ShipmentMonitoringFilingSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("filing_01")
  const [kind, setKind] = useState<string>("open")
  const [origin, setOrigin] = useState("fixture://shipment-monitoring-filing/")
  const save = useMutation({
    mutationFn: () =>
      saveShipmentMonitoringFiling(buildShipmentMonitoringFilingWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("filing_01")
      setKind("open")
      setOrigin("fixture://shipment-monitoring-filing/")
      void cache.invalidateQueries({
        queryKey: ["shipment-monitoring-filings", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-shipment-monitoring-filing="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja zgloszenia SENT/BDO (open/filed/closed) jako katalog HITL. Rodzaj to dana, nie
        live PUESC i nie XML SENT.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika zgloszenia SENT/BDO"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Status zgloszenia</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="shipment-monitoring-status"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://shipment-monitoring-filing/…)"
        ariaLabel="Pochodzenie znacznika zgloszenia SENT/BDO"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz zgloszenie
      </Button>
    </form>
  )
}
