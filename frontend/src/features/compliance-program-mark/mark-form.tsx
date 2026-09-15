import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildComplianceProgramMarkWrite,
  saveComplianceProgramMark,
} from "@/lib/compliance-program-marks-api"

export function ComplianceProgramMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("cp_draft_01")
  const [kind, setKind] = useState("draft")
  const [origin, setOrigin] = useState("fixture://compliance-program/")
  const save = useMutation({
    mutationFn: () =>
      saveComplianceProgramMark(buildComplianceProgramMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("cp_draft_01")
      setKind("draft")
      setOrigin("fixture://compliance-program/")
      void cache.invalidateQueries({
        queryKey: ["compliance-program-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-md flex-col gap-3 border border-dashed border-slate-700/50 p-4"
      data-compliance-program-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL stancji programu zgodności (draft / review / signed / exempt). Bajty PDF,
        U-art50 i L3 write zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://compliance-program/…)"
        ariaLabel="Pochodzenie stancji programu zgodności"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika programu zgodności"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Stancja programu</span>
        <select
          aria-label="Stancja draft review signed exempt other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="draft">draft — szkic</option>
          <option value="review">review — przegląd</option>
          <option value="signed">signed — podpisany</option>
          <option value="exempt">exempt — zwolniony</option>
          <option value="other">other — pozostałe</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stancję
      </Button>
    </form>
  )
}
