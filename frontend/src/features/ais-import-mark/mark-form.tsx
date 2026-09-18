import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildAisImportMarkWrite,
  saveAisImportMark,
} from "@/lib/ais-import-marks-api"

const KINDS = ["ais", "aes", "intrastat", "other"] as const

export function AisImportMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ais_01")
  const [kind, setKind] = useState<string>("ais")
  const [origin, setOrigin] = useState("fixture://ais-import-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveAisImportMark(buildAisImportMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("ais_01")
      setKind("ais")
      setOrigin("fixture://ais-import-mark/")
      void cache.invalidateQueries({
        queryKey: ["ais-import-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-ais-import-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja AIS-IMPORT / AES / Intrastat jako katalog HITL. Nie woła PUESC.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika AIS AES Intrastat"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj zgłoszenia</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="ais-import-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://ais-import-mark/…)"
        ariaLabel="Pochodzenie znacznika AIS"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik AIS
      </Button>
    </form>
  )
}
