import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  fetchFieldCarryForwards,
  fieldCarryForwardBody,
  saveFieldCarryForwards,
} from "@/lib/field-carry-forwards-api"
import type { Quotation } from "@/lib/quotations-api"
import { fetchShipments, type Shipment } from "@/lib/shipments-api"
import { getTenantContext } from "@/lib/tenant"

export function CarryForwardPanel(args: { rows: Quotation[]; signedIn: boolean }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [quotationId, setQuotationId] = useState("")
  const [shipmentId, setShipmentId] = useState("")
  const selected = args.rows.find((row) => row.id === quotationId)
  const shipsQuery = useQuery({
    queryKey: ["shipments-picker", ctx.organizationId],
    queryFn: fetchShipments,
    enabled: args.signedIn,
    retry: false,
  })
  const carryQuery = useQuery({
    queryKey: ["field-carry-forwards", ctx.organizationId, shipmentId],
    queryFn: () => fetchFieldCarryForwards(shipmentId),
    enabled: args.signedIn && shipmentId !== "",
    retry: false,
  })
  const mutation = useMutation({
    mutationFn: () => {
      if (selected === undefined) {
        return Promise.reject(new Error("Wybierz wycenę"))
      }
      return saveFieldCarryForwards(
        fieldCarryForwardBody({
          quotationId,
          shipmentId,
          incoterm: selected.incoterm,
          tradeSide: selected.trade_side,
          namedPlace: selected.named_place,
        }),
      )
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["field-carry-forwards", ctx.organizationId, shipmentId],
      })
    },
  })
  const ships = shipsForQuote(shipsQuery.data ?? [], quotationId)
  const current = (carryQuery.data ?? []).filter((row) => row.superseded_by === null)
  return (
    <section className="space-y-2 rounded-md border border-border bg-card p-3" data-carry-forward="job">
      <p className="text-sm font-medium">Przeniesienie pól na zlecenie</p>
      <p className="text-xs text-muted-foreground">
        Snapshot Incoterms. Zmiana to nowy wiersz, nie cichy overwrite.
      </p>
      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <label className="flex flex-col gap-1 text-xs">
          quotation_id
          <select
            aria-label="Wycena do przeniesienia"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={quotationId}
            onChange={(event) => {
              setQuotationId(event.target.value)
              setShipmentId("")
            }}
          >
            <option value="">Wycena</option>
            {args.rows.map((row) => (
              <option key={row.id} value={row.id}>
                {row.incoterm ?? "bez Incoterms"} · {row.id}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          shipment_id
          <select
            aria-label="Zlecenie docelowe"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={shipmentId}
            onChange={(event) => setShipmentId(event.target.value)}
          >
            <option value="">Zlecenie</option>
            {ships.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id}
              </option>
            ))}
          </select>
        </label>
        <Button
          type="button"
          disabled={!args.signedIn || quotationId === "" || shipmentId === "" || mutation.isPending}
          onClick={() => mutation.mutate()}
        >
          Przenieś pola
        </Button>
      </div>
      {mutation.isError ? (
        <p className="text-sm text-destructive">{(mutation.error as Error).message}</p>
      ) : null}
      {current.length > 0 ? (
        <ul className="font-mono text-xs">
          {current.map((row) => (
            <li key={row.id}>
              {row.field_key}={row.field_value}
            </li>
          ))}
        </ul>
      ) : null}
    </section>
  )
}

function shipsForQuote(rows: readonly Shipment[], quotationId: string): Shipment[] {
  if (quotationId === "") return []
  return rows.filter((row) => row.quotation_id === quotationId)
}
