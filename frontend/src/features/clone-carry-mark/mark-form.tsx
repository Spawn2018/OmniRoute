import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildCloneCarryMarkWrite,
  saveCloneCarryMark,
} from "@/lib/clone-carry-marks-api"

const CARRY_OPTIONS = ["carry", "held", "skip", "other"] as const

export function CloneCarryMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("carry_on_clone_01")
  const [kind, setKind] = useState<string>("carry")
  const [ref, setRef] = useState("fixture://clone-carry/")
  const save = useMutation({
    mutationFn: () => saveCloneCarryMark(buildCloneCarryMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("carry_on_clone_01")
      setKind("carry")
      setRef("fixture://clone-carry/")
      void cache.invalidateQueries({ queryKey: ["clone-carry-marks", args.organizationId] })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-clone-carry-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance przeniesienia allowlisty U1 przy klonie — nie auto-copy i nie similar SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod carry przy klonie"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>carry_kind</legend>
        {CARRY_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="clone-carry-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://clone-carry/…)"
        ariaLabel="Pochodzenie carry przy klonie"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz carry przy klonie
      </Button>
    </form>
  )
}
