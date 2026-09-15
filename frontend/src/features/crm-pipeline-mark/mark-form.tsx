import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCrmPipelineMarkWrite, saveCrmPipelineMark } from "@/lib/crm-pipeline-marks-api"

const KINDS = ["stage", "won", "lost", "hold", "other"] as const

export function CrmPipelineMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("crm_stage_01")
  const [kind, setKind] = useState<string>("stage")
  const [origin, setOrigin] = useState("fixture://crm-pipeline-mark/")
  const save = useMutation({
    mutationFn: () => saveCrmPipelineMark(buildCrmPipelineMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("crm_stage_01")
      setKind("stage")
      setOrigin("fixture://crm-pipeline-mark/")
      void cache.invalidateQueries({ queryKey: ["crm-pipeline-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-crm-pipeline-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Etap CRM jako katalog HITL. Rodzaj to dana, nie silnik lejka i nie FK do okazji.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod etapu CRM"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj etapu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="crm-pipeline-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://crm-pipeline-mark/…)"
        ariaLabel="Pochodzenie etapu CRM"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz etap CRM
      </Button>
    </form>
  )
}
