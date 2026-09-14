import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildRfidMarkWrite, saveRfidMark } from "@/lib/rfid-marks-api"

const KINDS = ["reader", "gate", "tag", "other"] as const

export function RfidMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("rfid_gate_01")
  const [kind, setKind] = useState<string>("gate")
  const [origin, setOrigin] = useState("fixture://rfid/")
  const save = useMutation({
    mutationFn: () => saveRfidMark(buildRfidMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("rfid_gate_01")
      setKind("gate")
      setOrigin("fixture://rfid/")
      void cache.invalidateQueries({
        queryKey: ["rfid-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-rfid-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Czytnik, bramka lub znakowanie RFID jako katalog HITL. Live poll, odczyt EPC i parowanie
        z lokalizacją nie wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika RFID"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="grid gap-2 text-xs">
        <span>Rodzaj RFID</span>
        <div
          className="inline-flex max-w-full flex-wrap rounded-md border p-0.5"
          role="group"
          aria-label="Rodzaj znacznika RFID"
        >
          {KINDS.map((token) => (
            <Button
              key={token}
              aria-pressed={kind === token}
              className="h-8 flex-1 min-w-[4.5rem] px-2 font-mono text-xs"
              onClick={() => setKind(token)}
              type="button"
              variant={kind === token ? "default" : "ghost"}
            >
              {token}
            </Button>
          ))}
        </div>
      </div>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://rfid/…)"
        ariaLabel="Pochodzenie znacznika RFID"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik RFID
      </Button>
    </form>
  )
}
