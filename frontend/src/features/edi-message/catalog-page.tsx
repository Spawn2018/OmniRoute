import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { createEdiMessage, fetchEdiMessages } from "@/lib/edi-messages-api"
import { getTenantContext } from "@/lib/tenant"

function MessageRecordForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [shipmentId, setShipmentId] = useState("")
  const [messageKind, setMessageKind] = useState("noted")
  const [sourceRef, setSourceRef] = useState("fixture://edi-message/")
  const save = useMutation({
    mutationFn: () =>
      createEdiMessage({
        shipment_id: shipmentId.trim(),
        message_kind: messageKind.trim(),
        source_ref: sourceRef.trim(),
      }),
    onSuccess: () => {
      setShipmentId("")
      void client.invalidateQueries({
        queryKey: ["edi-messages", args.organizationId],
      })
    },
  })
  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        save.mutate()
      }}
    >
      <Input aria-label="Identyfikator zlecenia" placeholder="shipment_id" value={shipmentId} onChange={(event) => setShipmentId(event.target.value)} required />
      <Input aria-label="Rodzaj komunikatu" placeholder="noted" value={messageKind} onChange={(event) => setMessageKind(event.target.value)} required />
      <Input aria-label="Pochodzenie zapisu" placeholder="source_ref" value={sourceRef} onChange={(event) => setSourceRef(event.target.value)} required />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz komunikat
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function EdiMessagePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const messages = useQuery({
    queryKey: ["edi-messages", ctx.organizationId],
    queryFn: fetchEdiMessages,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-edi-message="board">
      <CatalogHeading
        title="EDI"
        subtitle="edi_message M-39 · tabela na zleceniu · nie parser · nie live sieć"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {messages.isError ? <CatalogError error={messages.error} /> : null}
      <MessageRecordForm organizationId={ctx.organizationId} />
      {(messages.data ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          {row.message_kind} {row.source_ref}{" "}
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}
