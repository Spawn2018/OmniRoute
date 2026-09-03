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
import { createShipmentDocument, fetchShipmentDocuments } from "@/lib/shipment-documents-api"
import { getTenantContext } from "@/lib/tenant"

function DocumentRecordForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [shipmentId, setShipmentId] = useState("")
  const [documentKind, setDocumentKind] = useState("noted")
  const [sourceRef, setSourceRef] = useState("fixture://shipment-document/")
  const save = useMutation({
    mutationFn: () =>
      createShipmentDocument({
        shipment_id: shipmentId.trim(),
        document_kind: documentKind.trim(),
        source_ref: sourceRef.trim(),
      }),
    onSuccess: () => {
      setShipmentId("")
      void client.invalidateQueries({ queryKey: ["shipment-documents", args.organizationId] })
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
      <Input aria-label="Rodzaj dokumentu" placeholder="noted" value={documentKind} onChange={(event) => setDocumentKind(event.target.value)} required />
      <Input aria-label="Pochodzenie zapisu" placeholder="source_ref" value={sourceRef} onChange={(event) => setSourceRef(event.target.value)} required />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz dokument
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function ShipmentDocumentPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const documents = useQuery({
    queryKey: ["shipment-documents", ctx.organizationId],
    queryFn: fetchShipmentDocuments,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-shipment-document="board">
      <CatalogHeading
        title="Dokumenty zlecenia"
        subtitle="shipment_document M-38 · tabela na zleceniu · nie PDF · nie HBL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {documents.isError ? <CatalogError error={documents.error} /> : null}
      <DocumentRecordForm organizationId={ctx.organizationId} />
      {(documents.data ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          {row.document_kind} {row.source_ref}{" "}
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}
