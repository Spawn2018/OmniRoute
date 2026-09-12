import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createDualLedgerMark,
  makeDualLedgerMarkPayload,
} from "@/lib/dual-ledger-marks-api"

const LEDGER_KINDS = [
  { value: "ops", label: "Operacyjny" },
  { value: "finance", label: "Finansowy" },
  { value: "tax", label: "Podatkowy" },
  { value: "other", label: "Inne" },
] as const

export function DualLedgerMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("dlm_ops_01")
  const [kind, setKind] = useState("ops")
  const [ref, setRef] = useState("fixture://dual-ledger-mark/")
  const save = useMutation({
    mutationFn: () =>
      createDualLedgerMark(makeDualLedgerMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("dlm_ops_01")
      setKind("ops")
      setRef("fixture://dual-ledger-mark/")
      void qc.invalidateQueries({
        queryKey: ["dual-ledger-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-dlm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code dual ledger"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        ledger_kind
        <select
          aria-label="ledger_kind ops finance tax other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {LEDGER_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref dual ledger"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik dual ledger
      </Button>
    </form>
  )
}
