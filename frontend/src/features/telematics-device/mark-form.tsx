import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildTelematicsDeviceWrite, saveTelematicsDevice } from "@/lib/telematics-devices-api"

const KINDS = ["tracker", "fault", "other"] as const

export function TelematicsDeviceSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("trk_yard_01")
  const [kind, setKind] = useState<string>("tracker")
  const [origin, setOrigin] = useState("fixture://telematics-device/")
  const save = useMutation({
    mutationFn: () => saveTelematicsDevice(buildTelematicsDeviceWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("trk_yard_01")
      setKind("tracker")
      setOrigin("fixture://telematics-device/")
      void cache.invalidateQueries({ queryKey: ["telematics-devices", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-telematics-device="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Urządzenie jako katalog HITL. Rodzaj to dana, nie parowanie z pojazdem i nie live poll.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod urządzenia telematycznego"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj urządzenia</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="telematics-device-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://telematics-device/…)"
        ariaLabel="Pochodzenie urządzenia telematycznego"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz urządzenie
      </Button>
    </form>
  )
}
