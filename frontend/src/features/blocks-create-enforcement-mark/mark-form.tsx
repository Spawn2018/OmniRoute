import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildBlocksCreateEnforcementMarkWrite,
  saveBlocksCreateEnforcementMark,
} from "@/lib/blocks-create-enforcement-marks-api"

const KINDS = ["block_409", "warn_only", "record_only", "other"] as const

export function BlocksCreateEnforcementMarkSave(args: {
  organizationId: string | null
}) {
  const cache = useQueryClient()
  const [code, setCode] = useState("enf_01")
  const [kind, setKind] = useState<string>("block_409")
  const [origin, setOrigin] = useState("fixture://blocks-create-enforcement-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveBlocksCreateEnforcementMark(
        buildBlocksCreateEnforcementMarkWrite({ code, kind, origin }),
      ),
    onSuccess: () => {
      setCode("enf_01")
      setKind("block_409")
      setOrigin("fixture://blocks-create-enforcement-mark/")
      void cache.invalidateQueries({
        queryKey: ["blocks-create-enforcement-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-blocks-create-enforcement-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Tryb egzekucji bramy create jako katalog HITL. Rodzaj to dana, nie live 409
        i nie wiring create_block_mark.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika egzekucji bramy create"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj egzekucji</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="blocks-create-enforcement-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://blocks-create-enforcement-mark/…)"
        ariaLabel="Pochodzenie znacznika egzekucji bramy create"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz tryb egzekucji
      </Button>
    </form>
  )
}
