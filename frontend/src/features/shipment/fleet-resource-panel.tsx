import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchResources, resourceWrite, saveResource } from "@/lib/resources-api"
import { getTenantContext } from "@/lib/tenant"

const KINDS = [
  { token: "vehicle", label: "pojazd" },
  { token: "driver", label: "kierowca" },
  { token: "trailer", label: "naczepa" },
] as const

export function FleetResourcePanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const cache = useQueryClient()
  const [kind, setKind] = useState("vehicle")
  const [label, setLabel] = useState("")
  const [plate, setPlate] = useState("")
  const [capacityKg, setCapacityKg] = useState("")
  const listed = useQuery({
    queryKey: ["resources", ctx.organizationId, kind],
    queryFn: () => fetchResources(kind),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () =>
      saveResource(resourceWrite({ kind, label, plate, capacityKg })),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["resources", ctx.organizationId, kind] })
    },
  })
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-resource="fleet">
      <h2 className="text-sm font-medium">Katalog floty</h2>
      <p className="text-xs text-muted-foreground">
        Pojazd, kierowca albo naczepa. Opcjonalna pojemność kg. Nie trip. Nie własne HW.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj zasobu
        <select
          aria-label="Rodzaj zasobu floty"
          className="h-8 rounded-md border border-border bg-background px-2 text-sm"
          value={kind}
          onChange={(event) => setKind(event.target.value)}
        >
          {KINDS.map((entry) => (
            <option key={entry.token} value={entry.token}>
              {entry.label}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Nazwa
        <Input
          aria-label="Nazwa zasobu floty"
          placeholder="display_name"
          value={label}
          onChange={(event) => setLabel(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Numer rejestracyjny (opcjonalnie)
        <Input
          aria-label="Numer rejestracyjny zasobu"
          placeholder="registration_no"
          value={plate}
          onChange={(event) => setPlate(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pojemność kg (opcjonalnie)
        <Input
          aria-label="Pojemność kg zasobu"
          placeholder="capacity_kg"
          value={capacityKg}
          onChange={(event) => setCapacityKg(event.target.value)}
        />
      </label>
      <Button
        type="button"
        disabled={!args.signedIn || label.trim() === "" || persist.isPending}
        onClick={() => persist.mutate()}
      >
        Zapisz zasób
      </Button>
      {persist.isError ? <p className="text-sm text-destructive">{(persist.error as Error).message}</p> : null}
      <ul className="space-y-1">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.resource_kind} · {row.display_name}
            {row.registration_no ? ` · ${row.registration_no}` : ""}
            {row.capacity_kg ? ` · ${row.capacity_kg} kg` : ""}
          </li>
        ))}
      </ul>
    </section>
  )
}
