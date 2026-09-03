import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { createEdiMessage, fetchEdiMessages } from "@/lib/edi-messages-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_DRAFT = {
  shipmentId: "",
  messageKind: "noted",
  sourceRef: "fixture://edi-message/",
}

function MessageRecordForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_DRAFT)
  const save = useMutation({
    mutationFn: () =>
      createEdiMessage({
        shipment_id: draft.shipmentId.trim(),
        message_kind: draft.messageKind.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...EMPTY_DRAFT })
      void client.invalidateQueries({ queryKey: ["edi-messages", args.organizationId] })
    },
  })
  return (
    <form
      className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-4"
      onSubmit={(event) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <Input
        aria-label="Identyfikator zlecenia"
        placeholder="shipment_id"
        value={draft.shipmentId}
        onChange={(event) => setDraft({ ...draft, shipmentId: event.target.value })}
        required
      />
      <Input
        aria-label="Rodzaj komunikatu"
        placeholder="noted"
        value={draft.messageKind}
        onChange={(event) => setDraft({ ...draft, messageKind: event.target.value })}
        required
      />
      <Input
        aria-label="Pochodzenie zapisu"
        placeholder="source_ref"
        value={draft.sourceRef}
        onChange={(event) => setDraft({ ...draft, sourceRef: event.target.value })}
        required
      />
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
        <p key={row.id} className="font-mono text-xs">
          {row.message_kind} · {row.source_ref}{" "}
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}
