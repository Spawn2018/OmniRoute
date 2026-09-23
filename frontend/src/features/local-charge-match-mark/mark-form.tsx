import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildLocalChargeMatchMarkWrite,
  saveLocalChargeMatchMark,
} from "@/lib/local-charge-match-marks-api"

const MATCH_OPTIONS = ["match", "gap", "waive", "other"] as const

export function LocalChargeMatchMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("match_lane_01")
  const [kind, setKind] = useState<string>("match")
  const [ref, setRef] = useState("fixture://local-charge-match/")
  const save = useMutation({
    mutationFn: () =>
      saveLocalChargeMatchMark(buildLocalChargeMatchMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("match_lane_01")
      setKind("match")
      setRef("fixture://local-charge-match/")
      void cache.invalidateQueries({
        queryKey: ["local-charge-match-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-local-charge-match-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance dopasowania dopłaty lokalnej jako dana HITL — nie matching SQL vs local_charge i nie warning-jako-fakt.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod dopasowania dopłaty lokalnej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>match_kind</legend>
        {MATCH_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="local-charge-match-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://local-charge-match/…)"
        ariaLabel="Pochodzenie dopasowania dopłaty lokalnej"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz dopasowanie dopłaty lokalnej
      </Button>
    </form>
  )
}
