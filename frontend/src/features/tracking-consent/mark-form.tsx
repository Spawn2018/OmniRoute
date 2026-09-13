import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildTrackingConsentWrite, saveTrackingConsent } from "@/lib/tracking-consents-api"

const KINDS = ["party", "driver", "other"] as const

export function TrackingConsentSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("cns_party_01")
  const [kind, setKind] = useState<string>("party")
  const [origin, setOrigin] = useState("fixture://tracking-consent/")
  const save = useMutation({
    mutationFn: () => saveTrackingConsent(buildTrackingConsentWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("cns_party_01")
      setKind("party")
      setOrigin("fixture://tracking-consent/")
      void cache.invalidateQueries({ queryKey: ["tracking-consents", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-tracking-consent="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Zgoda na śledzenie jako katalog HITL. Rodzaj to dana, nie kolumna na kontakcie i nie live poll.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod zgody na śledzenie"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj zgody</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="tracking-consent-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tracking-consent/…)"
        ariaLabel="Pochodzenie zgody na śledzenie"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz zgodę
      </Button>
    </form>
  )
}
