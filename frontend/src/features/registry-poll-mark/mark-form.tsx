import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildRegistryPollMarkWrite, saveRegistryPollMark } from "@/lib/registry-poll-marks-api"

const KINDS = ["ceidg", "krs", "vies", "whitelist", "other"] as const

export function RegistryPollMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ceidg_01")
  const [kind, setKind] = useState<string>("ceidg")
  const [origin, setOrigin] = useState("fixture://registry-poll-mark/")
  const save = useMutation({
    mutationFn: () => saveRegistryPollMark(buildRegistryPollMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("ceidg_01")
      setKind("ceidg")
      setOrigin("fixture://registry-poll-mark/")
      void cache.invalidateQueries({ queryKey: ["registry-poll-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-registry-poll-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Poll rejestrów jako katalog HITL. Rodzaj to dana, nie live scrape i nie notice auto.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika poll rejestru"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj poll</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="yard-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://registry-poll-mark/…)"
        ariaLabel="Pochodzenie znacznika poll rejestru"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz poll
      </Button>
    </form>
  )
}
