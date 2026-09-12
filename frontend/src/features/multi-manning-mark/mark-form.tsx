import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createMultiManningMark,
  makeMultiManningMarkPayload,
} from "@/lib/multi-manning-marks-api"

const CREW_MODES = [
  { value: "dual", label: "Dual (2 kierowcow)" },
  { value: "relay", label: "Relay" },
  { value: "team", label: "Team" },
  { value: "other", label: "Inne" },
] as const

export function MultiManningMarkComposer(props: {
  organizationId: string | null
}) {
  const queryClient = useQueryClient()
  const [crewCode, setCrewCode] = useState("mm_manual_01")
  const [crewMode, setCrewMode] = useState("dual")
  const [crewRef, setCrewRef] = useState("fixture://multi-manning-mark/")
  const persist = useMutation({
    mutationFn: () =>
      createMultiManningMark(
        makeMultiManningMarkPayload(crewCode, crewMode, crewRef),
      ),
    onSuccess: () => {
      setCrewCode("mm_manual_01")
      setCrewMode("dual")
      setCrewRef("fixture://multi-manning-mark/")
      void queryClient.invalidateQueries({
        queryKey: ["multi-manning-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-none border-b border-amber-800/40 pb-3"
      data-mm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) persist.mutate()
      }}
    >
      <div className="w-full">
        <p className="text-sm font-semibold">Dodaj tryb zalogi</p>
        <p className="text-[11px] text-muted-foreground">
          HITL — bez DDD i bez driver2 SQL.
        </p>
      </div>
      <label className="min-w-[10rem] flex-1 text-xs">
        mark_code
        <input
          aria-label="mark_code crew mode"
          className="mt-1 h-8 w-full border border-amber-900/30 px-2 font-mono text-sm"
          onChange={(e) => setCrewCode(e.target.value)}
          required
          value={crewCode}
        />
      </label>
      <label className="min-w-[10rem] flex-1 text-xs">
        manning_kind
        <select
          aria-label="manning_kind crew dual"
          className="mt-1 h-8 w-full border border-amber-900/30 px-2 text-sm"
          onChange={(e) => setCrewMode(e.target.value)}
          value={crewMode}
        >
          {CREW_MODES.map((mode) => (
            <option key={mode.value} value={mode.value}>
              {mode.label}
            </option>
          ))}
        </select>
      </label>
      <div className="w-full">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref crew mode"
          value={crewRef}
          onChange={setCrewRef}
        />
      </div>
      {persist.error ? <CatalogError error={persist.error} /> : null}
      <Button
        disabled={!props.organizationId || persist.isPending}
        type="submit"
        variant="accent"
      >
        Zapisz tryb zalogi
      </Button>
    </form>
  )
}
