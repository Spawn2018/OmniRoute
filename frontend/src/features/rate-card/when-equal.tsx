import { useQuery } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { fetchEqualWhen } from "@/lib/rate-cards-api"

export function WhenEqualStrip(args: { organizationId: string | null }) {
  const [needle, setNeedle] = useState("sobota")
  const [armed, setArmed] = useState("")
  const equals = useQuery({
    queryKey: ["when-equals", args.organizationId, armed],
    queryFn: () => fetchEqualWhen(armed),
    enabled: Boolean(args.organizationId) && armed !== "",
    retry: false,
  })
  return (
    <aside className="max-w-sm space-y-2 border p-3 rounded-md" data-rate-card="equal-when">
      <form
        className="space-y-2"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          setArmed(needle.trim())
        }}
      >
        <p className="text-xs text-muted-foreground">
          Równość `applies_when` w SQL jak extra portowe. To nie parser WHEN/IF.
        </p>
        <label className="block text-xs">
          Warunek do porównania
          <input
            aria-label="Warunek równości karty"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2 font-mono"
            value={needle}
            onChange={(change) => setNeedle(change.target.value)}
          />
        </label>
        <Button type="submit" disabled={args.organizationId === null}>
          Dopasuj warunek
        </Button>
      </form>
      {equals.isError ? <CatalogError error={equals.error} /> : null}
      <ol data-rate-card="equal-rows" className="m-0 list-decimal pl-4 text-xs font-mono">
        {(equals.data ?? []).map((row) => (
          <li key={row.id}>
            {row.card_code} · {row.applies_when}
          </li>
        ))}
      </ol>
    </aside>
  )
}
