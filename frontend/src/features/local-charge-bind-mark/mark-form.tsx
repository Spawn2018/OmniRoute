import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildLocalChargeBindMarkWrite,
  saveLocalChargeBindMark,
} from "@/lib/local-charge-bind-marks-api"

const BIND_OPTIONS = ["charge", "quote", "other"] as const

export function LocalChargeBindMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bind_charge_01")
  const [kind, setKind] = useState<string>("charge")
  const [ref, setRef] = useState("fixture://local-charge-bind/")
  const save = useMutation({
    mutationFn: () =>
      saveLocalChargeBindMark(buildLocalChargeBindMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("bind_charge_01")
      setKind("charge")
      setRef("fixture://local-charge-bind/")
      void cache.invalidateQueries({
        queryKey: ["local-charge-bind-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-local-charge-bind-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance wiązania dopłaty lokalnej jako dana HITL — nie FK UUID do charge/quote i nie matching SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod wiązania dopłaty lokalnej"
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
              checked={kind === token}
              name="local-charge-bind-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://local-charge-bind/…)"
        ariaLabel="Pochodzenie wiązania dopłaty lokalnej"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wiązanie dopłaty lokalnej
      </Button>
    </form>
  )
}
