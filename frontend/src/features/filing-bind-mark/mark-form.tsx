import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildFilingBindMarkWrite, saveFilingBindMark } from "@/lib/filing-bind-marks-api"

const KINDS = ["shipment", "scheme", "both", "other"] as const

export function FilingBindMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bind_01")
  const [kind, setKind] = useState<string>("shipment")
  const [origin, setOrigin] = useState("fixture://filing-bind-mark/")
  const save = useMutation({
    mutationFn: () => saveFilingBindMark(buildFilingBindMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("bind_01")
      setKind("shipment")
      setOrigin("fixture://filing-bind-mark/")
      void cache.invalidateQueries({ queryKey: ["filing-bind-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-filing-bind-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja wiązania zgłoszenia SENT/BDO jako katalog HITL. Rodzaj to dana, nie FK
        shipment/scheme i nie PUESC.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika wiązania zgłoszenia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj wiązania</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="filing-bind-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://filing-bind-mark/…)"
        ariaLabel="Pochodzenie znacznika wiązania zgłoszenia"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wiązanie
      </Button>
    </form>
  )
}
