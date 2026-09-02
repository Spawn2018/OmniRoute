import { useState } from "react"
import { useForm } from "@tanstack/react-form"
import { Link, useNavigate } from "@tanstack/react-router"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  clearSessionToken,
  getTenantContext,
  issueSessionToken,
  setSessionToken,
} from "@/lib/api"

const DEMO_EMAIL = "dev@example.com"
const DEMO_PASSWORD = "correct-horse-battery"

async function persistSession(email: string, password: string): Promise<void> {
  const token = await issueSessionToken({ email, password })
  setSessionToken(token)
}

function DemoTenantCard({
  pending,
  onLogin,
}: {
  pending: boolean
  onLogin: () => void
}) {
  return (
    <div className="space-y-2 rounded-md border border-border bg-card p-3">
      <p className="text-sm font-medium">Tenant demo</p>
      <p className="text-xs text-muted-foreground">
        Spedycja Demo · {DEMO_EMAIL} · hasło w seedzie lokalnym. Wyceny, stawki, porty, kontrahenci.
      </p>
      <Button type="button" disabled={pending} onClick={onLogin}>
        Zaloguj tenanta demo
      </Button>
    </div>
  )
}

export function SessionPage() {
  const initial = getTenantContext()
  const [saved, setSaved] = useState(initial.organizationId.length > 0)
  const [error, setError] = useState<string | null>(null)
  const [demoPending, setDemoPending] = useState(false)
  const navigate = useNavigate()
  const claims = getTenantContext()

  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
    onSubmit: async ({ value }) => {
      setError(null)
      try {
        await persistSession(value.email.trim(), value.password)
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
      <DemoTenantCard
        pending={demoPending}
        onLogin={() => {
          setDemoPending(true)
          void persistSession(DEMO_EMAIL, DEMO_PASSWORD)
            .then(() => {
              setSaved(true)
              setError(null)
              void navigate({ to: "/quotations" })
            })
            .catch(() => {
              setSaved(false)
              setError("Nie udało się zalogować tenanta demo.")
            })
            .finally(() => setDemoPending(false))
        }}
      />
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
          Token zapisany. Tenant {claims.organizationId || getTenantContext().organizationId} ·{" "}
          <Link className="underline" to="/quotations">
            Wyceny
          </Link>
        </p>
      ) : null}
    </div>
  )
}
