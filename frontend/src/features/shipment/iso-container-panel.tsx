import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { containerWrite, fetchContainers, saveContainer } from "@/lib/containers-api"
import { getTenantContext } from "@/lib/tenant"

export function IsoContainerPanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const cache = useQueryClient()
  const [number, setNumber] = useState("")
  const [sizeType, setSizeType] = useState("22G1")
  const [shipment, setShipment] = useState("")
  const listed = useQuery({
    queryKey: ["containers", ctx.organizationId, sizeType],
    queryFn: () => fetchContainers(sizeType),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () => saveContainer(containerWrite({ number, sizeType, shipment })),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["containers", ctx.organizationId, sizeType] })
    },
  })
  const blocked = !args.signedIn || number.trim() === "" || persist.isPending
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-container="iso">
      <h2 className="text-sm font-medium">Kontener ISO</h2>
      <p className="text-xs text-muted-foreground">
        Numer z cyfrą kontrolną i typ 4 znaków. Nie VGM. Nie booking.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Numer ISO 6346
        <Input
          aria-label="Numer kontenera ISO"
          placeholder="container_no"
          value={number}
          onChange={(event) => setNumber(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Typ ISO (iso_size_type)
        <Input
          aria-label="Typ ISO kontenera"
          placeholder="iso_size_type"
          value={sizeType}
          onChange={(event) => setSizeType(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Zlecenie (opcjonalnie)
        <Input
          aria-label="Identyfikator zlecenia kontenera"
          placeholder="shipment_id"
          value={shipment}
          onChange={(event) => setShipment(event.target.value)}
        />
      </label>
      <Button type="button" disabled={blocked} onClick={() => persist.mutate()}>
        Zapisz kontener
      </Button>
      {persist.isError ? (
        <p className="text-sm text-destructive">{(persist.error as Error).message}</p>
      ) : null}
      <ul className="space-y-1">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.container_no} · {row.iso_size_type}
          </li>
        ))}
      </ul>
    </section>
  )
}
