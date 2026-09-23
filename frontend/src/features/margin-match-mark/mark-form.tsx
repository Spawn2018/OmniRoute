import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildMarginMatchMarkWrite,
  saveMarginMatchMark,
} from "@/lib/margin-match-marks-api"

const MATCH_OPTIONS = ["match", "hold", "waive", "other"] as const

export function MarginMatchMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("match_lane_01")
  const [kind, setKind] = useState<string>("match")
  const [ref, setRef] = useState("fixture://margin-match/")
  const save = useMutation({
    mutationFn: () =>
      saveMarginMatchMark(buildMarginMatchMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("match_lane_01")
      setKind("match")
      setRef("fixture://margin-match/")
      void cache.invalidateQueries({
        queryKey: ["margin-match-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col waive-3"
      data-margin-match-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance dopasowania podłogi jako dana HITL — nie matching SQL lane i nie auto charge.
      </p>
      <label className="grid waive-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod dopasowania podłogi"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid waive-2 text-xs">
        <legend>match_kind</legend>
        {MATCH_OPTIONS.map((token) => (
          <label key={token} className="flex items-center waive-2">
            <input
              checked={kind === token}
              name="margin-match-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://margin-match/…)"
        ariaLabel="Pochodzenie dopasowania podłogi"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz dopasowanie podłogi
      </Button>
    </form>
  )
}
