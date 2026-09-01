import { Link } from "@tanstack/react-router"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function TenantSessionNotice() {
  return (
    <div className="rounded-md border border-border bg-card p-3 text-sm">
      Ustaw identyfikatory sesji na stronie{" "}
      <Link className="underline" to="/session">
        Sesja
      </Link>
      .
    </div>
  )
}

export function CatalogError({ error }: { error: unknown }) {
  return (
    <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
      {(error as Error).message}
    </div>
  )
}

export function CatalogHeading({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div>
      <h2 className="text-base font-semibold">{title}</h2>
      <p className="text-xs text-muted-foreground">{subtitle}</p>
    </div>
  )
}

export function ResolveTokenForm({
  label,
  placeholder,
  pending,
  resolved,
  onResolve,
}: {
  label: string
  placeholder: string
  pending: boolean
  resolved: string | null
  onResolve: (token: string) => void
}) {
  const [token, setToken] = useState("")

  return (
    <form
      className="flex gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        onResolve(token)
      }}
    >
      <Input
        aria-label={label}
        placeholder={placeholder}
        value={token}
        onChange={(event) => setToken(event.target.value)}
      />
      <Button type="submit" variant="outline" disabled={pending || !token}>
        Rozwiąż
      </Button>
      {resolved ? <div className="self-center font-mono text-xs">{resolved}</div> : null}
    </form>
  )
}
