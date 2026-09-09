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
  const [seal, setSeal] = useState("")
  const [seal2, setSeal2] = useState("")
  const [seal3, setSeal3] = useState("")
  const [vessel, setVessel] = useState("")
  const [voyage, setVoyage] = useState("")
  const listed = useQuery({
    queryKey: ["containers", ctx.organizationId, sizeType],
    queryFn: () => fetchContainers(sizeType),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () =>
      saveContainer(
        containerWrite({ number, sizeType, shipment, seal, seal2, seal3, vessel, voyage }),
      ),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["containers", ctx.organizationId, sizeType] })
    },
  })
  const blocked = !args.signedIn || number.trim() === "" || persist.isPending
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-container="iso">
      <h2 className="text-sm font-medium">Kontener ISO</h2>
      <p className="text-xs text-muted-foreground">
        Numer z cyfrą kontrolną i typ 4 znaków. Opcjonalne plomby, statek i rejs. Nie VGM. Nie PIN. Nie booking.
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
      <label className="flex flex-col gap-1 text-xs">
        Pierwsza plomba (opcjonalnie)
        <Input
          aria-label="Pierwsza plomba kontenera"
          placeholder="seal_no_1"
          value={seal}
          onChange={(event) => setSeal(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Druga plomba (opcjonalnie)
        <Input
          aria-label="Druga plomba kontenera"
          placeholder="seal_no_2"
          value={seal2}
          onChange={(event) => setSeal2(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Trzecia plomba (opcjonalnie)
        <Input
          aria-label="Trzecia plomba kontenera"
          placeholder="seal_no_3"
          value={seal3}
          onChange={(event) => setSeal3(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Statek (opcjonalnie)
        <Input
          aria-label="Nazwa statku kontenera"
          placeholder="vessel_name"
          value={vessel}
          onChange={(event) => setVessel(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rejs (opcjonalnie)
        <Input
          aria-label="Numer rejsu kontenera"
          placeholder="voyage_no"
          value={voyage}
          onChange={(event) => setVoyage(event.target.value)}
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
            {row.seal_no_1 !== null ? ` · ${row.seal_no_1}` : ""}
            {row.seal_no_2 !== null ? ` · ${row.seal_no_2}` : ""}
            {row.seal_no_3 !== null ? ` · ${row.seal_no_3}` : ""}
            {row.vessel_name !== null ? ` · ${row.vessel_name}` : ""}
            {row.voyage_no !== null ? ` · ${row.voyage_no}` : ""}
          </li>
        ))}
      </ul>
    </section>
  )
}
