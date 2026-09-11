import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildFilingSchemeMarkWrite,
  saveFilingSchemeMark,
} from "@/lib/filing-scheme-marks-api"

const KINDS = ["ics2", "cbam", "eudr", "efti", "other"] as const

export function FilingSchemeMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("filing_ics2_01")
  const [kind, setKind] = useState<string>("ics2")
  const [origin, setOrigin] = useState("fixture://filing-scheme-mark/")
  const save = useMutation({
    mutationFn: () => saveFilingSchemeMark(buildFilingSchemeMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("filing_ics2_01")
      setKind("ics2")
      setOrigin("fixture://filing-scheme-mark/")
      void cache.invalidateQueries({ queryKey: ["filing-scheme-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-filing-scheme-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Schemat składania ICS2/CBAM/EUDR/eFTI jako katalog HITL. Rodzaj to dana, nie SENT-UE i nie filer live.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika schematu składania"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj schematu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="filing-scheme-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://filing-scheme-mark/…)"
        ariaLabel="Pochodzenie znacznika schematu składania"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz schemat składania
      </Button>
    </form>
  )
}
