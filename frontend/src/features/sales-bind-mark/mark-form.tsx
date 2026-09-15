import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildSalesBindMarkWrite, saveSalesBindMark } from "@/lib/sales-bind-marks-api"

const BIND_OPTIONS = ["opportunity", "party", "other"] as const

export function SalesBindMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("sales_bind_opp_01")
  const [bind, setBind] = useState<string>("opportunity")
  const [ref, setRef] = useState("fixture://sales-bind-mark/")
  const save = useMutation({
    mutationFn: () => saveSalesBindMark(buildSalesBindMarkWrite(code, bind, ref)),
    onSuccess: () => {
      setCode("sales_bind_opp_01")
      setBind("opportunity")
      setRef("fixture://sales-bind-mark/")
      void cache.invalidateQueries({ queryKey: ["sales-bind-marks", args.organizationId] })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-sales-bind-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wiązanie korytarza sprzedażowego jako dana HITL — nie HubSpot i nie FK UUID.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod bind sprzedaży"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>bind_kind</legend>
        {BIND_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={bind === token}
              name="sales-bind-kind"
              onChange={() => setBind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://sales-bind-mark/…)"
        ariaLabel="Pochodzenie bind sprzedaży"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz bind korytarza
      </Button>
    </form>
  )
}
