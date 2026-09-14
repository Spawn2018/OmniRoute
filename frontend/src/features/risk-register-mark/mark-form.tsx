import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildRiskRegisterMarkWrite,
  saveRiskRegisterMark,
} from "@/lib/risk-register-marks-api"

const KINDS = ["open", "mitigated", "accepted", "other"] as const

export function RiskRegisterMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("rr_open_01")
  const [kind, setKind] = useState<string>("open")
  const [origin, setOrigin] = useState("fixture://risk-register/")
  const save = useMutation({
    mutationFn: () =>
      saveRiskRegisterMark(buildRiskRegisterMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("rr_open_01")
      setKind("open")
      setOrigin("fixture://risk-register/")
      void cache.invalidateQueries({
        queryKey: ["risk-register-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-risk-register-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL stancji wpisu rejestru ryzyka (open/mitigated/accepted). Scoring osoby, L3
        silnik i Mob Expo zostają poza tym katalogiem.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika rejestru ryzyka"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="grid gap-2 text-xs">
        <span>Rodzaj ryzyka</span>
        <div
          className="inline-flex max-w-full flex-wrap rounded-md border p-0.5"
          role="group"
          aria-label="Rodzaj znacznika rejestru ryzyka"
        >
          {KINDS.map((token) => (
            <Button
              key={token}
              aria-pressed={kind === token}
              className="h-8 flex-1 min-w-[4.5rem] px-2 font-mono text-xs"
              onClick={() => setKind(token)}
              type="button"
              variant={kind === token ? "default" : "ghost"}
            >
              {token}
            </Button>
          ))}
        </div>
      </div>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://risk-register/…)"
        ariaLabel="Pochodzenie znacznika rejestru ryzyka"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik rejestru
      </Button>
    </form>
  )
}
