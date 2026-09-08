import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listShipmentLegs, saveShipmentLeg } from "@/lib/shipment-legs-api"

type AirDraft = {
  shipmentId: string
  originId: string
  destId: string
  sourceRef: string
}

const EMPTY_AIR: AirDraft = {
  shipmentId: "",
  originId: "",
  destId: "",
  sourceRef: "fixture://shipment-leg/",
}

function persistAir(draft: AirDraft) {
  return saveShipmentLeg({
    leg_kind: "air",
    shipment_id: draft.shipmentId.trim(),
    origin_location_id: draft.originId.trim(),
    destination_location_id: draft.destId.trim(),
    source_ref: draft.sourceRef.trim(),
  })
}

function AirwayFields(args: { draft: AirDraft; patch: (next: AirDraft) => void }) {
  return (
    <fieldset className="flex flex-col gap-2">
      <legend className="text-xs">Lotniska UN/LOCODE</legend>
      <label className="text-xs">
        Zlecenie
        <input
          aria-label="Identyfikator zlecenia lotniczego"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="shipment_id"
          value={args.draft.shipmentId}
          onChange={(event) =>
            args.patch({ ...args.draft, shipmentId: event.currentTarget.value })
          }
          required
        />
      </label>
      <label className="text-xs">
        Start lotnisko
        <input
          aria-label="Identyfikator lotniska startu"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="origin_location_id"
          value={args.draft.originId}
          onChange={(event) =>
            args.patch({ ...args.draft, originId: event.currentTarget.value })
          }
          required
        />
      </label>
      <label className="text-xs">
        Koniec lotnisko
        <input
          aria-label="Identyfikator lotniska końca"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="destination_location_id"
          value={args.draft.destId}
          onChange={(event) =>
            args.patch({ ...args.draft, destId: event.currentTarget.value })
          }
          required
        />
      </label>
      <label className="text-xs">
        Źródło zapisu
        <input
          aria-label="Źródło zapisu odcinka lotniczego"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="source_ref"
          value={args.draft.sourceRef}
          onChange={(event) =>
            args.patch({ ...args.draft, sourceRef: event.currentTarget.value })
          }
          required
        />
      </label>
    </fieldset>
  )
}

function AirwaySaveForm(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_AIR)
  const persist = useMutation({
    mutationFn: () => persistAir(draft),
    onSuccess: () => {
      setDraft({ ...EMPTY_AIR })
      void cache.invalidateQueries({ queryKey: ["airway-legs", args.organizationId] })
    },
  })
  return (
    <form
      className="grid gap-2"
      data-air="leg-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Dwa lotniska z flagą airport. Nie HAWB. Nie IATA.
      </p>
      <AirwayFields draft={draft} patch={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz odcinek lotniczy
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function AirwayLegRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["airway-legs", args.organizationId],
    queryFn: listShipmentLegs,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const air = (listed.data ?? []).filter((row) => row.leg_kind === "air")
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-air="legs">
        {air.map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.shipment_id} · {row.origin_location_id} → {row.destination_location_id}{" "}
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function AirwayLegPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <AirwaySaveForm organizationId={args.organizationId} />
      <AirwayLegRows organizationId={args.organizationId} />
    </>
  )
}
