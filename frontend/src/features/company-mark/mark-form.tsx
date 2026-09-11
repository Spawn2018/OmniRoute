import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCompanyMarkWrite, saveCompanyMark } from "@/lib/company-marks-api"

const KINDS = ["hq", "branch", "other"] as const

export function CompanyMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("co_hq_01")
  const [kind, setKind] = useState<string>("hq")
  const [origin, setOrigin] = useState("fixture://company-mark/")
  const save = useMutation({
    mutationFn: () => saveCompanyMark(buildCompanyMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("co_hq_01")
      setKind("hq")
      setOrigin("fixture://company-mark/")
      void cache.invalidateQueries({ queryKey: ["company-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-company-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik spółki jako katalog HITL. Rodzaj to dana, nie silnik hq i nie drugi tenant.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika spółki"
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
              name="company-work"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://company-mark/…)"
        ariaLabel="Pochodzenie znacznika spółki"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik spółki
      </Button>
    </form>
  )
}
