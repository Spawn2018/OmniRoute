import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildLocalChargeWarningMarkWrite,
  saveLocalChargeWarningMark,
} from "@/lib/local-charge-warning-marks-api"

const WARNING_OPTIONS = ["warn", "hold", "waived", "other"] as const

export function LocalChargeWarningMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("warn_thc_01")
  const [kind, setKind] = useState<string>("warn")
  const [ref, setRef] = useState("fixture://local-charge-warning/")
  const save = useMutation({
    mutationFn: () =>
      saveLocalChargeWarningMark(buildLocalChargeWarningMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("warn_thc_01")
      setKind("warn")
      setRef("fixture://local-charge-warning/")
      void cache.invalidateQueries({
        queryKey: ["local-charge-warning-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-local-charge-warning-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance ostrzeżenia braku dopłaty jako dana HITL — nie warning-jako-fakt i nie 409 wyceny.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod ostrzeżenia dopłaty lokalnej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>warning_kind</legend>
        {WARNING_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="local-charge-warning-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://local-charge-warning/…)"
        ariaLabel="Pochodzenie ostrzeżenia dopłaty lokalnej"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz ostrzeżenie dopłaty
      </Button>
    </form>
  )
}
