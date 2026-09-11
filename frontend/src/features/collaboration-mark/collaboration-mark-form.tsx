import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createCollaborationMark,
  toCollaborationWrite,
} from "@/lib/collaboration-marks-api"

const ROLES = [
  { id: "shipper", label: "Załadowca" },
  { id: "carrier", label: "Przewoźnik" },
  { id: "consignee", label: "Odbiorca" },
] as const

export function CollaborationMarkWriter(props: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [slug, setSlug] = useState("seat_shipper_01")
  const [role, setRole] = useState("shipper")
  const [pointer, setPointer] = useState("fixture://collaboration-mark/")
  const mutation = useMutation({
    mutationFn: () =>
      createCollaborationMark(toCollaborationWrite({ slug, role, pointer })),
    onSuccess: () => {
      setSlug("seat_shipper_01")
      setRole("shipper")
      setPointer("fixture://collaboration-mark/")
      void cache.invalidateQueries({
        queryKey: ["collaboration-marks", props.organizationId],
      })
    },
  })
  return (
    <form
      className="flex max-w-lg flex-col gap-4"
      data-collaboration-mark="editor"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <p className="text-sm text-muted-foreground">
        Rola współpracy trzech stron jako katalog. Bez wspólnego SELECT i bez
        tuple OpenFGA na kontrahencie.
      </p>
      <div className="grid gap-1 text-xs">
        <span>Kod roli</span>
        <input
          aria-label="Kod znacznika współpracy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(event) => setSlug(event.target.value)}
          required
          value={slug}
        />
      </div>
      <fieldset className="grid gap-2">
        <legend className="text-xs">Rola</legend>
        {ROLES.map((entry) => (
          <label key={entry.id} className="flex items-center gap-2 text-sm">
            <input
              checked={role === entry.id}
              name="collaboration-role"
              onChange={() => setRole(entry.id)}
              type="radio"
              value={entry.id}
            />
            {entry.label} ({entry.id})
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://collaboration-mark/…)"
        ariaLabel="Pochodzenie znacznika współpracy"
        value={pointer}
        onChange={setPointer}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit">
        Zapisz rolę współpracy
      </Button>
    </form>
  )
}
