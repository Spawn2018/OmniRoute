import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  bookingInstructionBody,
  fetchBookingInstructions,
  saveBookingInstruction,
} from "@/lib/booking-instructions-api"
import { getTenantContext } from "@/lib/tenant"

const SCOPE_TOKENS = ["precarriage", "ocean", "oncarriage", "contact_exchange", "none"] as const
const ROLE_TOKENS = [
  "shipper",
  "consignee",
  "origin_agent",
  "dest_agent",
  "ocean_carrier",
  "omni_customs",
  "client_customs",
] as const
const STATUS_TOKENS = ["suggested", "accepted", "sent", "confirmed", "rejected"] as const

function tokenColumn(
  group: string,
  current: string,
  tokens: readonly string[],
  onPick: (token: string) => void,
) {
  return (
    <div className="flex flex-col gap-1 text-xs" role="radiogroup" aria-label={group}>
      {tokens.map((token) => (
        <label key={`${group}-${token}`} className="flex items-center gap-2">
          <input
            type="radio"
            name={group}
            value={token}
            checked={current === token}
            onChange={() => onPick(token)}
          />
          {token}
        </label>
      ))}
    </div>
  )
}

function useInstructionJob(signedIn: boolean) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [shipmentId, setShipmentId] = useState("")
  const [bookingScope, setBookingScope] = useState("contact_exchange")
  const [targetRole, setTargetRole] = useState("origin_agent")
  const [status, setStatus] = useState("suggested")
  const listQuery = useQuery({
    queryKey: ["booking-instructions", ctx.organizationId, shipmentId],
    queryFn: () => fetchBookingInstructions(shipmentId),
    enabled: signedIn && shipmentId !== "",
    retry: false,
  })
  const mutation = useMutation({
    mutationFn: () =>
      saveBookingInstruction(
        bookingInstructionBody({ shipmentId, bookingScope, targetRole, status }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["booking-instructions", ctx.organizationId, shipmentId],
      })
    },
  })
  return {
    shipmentId,
    setShipmentId,
    bookingScope,
    setBookingScope,
    targetRole,
    setTargetRole,
    status,
    setStatus,
    mutation,
    rows: listQuery.data ?? [],
  }
}

export function BookingInstructionPanel(args: { signedIn: boolean }) {
  const job = useInstructionJob(args.signedIn)
  return (
    <section className="space-y-2 rounded-md border border-border bg-card p-3" data-booking-instruction="job">
      <p className="text-sm font-medium">Instrukcja bookingu</p>
      <p className="text-xs text-muted-foreground">
        Zakres z I1 i rola ze zlecenia. Status to dana. Nie HTTP armatora.
      </p>
      <Input
        aria-label="Identyfikator zlecenia instrukcji"
        placeholder="shipment_id"
        value={job.shipmentId}
        onChange={(event) => job.setShipmentId(event.target.value)}
      />
      {tokenColumn("zakres bookingu", job.bookingScope, SCOPE_TOKENS, job.setBookingScope)}
      {tokenColumn("rola celu bookingu", job.targetRole, ROLE_TOKENS, job.setTargetRole)}
      {tokenColumn("status instrukcji", job.status, STATUS_TOKENS, job.setStatus)}
      <Button
        type="button"
        disabled={!args.signedIn || job.shipmentId === "" || job.mutation.isPending}
        onClick={() => job.mutation.mutate()}
      >
        Zapisz instrukcję
      </Button>
      {job.mutation.isError ? (
        <p className="text-sm text-destructive">{(job.mutation.error as Error).message}</p>
      ) : null}
      <ul className="space-y-1">
        {job.rows.map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.booking_scope} {row.target_role} {row.status}
          </li>
        ))}
      </ul>
    </section>
  )
}
