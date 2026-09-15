import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCrmLinkMarkWrite, saveCrmLinkMark } from "@/lib/crm-link-marks-api"

const KINDS = ["lead", "party", "other"] as const

export function CrmLinkMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("crm_link_lead_01")
  const [linkKind, setLinkKind] = useState<string>("lead")
  const [sourceRef, setSourceRef] = useState("fixture://crm-link-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveCrmLinkMark(
        buildCrmLinkMarkWrite({ code: markCode, kind: linkKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("crm_link_lead_01")
      setLinkKind("lead")
      setSourceRef("fixture://crm-link-mark/")
      void cache.invalidateQueries({ queryKey: ["crm-link-marks", args.organizationId] })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (args.organizationId) save.mutate()
  }

  return (
    <form className="grid max-w-xl gap-3" data-crm-link-mark="write" onSubmit={onSubmit}>
      <p className="text-xs text-muted-foreground">
        Stance link CRM jako katalog HITL. Rodzaj to dana, nie FK UUID i nie cold-send.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance link CRM"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj powiązania</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={linkKind === token}
              name="crm-link-mark-kind"
              onChange={() => setLinkKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://crm-link-mark/…)"
        ariaLabel="Pochodzenie stance link CRM"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance link
      </Button>
    </form>
  )
}
