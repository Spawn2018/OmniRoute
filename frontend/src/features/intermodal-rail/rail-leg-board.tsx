import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listShipmentLegs, saveShipmentLeg } from "@/lib/shipment-legs-api"

type RailDraft = {
  shipmentId: string
  originId: string
  destId: string
  sourceRef: string
}

const EMPTY_RAIL: RailDraft = {
  shipmentId: "",
  originId: "",
  destId: "",
  sourceRef: "fixture://shipment-leg/",
}

const RAIL_FIELDS = [
  { key: "shipmentId", name: "shipment_id", caption: "Zlecenie" },
  { key: "originId", name: "origin_location_id", caption: "Start UN/LOCODE" },
  { key: "destId", name: "destination_location_id", caption: "Koniec UN/LOCODE" },
  { key: "sourceRef", name: "source_ref", caption: "Źródło" },
] as const

function persistRail(draft: RailDraft) {
  return saveShipmentLeg({
    leg_kind: "rail",
    shipment_id: draft.shipmentId.trim(),
    origin_location_id: draft.originId.trim(),
    destination_location_id: draft.destId.trim(),
    source_ref: draft.sourceRef.trim(),
  })
}

function RailFieldGrid(args: { draft: RailDraft; patch: (next: RailDraft) => void }) {
  return (
    <fieldset className="grid gap-2">
      {RAIL_FIELDS.map((field) => (
        <label key={field.name} className="text-xs">
          {field.caption}
          <input
            className="border-input h-8 w-full rounded-md border px-2 text-xs"
            name={field.name}
            value={args.draft[field.key]}
            onChange={(ev) =>
              args.patch({ ...args.draft, [field.key]: ev.currentTarget.value })
            }
            required
          />
        </label>
      ))}
    </fieldset>
  )
}

function RailSaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_RAIL)
  const save = useMutation({
    mutationFn: () => persistRail(draft),
    onSuccess: () => {
      setDraft({ ...EMPTY_RAIL })
      void client.invalidateQueries({ queryKey: ["rail-shipment-legs", args.organizationId] })
    },
  })
  return (
    <form
      className="grid gap-2"
      data-intermodal-rail="leg-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <RailFieldGrid draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz odcinek kolejowy
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

function RailLegRows(args: { organizationId: string | null }) {
  const rows = useQuery({
    queryKey: ["rail-shipment-legs", args.organizationId],
    queryFn: listShipmentLegs,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const rails = (rows.data ?? []).filter((row) => row.leg_kind === "rail")
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <dl data-intermodal-rail="legs">
        {rails.map((row) => (
          <div key={row.id} className="font-mono text-xs">
            <dt className="inline">{row.shipment_id}</dt>
            {" · "}
            <dd className="inline">{row.origin_location_id}</dd>
            {" → "}
            <dd className="inline">{row.destination_location_id}</dd>{" "}
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </div>
        ))}
      </dl>
    </>
  )
}

export function RailLegBoard(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <RailSaveStrip organizationId={args.organizationId} />
      <RailLegRows organizationId={args.organizationId} />
    </>
  )
}
