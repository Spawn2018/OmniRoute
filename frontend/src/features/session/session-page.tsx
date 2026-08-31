import { useState } from "react"
import { useForm } from "@tanstack/react-form"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { getTenantContext, setTenantContext } from "@/lib/api"

export function SessionPage() {
  const initial = getTenantContext()
  const [saved, setSaved] = useState(false)

  const form = useForm({
    defaultValues: {
      organizationId: initial.organizationId,
      userId: initial.userId,
    },
    onSubmit: ({ value }) => {
      setTenantContext({
        organizationId: value.organizationId.trim(),
        userId: value.userId.trim(),
      })
      setSaved(true)
    },
  })

  return (
    <div className="max-w-lg space-y-3">
      <div>
        <h2 className="text-base font-semibold">Sesja deweloperska</h2>
        <p className="text-xs text-muted-foreground">
          Tymczasowe headery pod RLS/OpenFGA (JWT w kolejnym plastrze).
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
              <span className="text-xs text-muted-foreground">X-Organization-Id</span>
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
              <span className="text-xs text-muted-foreground">X-User-Id</span>
              <Input
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <Button type="submit">Zapisz w localStorage</Button>
      </form>
      {saved ? <p className="text-xs text-accent">Zapisano.</p> : null}
    </div>
  )
}
