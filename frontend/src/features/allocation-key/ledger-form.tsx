import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createAllocationKey, makeAllocationKeyPayload } from "@/lib/allocation-keys-api"

export function AllocationKeyComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [keyCode, setKeyCode] = useState("lane_direct")
  const [ref, setRef] = useState("fixture://allocation-key/")
  const save = useMutation({
    mutationFn: () =>
      createAllocationKey(
        makeAllocationKeyPayload({
          keyCode,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://allocation-key/")
      void qc.invalidateQueries({
        queryKey: ["allocation-keys", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-teal-700/30 bg-teal-50/20 p-3 dark:bg-teal-950/10"
      data-allocation-key="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        key_code
        <input
          aria-label="key_code klucz alokacji"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setKeyCode(e.target.value)}
          required
          value={keyCode}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref allocation key"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz klucz alokacji
      </Button>
    </form>
  )
}
