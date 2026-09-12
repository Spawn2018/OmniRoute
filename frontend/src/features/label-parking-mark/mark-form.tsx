import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createLabelParkingMark,
  makeLabelParkingMarkPayload,
} from "@/lib/label-parking-marks-api"

const PARKING_KINDS = [
  { value: "secure", label: "Secure" },
  { value: "labeled", label: "Labeled" },
  { value: "other", label: "Inne" },
] as const

export function LabelParkingMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("lp_secure_01")
  const [kind, setKind] = useState("secure")
  const [ref, setRef] = useState("fixture://label-parking-mark/")
  const save = useMutation({
    mutationFn: () => createLabelParkingMark(makeLabelParkingMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("lp_secure_01")
      setKind("secure")
      setRef("fixture://label-parking-mark/")
      void qc.invalidateQueries({ queryKey: ["label-parking-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-3"
      data-lp="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="text-sm font-semibold tracking-tight">Nowy znacznik parkingu</p>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code label parking"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="space-y-1">
        <legend className="text-xs">parking_kind</legend>
        {PARKING_KINDS.map((opt) => (
          <label key={opt.value} className="flex items-center gap-2 text-sm">
            <input
              checked={kind === opt.value}
              name="parking_kind"
              onChange={() => setKind(opt.value)}
              type="radio"
              value={opt.value}
            />
            {opt.label}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref label parking"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="default">
        Zapisz parking
      </Button>
    </form>
  )
}
