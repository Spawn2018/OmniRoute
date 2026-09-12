import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createPostingMark,
  makePostingMarkPayload,
} from "@/lib/posting-marks-api"

const POSTING_KINDS = [
  { value: "posting", label: "Posting" },
  { value: "delegation", label: "Delegation" },
  { value: "host", label: "Host state" },
  { value: "other", label: "Inne" },
] as const

export function PostingMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("po_manual_01")
  const [kind, setKind] = useState("posting")
  const [ref, setRef] = useState("fixture://posting-mark/")
  const save = useMutation({
    mutationFn: () => createPostingMark(makePostingMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("po_manual_01")
      setKind("posting")
      setRef("fixture://posting-mark/")
      void qc.invalidateQueries({ queryKey: ["posting-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="grid gap-2 rounded-md border border-sky-700/30 bg-background p-3 sm:grid-cols-[1fr_1fr_auto]"
      data-po="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="sm:col-span-3 text-sm font-medium">Nowy znacznik posting</p>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code posting"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        posting_kind
        <select
          aria-label="posting_kind posting host"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {POSTING_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <div className="sm:col-span-3">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref posting"
          value={ref}
          onChange={setRef}
        />
      </div>
      {save.error ? (
        <div className="sm:col-span-3">
          <CatalogError error={save.error} />
        </div>
      ) : null}
      <Button
        className="sm:col-start-3"
        disabled={!props.organizationId || save.isPending}
        type="submit"
        variant="outline"
      >
        Zapisz posting
      </Button>
    </form>
  )
}
