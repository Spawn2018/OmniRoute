import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  fetchShipmentStakeholders,
  saveShipmentStakeholder,
  shipmentStakeholderBody,
} from "@/lib/shipment-stakeholders-api"
import type { Shipment } from "@/lib/shipments-api"
import { getTenantContext } from "@/lib/tenant"

const ROLES = [
  "shipper",
  "consignee",
  "origin_agent",
  "dest_agent",
  "ocean_carrier",
  "omni_customs",
  "client_customs",
] as const

export function ShipmentStakeholderPanel(args: { rows: Shipment[]; signedIn: boolean }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const firstId = args.rows[0]?.id ?? ""
  const [shipmentId, setShipmentId] = useState(firstId)
  const [partyId, setPartyId] = useState("")
  const [role, setRole] = useState("shipper")
  const chosen = shipmentId || firstId
  const listQuery = useQuery({
    queryKey: ["shipment-stakeholders", ctx.organizationId, chosen],
    queryFn: () => fetchShipmentStakeholders(chosen),
    enabled: args.signedIn && chosen !== "",
    retry: false,
  })
  const mutation = useMutation({
    mutationFn: () =>
      saveShipmentStakeholder(
        shipmentStakeholderBody({ shipmentId: chosen, partyId, role }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["shipment-stakeholders", ctx.organizationId, chosen],
      })
    },
  })
  return (
    <section className="space-y-2 rounded-md border border-border bg-card p-3" data-shipment-stakeholder="job">
      <p className="text-sm font-medium">Strony zlecenia</p>
      <p className="text-xs text-muted-foreground">Rola z karty I2. party_id obowiązkowe. Nie kolumny korpo EXP1.</p>
      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <label className="flex flex-col gap-1 text-xs">
          zlecenie
          <select
            aria-label="Zlecenie strony"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={chosen}
            onChange={(event) => setShipmentId(event.target.value)}
          >
            {args.rows.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          rola
          <select
            aria-label="Rola strony zlecenia"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={role}
            onChange={(event) => setRole(event.target.value)}
          >
            {ROLES.map((token) => (
              <option key={token} value={token}>
                {token}
              </option>
            ))}
          </select>
        </label>
        <Input
          aria-label="Identyfikator kontrahenta strony"
          placeholder="party_id"
          value={partyId}
          onChange={(event) => setPartyId(event.target.value)}
        />
        <Button
          type="button"
          disabled={!args.signedIn || chosen === "" || mutation.isPending}
          onClick={() => mutation.mutate()}
        >
          Zapisz stronę
        </Button>
      </div>
      {mutation.isError ? (
        <p className="text-sm text-destructive">{(mutation.error as Error).message}</p>
      ) : null}
      {(listQuery.data ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.role} {row.party_id}
        </p>
      ))}
    </section>
  )
}
