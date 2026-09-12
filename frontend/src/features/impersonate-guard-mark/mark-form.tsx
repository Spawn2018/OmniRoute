import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createImpersonateGuardMark,
  makeImpersonateGuardMarkPayload,
} from "@/lib/impersonate-guard-marks-api"

const GUARD_KINDS = [
  { value: "impersonate", label: "Impersonate" },
  { value: "unwrap_denied", label: "Unwrap denied" },
  { value: "other", label: "Inne" },
] as const

export function ImpersonateGuardMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("igm_impersonate_01")
  const [kind, setKind] = useState("impersonate")
  const [ref, setRef] = useState("fixture://impersonate-guard-mark/")
  const save = useMutation({
    mutationFn: () =>
      createImpersonateGuardMark(makeImpersonateGuardMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("igm_impersonate_01")
      setKind("impersonate")
      setRef("fixture://impersonate-guard-mark/")
      void qc.invalidateQueries({
        queryKey: ["impersonate-guard-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-igm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code impersonate guard"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        guard_kind
        <select
          aria-label="guard_kind impersonate unwrap_denied"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {GUARD_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref impersonate guard"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik impersonate guard
      </Button>
    </form>
  )
}
