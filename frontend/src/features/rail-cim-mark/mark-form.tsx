import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useId, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createRailCimMark, makeRailCimMarkPayload } from "@/lib/rail-cim-marks-api"

const KIND_OPTIONS = [
  { value: "uic", label: "UIC" },
  { value: "cim", label: "CIM" },
  { value: "smgs", label: "SMGS" },
  { value: "other", label: "Inne" },
] as const

export function RailCimMarkComposer(props: { organizationId: string | null }) {
  const formId = useId()
  const qc = useQueryClient()
  const [code, setCode] = useState("rcim_manual_01")
  const [kind, setKind] = useState("uic")
  const [ref, setRef] = useState("fixture://rail-cim-mark/")
  const mutation = useMutation({
    mutationFn: () => createRailCimMark(makeRailCimMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("rcim_manual_01")
      setKind("uic")
      setRef("fixture://rail-cim-mark/")
      void qc.invalidateQueries({ queryKey: ["rail-cim-marks", props.organizationId] })
    },
  })

  return (
    <aside className="rounded border border-amber-700/40 bg-card p-3 shadow-sm">
      <form
        id={formId}
        className="space-y-3"
        data-rcim="composer"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) mutation.mutate()
        }}
      >
        <div>
          <p className="font-medium text-sm">Nowy znacznik UIC/CIM/SMGS</p>
          <p className="text-[11px] text-muted-foreground">HITL — bez filing i bez scrape.</p>
        </div>
        <label className="block text-xs">
          mark_code
          <input
            aria-label="mark_code rail CIM"
            className="mt-1 block h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <fieldset className="space-y-1">
          <legend className="text-xs">rail_kind</legend>
          <div className="flex flex-wrap gap-2">
            {KIND_OPTIONS.map((opt) => (
              <label key={opt.value} className="flex items-center gap-1 text-xs">
                <input
                  checked={kind === opt.value}
                  name="rail_kind"
                  onChange={() => setKind(opt.value)}
                  type="radio"
                  value={opt.value}
                />
                {opt.label}
              </label>
            ))}
          </div>
        </fieldset>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref rail CIM"
          value={ref}
          onChange={setRef}
        />
        {mutation.error ? <CatalogError error={mutation.error} /> : null}
        <Button
          disabled={!props.organizationId || mutation.isPending}
          form={formId}
          type="submit"
          variant="ghost"
        >
          Zapisz znacznik rail
        </Button>
      </form>
    </aside>
  )
}
