import { useState } from "react"
import { useForm } from "@tanstack/react-form"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  clearSessionToken,
  getTenantContext,
  issueSessionToken,
  setSessionToken,
} from "@/lib/api"

export function SessionPage() {
  const initial = getTenantContext()
  const [saved, setSaved] = useState(initial.organizationId.length > 0)
  const [error, setError] = useState<string | null>(null)
  const claims = getTenantContext()

  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
    onSubmit: async ({ value }) => {
      setError(null)
      try {
        const token = await issueSessionToken({
          email: value.email.trim(),
          password: value.password,
        })
        setSessionToken(token)
        setSaved(true)
      } catch {
        setSaved(false)
        setError("Nie udało się zalogować. Sprawdź email i hasło.")
      }
    },
  })

  return (
    <div className="max-w-lg space-y-3">
      <div>
        <h2 className="text-base font-semibold">Sesja</h2>
        <p className="text-xs text-muted-foreground">
          Email i hasło. Token JWT z claims org/sub. Headery X-Organization-Id nie ustalają
          tenanta.
        </p>
      </div>
      <form
        className="space-y-3"
        onSubmit={(event) => {
          event.preventDefault()
          event.stopPropagation()
          void form.handleSubmit()
        }}
      >
        <form.Field name="email">
          {(field) => (
            <label className="block space-y-1">
              <span className="text-xs text-muted-foreground">email</span>
              <Input
                type="email"
                autoComplete="username"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <form.Field name="password">
          {(field) => (
            <label className="block space-y-1">
              <span className="text-xs text-muted-foreground">hasło</span>
              <Input
                type="password"
                autoComplete="current-password"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <div className="flex gap-2">
          <Button type="submit">Zaloguj</Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              clearSessionToken()
              setSaved(false)
              setError(null)
            }}
          >
            Wyczyść
          </Button>
        </div>
      </form>
      {error ? <p className="text-xs text-destructive">{error}</p> : null}
      {saved ? (
        <p className="text-xs text-accent">
          Token zapisany. Tenant {claims.organizationId || getTenantContext().organizationId}
        </p>
      ) : null}
    </div>
  )
}
