import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCutoffMarkWrite, saveCutoffMark } from "@/lib/cutoff-marks-api"

const KINDS = [
  { value: "booking", label: "booking" },
  { value: "document", label: "document" },
  { value: "gate", label: "gate" },
  { value: "other", label: "other" },
] as const

export function CutoffMarkEditor(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("booking_01")
  const [kind, setKind] = useState("booking")
  const [origin, setOrigin] = useState("fixture://cutoff-mark/")
  const save = useMutation({
    mutationFn: () => saveCutoffMark(buildCutoffMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("booking_01")
      setKind("booking")
      setOrigin("fixture://cutoff-mark/")
      void qc.invalidateQueries({ queryKey: ["cutoff-marks", props.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-cutoff-mark="editor"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Cutoff rozdzielony jako etykieta HITL. Bez silnika cutoff i bez countdown.
      </p>
      <label className="grid gap-1 text-xs">
        Kod
        <input
          aria-label="Kod znacznika cutoff"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        cutoff_kind
        <select
          aria-label="Rodzaj cutoff"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {KINDS.map((row) => (
            <option key={row.value} value={row.value}>
              {row.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie cutoff"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit">
        Zapisz cutoff
      </Button>
    </form>
  )
}
