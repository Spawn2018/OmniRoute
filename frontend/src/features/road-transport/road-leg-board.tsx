import { type FormEvent, useId, useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { listShipmentLegs, saveShipmentLeg } from "@/lib/shipment-legs-api"

type LegDraft = {
  shipmentId: string
  originId: string
  destId: string
  sourceRef: string
}

const EMPTY_LEG: LegDraft = {
  shipmentId: "",
  originId: "",
  destId: "",
  sourceRef: "fixture://shipment-leg/",
}

function ShipAndSourceFields(args: { draft: LegDraft; patch: (next: LegDraft) => void }) {
  const draft = args.draft
  const shipField = useId()
  const sourceField = useId()
  return (
    <>
      <label className="text-xs" htmlFor={shipField}>
        Zlecenie
        <Input
          id={shipField}
          name="shipment_id"
          placeholder="shipment_id"
          value={draft.shipmentId}
          onChange={(event) => args.patch({ ...draft, shipmentId: event.target.value })}
          required
        />
      </label>
      <label className="text-xs" htmlFor={sourceField}>
        Źródło
        <Input
          id={sourceField}
          name="source_ref"
          placeholder="source_ref"
          value={draft.sourceRef}
          onChange={(event) => args.patch({ ...draft, sourceRef: event.target.value })}
          required
        />
      </label>
    </>
  )
}

function OriginDestFields(args: { draft: LegDraft; patch: (next: LegDraft) => void }) {
  const draft = args.draft
  const originField = useId()
  const destField = useId()
  return (
    <>
      <label className="text-xs" htmlFor={originField}>
        Start
        <Input
          id={originField}
          name="origin_location_id"
          placeholder="origin_location_id"
          value={draft.originId}
          onChange={(event) => args.patch({ ...draft, originId: event.target.value })}
          required
        />
      </label>
      <label className="text-xs" htmlFor={destField}>
        Koniec
        <Input
          id={destField}
          name="destination_location_id"
          placeholder="destination_location_id"
          value={draft.destId}
          onChange={(event) => args.patch({ ...draft, destId: event.target.value })}
          required
        />
      </label>
    </>
  )
}

function LegSaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LEG)
  const save = useMutation({
    mutationFn: () =>
      saveShipmentLeg({
        shipment_id: draft.shipmentId.trim(),
        origin_location_id: draft.originId.trim(),
        destination_location_id: draft.destId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...EMPTY_LEG })
      void client.invalidateQueries({ queryKey: ["shipment-legs", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-col gap-2"
      data-road-transport="leg-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <ShipAndSourceFields draft={draft} patch={setDraft} />
      <OriginDestFields draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz odcinek
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

function LegRows(args: { organizationId: string | null }) {
  const rows = useQuery({
    queryKey: ["shipment-legs", args.organizationId],
    queryFn: listShipmentLegs,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <ul data-road-transport="legs">
        {(rows.data ?? [])
          .filter((row) => row.leg_kind === "road")
          .map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.leg_kind} {row.shipment_id} {row.origin_location_id} → {row.destination_location_id}{" "}
            {row.source_ref}{" "}
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function RoadLegBoard(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <LegSaveStrip organizationId={args.organizationId} />
      <LegRows organizationId={args.organizationId} />
    </>
  )
}
