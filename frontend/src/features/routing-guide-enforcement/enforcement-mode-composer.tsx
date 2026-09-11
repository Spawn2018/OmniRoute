import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  packEnforcementMode,
  postEnforcementMode,
} from "@/lib/routing-guide-enforcements-api"

const MODES = [
  { token: "record_only", caption: "Tylko zapis" },
  { token: "block_409", caption: "Blokada 409 (katalog)" },
] as const

export function EnforcementModeComposer(props: {
  tenantKey: string | null
}) {
  const cache = useQueryClient()
  const [code, setCode] = useState("mode_record_01")
  const [mode, setMode] = useState("record_only")
  const [origin, setOrigin] = useState("fixture://routing-guide-enforcement/")
  const write = useMutation({
    mutationFn: () =>
      postEnforcementMode(packEnforcementMode({ code, mode, origin })),
    onSuccess: () => {
      setCode("mode_record_01")
      setMode("record_only")
      setOrigin("fixture://routing-guide-enforcement/")
      void cache.invalidateQueries({
        queryKey: ["routing-guide-enforcements", props.tenantKey],
      })
    },
  })
  return (
    <form
      className="max-w-md space-y-5 border-l-2 border-muted pl-4"
      data-enforcement-mode="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.tenantKey) write.mutate()
      }}
    >
      <p className="text-sm leading-relaxed text-muted-foreground">
        Tryb egzekucji przewodnika jako wpis katalogu. Nie odpala HTTP 409 na
        zleceniu ani ASN w tym plasterze.
      </p>
      <div className="space-y-1">
        <label className="text-xs font-medium" htmlFor="enforcement-code">
          Kod trybu
        </label>
        <input
          aria-label="Kod trybu egzekucji przewodnika"
          className="h-10 w-full rounded border bg-background px-3 font-mono text-sm"
          id="enforcement-code"
          onChange={(event) => setCode(event.target.value)}
          required
          value={code}
        />
      </div>
      <div className="space-y-2">
        <span className="text-xs font-medium">Tryb</span>
        <div className="flex gap-2" role="group" aria-label="Tryb egzekucji">
          {MODES.map((entry) => {
            const active = mode === entry.token
            return (
              <button
                key={entry.token}
                aria-pressed={active}
                className={
                  active
                    ? "flex-1 rounded border border-foreground bg-foreground px-3 py-2 text-left text-xs text-background"
                    : "flex-1 rounded border border-muted bg-background px-3 py-2 text-left text-xs text-muted-foreground"
                }
                onClick={() => setMode(entry.token)}
                type="button"
              >
                <span className="block font-medium">{entry.caption}</span>
                <span className="mt-0.5 block font-mono opacity-80">{entry.token}</span>
              </button>
            )
          })}
        </div>
      </div>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://routing-guide-enforcement/…)"
        ariaLabel="Pochodzenie trybu egzekucji przewodnika"
        value={origin}
        onChange={setOrigin}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
      <Button disabled={!props.tenantKey || write.isPending} type="submit">
        Zapisz tryb egzekucji
      </Button>
    </form>
  )
}
