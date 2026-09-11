import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildLegalHoldMarkWrite, saveLegalHoldMark } from "@/lib/legal-hold-marks-api"

const KINDS = ["retention", "legal_hold", "eidas"] as const

export function LegalHoldMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("legal_hold_wo_01")
  const [kind, setKind] = useState<string>("retention")
  const [origin, setOrigin] = useState("fixture://legal-hold-mark/")
  const save = useMutation({
    mutationFn: () => saveLegalHoldMark(buildLegalHoldMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("legal_hold_wo_01")
      setKind("retention")
      setOrigin("fixture://legal-hold-mark/")
      void cache.invalidateQueries({ queryKey: ["legal-hold-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-legal-hold-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik legal hold jako katalog HITL. Rodzaj to dana, nie silnik retention i nie eIDAS crypto.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika legal hold"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj pracy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="legal_hold-work"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://legal-hold-mark/…)"
        ariaLabel="Pochodzenie znacznika legal hold"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik legal hold
      </Button>
    </form>
  )
}
