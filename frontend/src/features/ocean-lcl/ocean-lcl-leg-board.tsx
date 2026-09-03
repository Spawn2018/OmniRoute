import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listShipmentLegs, saveShipmentLeg } from "@/lib/shipment-legs-api"

const LCL_SLOTS = [
  ["Zlecenie", "shipment_id", ""],
  ["Start port morski", "origin_location_id", ""],
  ["Koniec port morski", "destination_location_id", ""],
  ["Źródło", "source_ref", "fixture://shipment-leg/"],
] as const

function readOceanLegForm(form: HTMLFormElement) {
  const box = new FormData(form)
  const text = (key: string) => String(box.get(key) ?? "").trim()
  return {
    leg_kind: "ocean_lcl" as const,
    shipment_id: text("shipment_id"),
    origin_location_id: text("origin_location_id"),
    destination_location_id: text("destination_location_id"),
    source_ref: text("source_ref"),
  }
}

function OceanLclSlots() {
  return (
    <dl className="flex flex-wrap gap-3">
      {LCL_SLOTS.map(([caption, name, preset]) => (
        <div key={name}>
          <dt className="text-xs">{caption}</dt>
          <dd>
            <input
              className="w-48 border px-1 text-xs"
              defaultValue={preset || undefined}
              name={name}
              required
            />
          </dd>
        </div>
      ))}
    </dl>
  )
}

function OceanLclSaveForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const save = useMutation({
    mutationFn: saveShipmentLeg,
    onSuccess: () => {
      void client.invalidateQueries({ queryKey: ["lcl-legs", args.organizationId] })
    },
  })
  return (
    <form
      data-ocean-lcl="leg-form"
      onSubmit={(event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const form = event.currentTarget
        save.mutate(readOceanLegForm(form), { onSuccess: () => form.reset() })
      }}
    >
      <OceanLclSlots />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz odcinek drobnicy
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

function OceanLclLegList(args: { organizationId: string | null }) {
  const rows = useQuery({
    queryKey: ["lcl-legs", args.organizationId],
    queryFn: listShipmentLegs,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const sea = (rows.data ?? []).filter((row) => row.leg_kind === "ocean_lcl")
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <ul data-ocean-lcl="legs">
        {sea.map((row) => (
          <li key={row.id} className="text-xs">
            {row.shipment_id} → {row.origin_location_id} / {row.destination_location_id}{" "}
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function OceanLclLegBoard(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <OceanLclSaveForm organizationId={args.organizationId} />
      <OceanLclLegList organizationId={args.organizationId} />
    </>
  )
}
