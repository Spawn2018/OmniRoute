import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createAutonomyLevel, makeAutonomyLevelPayload } from "@/lib/autonomy-levels-api"

export function AutonomyLevelComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [levelCode, setLevelCode] = useState("observer")
  const [ref, setRef] = useState("fixture://autonomy-level/")
  const save = useMutation({
    mutationFn: () =>
      createAutonomyLevel(
        makeAutonomyLevelPayload({
          levelCode,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://autonomy-level/")
      void qc.invalidateQueries({
        queryKey: ["autonomy-levels", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-autonomy-level="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        level_code
        <input
          aria-label="level_code poziom autonomii"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setLevelCode(e.target.value)}
          required
          value={levelCode}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref autonomy level"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz poziom autonomii
      </Button>
    </form>
  )
}
