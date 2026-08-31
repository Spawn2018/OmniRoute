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
      organizationId: initial.organizationId,
      userId: initial.userId,
    },
    onSubmit: async ({ value }) => {
      setError(null)
      try {
        const token = await issueSessionToken({
          organizationId: value.organizationId.trim(),
          userId: value.userId.trim(),
        })
        setSessionToken(token)
        setSaved(true)
      } catch {
        setSaved(false)
        setError("Nie udało się uzyskać tokenu sesji. Sprawdź ID z seeda.")
      }
    },
  })

  return (
    <div className="max-w-lg space-y-3">
      <div>
        <h2 className="text-base font-semibold">Sesja deweloperska</h2>
        <p className="text-xs text-muted-foreground">
          Hello JWT: token z claims org/sub. Headery X-Organization-Id nie ustalają tenanta.
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
        <form.Field name="organizationId">
          {(field) => (
            <label className="block space-y-1">
              <span className="text-xs text-muted-foreground">organization_id</span>
              <Input
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <form.Field name="userId">
          {(field) => (
            <label className="block space-y-1">
              <span className="text-xs text-muted-foreground">user_id</span>
              <Input
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <div className="flex gap-2">
          <Button type="submit">Pobierz token</Button>
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
