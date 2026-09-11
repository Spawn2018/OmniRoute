import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildEdiMapMarkWrite, saveEdiMapMark } from "@/lib/edi-map-marks-api"

const KINDS = ["field_map", "segment", "other"] as const

export function EdiMapMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("edi_map_01")
  const [kind, setKind] = useState<string>("field_map")
  const [origin, setOrigin] = useState("fixture://edi-map-mark/")
  const save = useMutation({
    mutationFn: () => saveEdiMapMark(buildEdiMapMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("edi_map_01")
      setKind("field_map")
      setOrigin("fixture://edi-map-mark/")
      void cache.invalidateQueries({ queryKey: ["edi-map-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-edi-map-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Mapa pól EDI jako katalog HITL. Rodzaj to dana, nie silent write i nie parser live.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika mapy EDI"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj mapy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="edi-map-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://edi-map-mark/…)"
        ariaLabel="Pochodzenie znacznika mapy EDI"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz mapę EDI
      </Button>
    </form>
  )
}
