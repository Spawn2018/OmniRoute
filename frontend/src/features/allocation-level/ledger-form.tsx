import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createAllocationLevel, makeAllocationLevelPayload } from "@/lib/allocation-levels-api"

export function AllocationLevelComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [levelCode, setLevelCode] = useState("tier_one")
  const [ref, setRef] = useState("fixture://allocation-level/")
  const save = useMutation({
    mutationFn: () =>
      createAllocationLevel(
        makeAllocationLevelPayload({
          levelCode,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://allocation-level/")
      void qc.invalidateQueries({
        queryKey: ["allocation-levels", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-teal-700/30 bg-teal-50/20 p-3 dark:bg-teal-950/10"
      data-allocation-level="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        level_code
        <input
          aria-label="level_code poziom alokacji"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setLevelCode(e.target.value)}
          required
          value={levelCode}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref allocation level"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz poziom alokacji
      </Button>
    </form>
  )
}
