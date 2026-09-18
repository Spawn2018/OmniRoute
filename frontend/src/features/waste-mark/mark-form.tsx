import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildWasteMarkWrite, saveWasteMark } from "@/lib/waste-marks-api"

const KINDS = ["bdo", "kpo", "wsr", "other"] as const

export function WasteMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bdo_01")
  const [kind, setKind] = useState<string>("bdo")
  const [origin, setOrigin] = useState("fixture://waste-mark/")
  const save = useMutation({
    mutationFn: () => saveWasteMark(buildWasteMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("bdo_01")
      setKind("bdo")
      setOrigin("fixture://waste-mark/")
      void cache.invalidateQueries({
        queryKey: ["waste-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-waste-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja BDO / KPO / WSR jako katalog HITL. Nie woła MOS i nie ustawia is_waste.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika odpadów"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj odpadów</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="waste-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://waste-mark/…)"
        ariaLabel="Pochodzenie znacznika odpadów"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik odpadów
      </Button>
    </form>
  )
}
