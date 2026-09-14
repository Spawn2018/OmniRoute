import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildL3GateMarkWrite, saveL3GateMark } from "@/lib/l3-gate-marks-api"

const KINDS = [
  { token: "sot", label: "sot — źródło prawdy" },
  { token: "owner", label: "owner — właściciel decyzji" },
  { token: "exception", label: "exception — wyjątek od bramy" },
  { token: "rollback", label: "rollback — wycofanie zmiany" },
  { token: "blast", label: "blast — promień wybuchu" },
  { token: "other", label: "other — pozostałe" },
] as const

export function L3GateMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("l3_sot_01")
  const [kind, setKind] = useState<string>("sot")
  const [origin, setOrigin] = useState("fixture://l3-gate/")
  const save = useMutation({
    mutationFn: () => saveL3GateMark(buildL3GateMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("l3_sot_01")
      setKind("sot")
      setOrigin("fixture://l3-gate/")
      void cache.invalidateQueries({
        queryKey: ["l3-gate-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-4 border-emerald-800/50 pl-3"
      data-l3-gate-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL checklisty bramy przed L3 (SoT/owner/exception/rollback/blast). Silnik L3 write,
        scoring Pain×Frequency i mutacja autonomy_level zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://l3-gate/…)"
        ariaLabel="Pochodzenie znacznika bramy L3"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika bramy L3"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="flex flex-col gap-1 text-xs">
        <span>Element checklisty bramy L3</span>
        <div
          aria-label="Rodzaj bramy L3 sot owner exception rollback blast other"
          className="flex flex-col gap-1"
          role="group"
        >
          {KINDS.map(({ token, label }) => (
            <Button
              key={token}
              aria-pressed={kind === token}
              className="h-9 justify-start rounded-none px-3 font-mono text-xs"
              onClick={() => setKind(token)}
              type="button"
              variant={kind === token ? "default" : "outline"}
            >
              {label}
            </Button>
          ))}
        </div>
      </div>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stancję bramy L3
      </Button>
    </form>
  )
}
