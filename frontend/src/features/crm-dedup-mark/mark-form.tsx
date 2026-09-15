import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCrmDedupMarkWrite, saveCrmDedupMark } from "@/lib/crm-dedup-marks-api"

const KINDS = ["nip", "vat", "email", "other"] as const

export function CrmDedupMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("crm_dedup_nip_01")
  const [dedupKind, setDedupKind] = useState<string>("nip")
  const [sourceRef, setSourceRef] = useState("fixture://crm-dedup-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveCrmDedupMark(
        buildCrmDedupMarkWrite({ code: markCode, kind: dedupKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("crm_dedup_nip_01")
      setDedupKind("nip")
      setSourceRef("fixture://crm-dedup-mark/")
      void cache.invalidateQueries({ queryKey: ["crm-dedup-marks", args.organizationId] })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (args.organizationId) save.mutate()
  }

  return (
    <form className="grid max-w-xl gap-3" data-crm-dedup-mark="write" onSubmit={onSubmit}>
      <p className="text-xs text-muted-foreground">
        Stance dedup CRM jako katalog HITL. Rodzaj to dana, nie merge SQL i nie cold-send.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance dedup CRM"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj dedup</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={dedupKind === token}
              name="crm-dedup-mark-kind"
              onChange={() => setDedupKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://crm-dedup-mark/…)"
        ariaLabel="Pochodzenie stance dedup CRM"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance dedup
      </Button>
    </form>
  )
}
