import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildStyleFidelityMarkWrite,
  saveStyleFidelityMark,
} from "@/lib/style-fidelity-marks-api"

const KINDS = [
  { token: "pass", label: "pass" },
  { token: "hold", label: "hold" },
  { token: "reject", label: "reject" },
  { token: "exempt", label: "exempt" },
  { token: "other", label: "other" },
] as const

export function StyleFidelityMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("fid_pass_01")
  const [kind, setKind] = useState("pass")
  const [origin, setOrigin] = useState("fixture://style-fidelity/")
  const save = useMutation({
    mutationFn: () =>
      saveStyleFidelityMark(buildStyleFidelityMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("fid_pass_01")
      setKind("pass")
      setOrigin("fixture://style-fidelity/")
      void cache.invalidateQueries({
        queryKey: ["style-fidelity-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-xl flex-col gap-4 rounded-sm bg-muted/20 p-3"
      data-style-fidelity-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL stancji bramki fidelity (pass/hold/reject/exempt). Wyliczanie progu 85%,
        porównanie LLM i auto-blokada szkicu zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://style-fidelity/…)"
        ariaLabel="Pochodzenie stancji fidelity"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika fidelity"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="flex flex-col gap-1 text-xs">
        <span>Stancja bramki fidelity</span>
        <div
          aria-label="Rodzaj fidelity pass hold reject exempt other"
          className="flex flex-wrap gap-1"
          role="group"
        >
          {KINDS.map(({ token, label }) => (
            <Button
              key={token}
              aria-pressed={kind === token}
              className="h-8 min-w-16 rounded-none px-2 font-mono text-xs"
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
        Zapisz stancję fidelity
      </Button>
    </form>
  )
}
