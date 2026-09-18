import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildCreateBlockMarkWrite,
  saveCreateBlockMark,
} from "@/lib/create-block-marks-api"

const KINDS = ["block", "warn", "allow", "other"] as const

export function CreateBlockMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("gate_01")
  const [kind, setKind] = useState<string>("block")
  const [origin, setOrigin] = useState("fixture://create-block-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveCreateBlockMark(buildCreateBlockMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("gate_01")
      setKind("block")
      setOrigin("fixture://create-block-mark/")
      void cache.invalidateQueries({
        queryKey: ["create-block-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-create-block-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja bramy tworzenia zlecenia jako katalog HITL. Rodzaj to dana, nie live 409
        i nie egzekucja blocks_create.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika bramy create"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj bramy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="create-block-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://create-block-mark/…)"
        ariaLabel="Pochodzenie znacznika bramy create"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz bramę
      </Button>
    </form>
  )
}
