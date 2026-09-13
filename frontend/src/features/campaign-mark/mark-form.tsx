import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCampaignMarkWrite, saveCampaignMark } from "@/lib/campaign-marks-api"

const KINDS = ["campaign", "attribution", "other"] as const

export function CampaignMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("cmp_campaign_01")
  const [kind, setKind] = useState<string>("campaign")
  const [origin, setOrigin] = useState("fixture://campaign-mark/")
  const save = useMutation({
    mutationFn: () => saveCampaignMark(buildCampaignMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("cmp_campaign_01")
      setKind("campaign")
      setOrigin("fixture://campaign-mark/")
      void cache.invalidateQueries({ queryKey: ["campaign-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-campaign-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kampania jako katalog HITL. Rodzaj to dana, nie lejek X7 i nie atrybucja live.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika kampanii"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj kampanii</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="campaign-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://campaign-mark/…)"
        ariaLabel="Pochodzenie znacznika kampanii"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz kampanię
      </Button>
    </form>
  )
}
