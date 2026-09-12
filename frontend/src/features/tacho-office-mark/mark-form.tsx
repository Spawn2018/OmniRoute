import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createTachoOfficeMark,
  makeTachoOfficeMarkPayload,
} from "@/lib/tacho-office-marks-api"

const TACHO_KINDS = [
  { value: "office", label: "Office" },
  { value: "card", label: "Card" },
  { value: "ddd", label: "DDD marker" },
  { value: "other", label: "Inne" },
] as const

export function TachoOfficeMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("to_manual_01")
  const [kind, setKind] = useState("office")
  const [ref, setRef] = useState("fixture://tacho-office-mark/")
  const save = useMutation({
    mutationFn: () =>
      createTachoOfficeMark(makeTachoOfficeMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("to_manual_01")
      setKind("office")
      setRef("fixture://tacho-office-mark/")
      void qc.invalidateQueries({
        queryKey: ["tacho-office-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border-t border-zinc-600/30 pt-3"
      data-to="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="text-sm font-semibold">Nowy znacznik tacho office</p>
      <div className="grid gap-2 sm:grid-cols-2">
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code tacho office"
            className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          tacho_kind
          <select
            aria-label="tacho_kind office card"
            className="mt-1 h-9 w-full rounded border px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {TACHO_KINDS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </label>
      </div>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref tacho office"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button
        disabled={!props.organizationId || save.isPending}
        type="submit"
        variant="ghost"
      >
        Zapisz tacho office
      </Button>
    </form>
  )
}
