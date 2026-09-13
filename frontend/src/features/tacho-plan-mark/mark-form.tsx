import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { createTachoPlanMark, makeTachoPlanMarkPayload } from "@/lib/tacho-plan-marks-api"

const CONSTRAINTS = ["plan", "window", "rest", "other"] as const

export function TachoPlanMarkSave({ organizationId }: { organizationId: string | null }) {
  const queryClient = useQueryClient()
  const [code, setCode] = useState("tpm_plan_01")
  const [kind, setKind] = useState("plan")
  const [origin, setOrigin] = useState("fixture://tacho-plan-mark/")
  const write = useMutation({
    mutationFn: () => createTachoPlanMark(makeTachoPlanMarkPayload(code, kind, origin)),
    onSuccess: () => {
      setCode("tpm_plan_01")
      setKind("plan")
      setOrigin("fixture://tacho-plan-mark/")
      void queryClient.invalidateQueries({ queryKey: ["tacho-plan-board", organizationId] })
    },
  })

  function onSave(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (organizationId) write.mutate()
  }

  return (
    <form className="flex max-w-lg flex-col gap-4" data-tacho-plan-mark="compose" onSubmit={onSave}>
      <p className="text-sm text-muted-foreground">
        Ograniczenie tacho zapisujesz jako stance planu. Godziny z DDD nie wchodzą do tego katalogu.
      </p>
      <label className="flex flex-col gap-1 text-sm">
        Kod ograniczenia (snake 2–32)
        <input
          aria-label="Kod ograniczenia tacho w planie"
          className="h-9 rounded border px-2 font-mono"
          onChange={(event) => setCode(event.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Rodzaj ograniczenia
        <select
          aria-label="Rodzaj ograniczenia tacho"
          className="h-9 rounded border bg-background px-2"
          onChange={(event) => setKind(event.target.value)}
          value={kind}
        >
          {CONSTRAINTS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tacho-plan-mark/…)"
        ariaLabel="Pochodzenie ograniczenia tacho"
        value={origin}
        onChange={setOrigin}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
      <button
        className="h-9 rounded border px-3 text-sm"
        disabled={!organizationId || write.isPending}
        type="submit"
      >
        Dodaj ograniczenie do planu
      </button>
    </form>
  )
}
