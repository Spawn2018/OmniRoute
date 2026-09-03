import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listShipmentLegs, saveShipmentLeg } from "@/lib/shipment-legs-api"

const CN_ROWS = [
  ["Zlecenie", "shipment_id", ""],
  ["Start CN UN/LOCODE", "origin_location_id", ""],
  ["Koniec CN UN/LOCODE", "destination_location_id", ""],
  ["Źródło", "source_ref", "fixture://shipment-leg/"],
] as const

function readChinaLegForm(form: HTMLFormElement) {
  const box = new FormData(form)
  const text = (key: string) => String(box.get(key) ?? "").trim()
  return {
    leg_kind: "china_rail" as const,
    shipment_id: text("shipment_id"),
    origin_location_id: text("origin_location_id"),
    destination_location_id: text("destination_location_id"),
    source_ref: text("source_ref"),
  }
}

function ChinaRailCells() {
  return (
    <tbody>
      {CN_ROWS.map(([caption, name, preset]) => (
        <tr key={name}>
          <th className="pr-2 text-left text-xs font-normal">{caption}</th>
          <td>
            <input
              className="w-full border px-1 text-xs"
              defaultValue={preset || undefined}
              name={name}
              required
            />
          </td>
        </tr>
      ))}
    </tbody>
  )
}

function ChinaRailSaveForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const save = useMutation({
    mutationFn: saveShipmentLeg,
    onSuccess: () => {
      void client.invalidateQueries({ queryKey: ["cn-rail-legs", args.organizationId] })
    },
  })
  return (
    <form
      data-china-rail="leg-form"
      onSubmit={(event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const form = event.currentTarget
        save.mutate(readChinaLegForm(form), { onSuccess: () => form.reset() })
      }}
    >
      <table>
        <ChinaRailCells />
      </table>
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz odcinek kolej z Chin
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

function ChinaRailLegList(args: { organizationId: string | null }) {
  const rows = useQuery({
    queryKey: ["cn-rail-legs", args.organizationId],
    queryFn: listShipmentLegs,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const china = (rows.data ?? []).filter((row) => row.leg_kind === "china_rail")
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <ol data-china-rail="legs">
        {china.map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.shipment_id} {row.origin_location_id} {row.destination_location_id}{" "}
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ol>
    </>
  )
}

export function ChinaRailLegBoard(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <ChinaRailSaveForm organizationId={args.organizationId} />
      <ChinaRailLegList organizationId={args.organizationId} />
    </>
  )
}
