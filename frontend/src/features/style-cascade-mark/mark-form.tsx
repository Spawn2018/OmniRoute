import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildStyleCascadeMarkWrite,
  saveStyleCascadeMark,
} from "@/lib/style-cascade-marks-api"

const KINDS = [
  { token: "global", label: "global — Global AI" },
  { token: "company", label: "company — styl spółki" },
  { token: "department", label: "department — dział" },
  { token: "user", label: "user — użytkownik" },
  { token: "customer", label: "customer — klient" },
  { token: "person", label: "person — person-to-person" },
  { token: "context", label: "context — bieżący kontekst" },
  { token: "other", label: "other — pozostałe" },
] as const

export function StyleCascadeMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("style_user_01")
  const [kind, setKind] = useState("user")
  const [origin, setOrigin] = useState("fixture://style-cascade/")
  const save = useMutation({
    mutationFn: () =>
      saveStyleCascadeMark(buildStyleCascadeMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("style_user_01")
      setKind("user")
      setOrigin("fixture://style-cascade/")
      void cache.invalidateQueries({
        queryKey: ["style-cascade-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-t-2 border-dashed border-teal-900/40 pt-3"
      data-style-cascade-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL poziomów kaskady stylu (Global→…→Context). Bramka fidelity 85%, scoring
        osoby i silnik generowania treści zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://style-cascade/…)"
        ariaLabel="Pochodzenie poziomu kaskady stylu"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika kaskady stylu"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="flex flex-col gap-1 text-xs">
        <legend>Poziom kaskady stylu</legend>
        {KINDS.map(({ token, label }) => (
          <label key={token} className="flex items-center gap-2 font-mono">
            <input
              checked={kind === token}
              name="cascade_kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            <span>{label}</span>
          </label>
        ))}
      </fieldset>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz poziom kaskady stylu
      </Button>
    </form>
  )
}
