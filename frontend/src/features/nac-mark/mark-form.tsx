import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildNacMarkWrite, saveNacMark } from "@/lib/nac-marks-api"

const KINDS = ["nac", "nominated", "agent", "other"] as const

export function NacMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("nac_agent_01")
  const [kind, setKind] = useState<string>("agent")
  const [origin, setOrigin] = useState("fixture://nac-mark/")
  const save = useMutation({
    mutationFn: () => saveNacMark(buildNacMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("nac_agent_01")
      setKind("agent")
      setOrigin("fixture://nac-mark/")
      void cache.invalidateQueries({
        queryKey: ["nac-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-nac-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance NAC i agenta nominowanego jako katalog HITL. Live NAC HTTP i auto-dispatch nie
        wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance NAC"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj NAC</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="nac-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://nac-mark/…)"
        ariaLabel="Pochodzenie stance NAC"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance NAC
      </Button>
    </form>
  )
}
