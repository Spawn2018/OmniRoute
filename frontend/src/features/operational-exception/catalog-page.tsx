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
import {
  createOperationalException,
  fetchOperationalExceptions,
} from "@/lib/operational-exceptions-api"
import { getTenantContext } from "@/lib/tenant"

function ExceptionRecordForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [shipmentId, setShipmentId] = useState("")
  const [exceptionKind, setExceptionKind] = useState("noted")
  const [sourceRef, setSourceRef] = useState("fixture://operational-exception/")
  const save = useMutation({
    mutationFn: () =>
      createOperationalException({
        shipment_id: shipmentId.trim(),
        exception_kind: exceptionKind.trim(),
        source_ref: sourceRef.trim(),
      }),
    onSuccess: () => {
      setShipmentId("")
      void client.invalidateQueries({
        queryKey: ["operational-exceptions", args.organizationId],
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
      <Input aria-label="Rodzaj wyjątku" placeholder="noted" value={exceptionKind} onChange={(event) => setExceptionKind(event.target.value)} required />
      <Input aria-label="Pochodzenie zapisu" placeholder="source_ref" value={sourceRef} onChange={(event) => setSourceRef(event.target.value)} required />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz wyjątek
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function OperationalExceptionPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const exceptions = useQuery({
    queryKey: ["operational-exceptions", ctx.organizationId],
    queryFn: fetchOperationalExceptions,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-operational-exception="board">
      <CatalogHeading
        title="Wyjątki"
        subtitle="operational_exception M-37 · tabela na zleceniu · nie AIS · nie mapa"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {exceptions.isError ? <CatalogError error={exceptions.error} /> : null}
      <ExceptionRecordForm organizationId={ctx.organizationId} />
      {(exceptions.data ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          {row.exception_kind} {row.source_ref}{" "}
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}
