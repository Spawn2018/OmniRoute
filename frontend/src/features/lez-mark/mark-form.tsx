import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createLezMark, makeLezMarkPayload } from "@/lib/lez-marks-api"

const LEZ_KINDS = [
  { value: "lez", label: "LEZ" },
  { value: "ban", label: "Zakaz" },
  { value: "zone", label: "Strefa" },
  { value: "other", label: "Inne" },
] as const

export function LezMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("lz_manual_01")
  const [kind, setKind] = useState("lez")
  const [ref, setRef] = useState("fixture://lez-mark/")
  const save = useMutation({
    mutationFn: () => createLezMark(makeLezMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("lz_manual_01")
      setKind("lez")
      setRef("fixture://lez-mark/")
      void qc.invalidateQueries({ queryKey: ["lez-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="grid gap-2 rounded border border-emerald-700/40 bg-background p-3 md:grid-cols-3"
      data-lz="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="md:col-span-3 text-sm font-medium">Nowy znacznik LEZ</p>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code lez"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        lez_kind
        <select
          aria-label="lez_kind lez ban"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {LEZ_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <div className="md:col-span-3">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref lez"
          value={ref}
          onChange={setRef}
        />
      </div>
      {save.error ? (
        <div className="md:col-span-3">
          <CatalogError error={save.error} />
        </div>
      ) : null}
      <Button
        className="md:col-span-3 md:justify-self-start"
        disabled={!props.organizationId || save.isPending}
        type="submit"
        variant="outline"
      >
        Zapisz LEZ
      </Button>
    </form>
  )
}
