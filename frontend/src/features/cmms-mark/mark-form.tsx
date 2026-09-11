import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCmmsMarkWrite, saveCmmsMark } from "@/lib/cmms-marks-api"

const KINDS = ["work_order", "dtc", "other"] as const

export function CmmsMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("cmms_wo_01")
  const [kind, setKind] = useState<string>("work_order")
  const [origin, setOrigin] = useState("fixture://cmms-mark/")
  const save = useMutation({
    mutationFn: () => saveCmmsMark(buildCmmsMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("cmms_wo_01")
      setKind("work_order")
      setOrigin("fixture://cmms-mark/")
      void cache.invalidateQueries({ queryKey: ["cmms-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-cmms-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik CMMS jako katalog HITL. Rodzaj to dana, nie silnik work_order i nie kara kierowcy.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika CMMS"
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
              name="cmms-work"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://cmms-mark/…)"
        ariaLabel="Pochodzenie znacznika CMMS"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik CMMS
      </Button>
    </form>
  )
}
