import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createCopyBanMark,
  makeCopyBanMarkPayload,
} from "@/lib/copy-ban-marks-api"

const BAN_KINDS = [
  { value: "eight_min", label: "8 min" },
  { value: "fifteen_k", label: "15k" },
  { value: "five_hundred_k", label: "500k" },
  { value: "other", label: "Inne" },
] as const

export function CopyBanMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("cbm_eight_min_01")
  const [kind, setKind] = useState("eight_min")
  const [ref, setRef] = useState("fixture://copy-ban-mark/")
  const save = useMutation({
    mutationFn: () => createCopyBanMark(makeCopyBanMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("cbm_eight_min_01")
      setKind("eight_min")
      setRef("fixture://copy-ban-mark/")
      void qc.invalidateQueries({ queryKey: ["copy-ban-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-cbm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code copy ban"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        ban_kind
        <select
          aria-label="ban_kind eight_min fifteen_k five_hundred_k"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {BAN_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref copy ban"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz zakaz copy
      </Button>
    </form>
  )
}
