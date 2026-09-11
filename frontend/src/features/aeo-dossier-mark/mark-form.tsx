import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildAeoDossierMarkWrite, saveAeoDossierMark } from "@/lib/aeo-dossier-marks-api"

const KINDS = ["aeo", "authorised", "other"] as const

export function AeoDossierMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("aeo_dossier_01")
  const [kind, setKind] = useState<string>("aeo")
  const [origin, setOrigin] = useState("fixture://aeo-dossier-mark/")
  const save = useMutation({
    mutationFn: () => saveAeoDossierMark(buildAeoDossierMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("aeo_dossier_01")
      setKind("aeo")
      setOrigin("fixture://aeo-dossier-mark/")
      void cache.invalidateQueries({ queryKey: ["aeo-dossier-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-aeo-dossier-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Dossier AEO jako katalog HITL. Rodzaj to dana, nie party_document i nie scoring.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika dossier AEO"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj dossier</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="aeo-dossier-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://aeo-dossier-mark/…)"
        ariaLabel="Pochodzenie znacznika dossier AEO"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz dossier AEO
      </Button>
    </form>
  )
}
