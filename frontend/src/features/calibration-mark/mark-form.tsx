import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCalibrationWrite, saveCalibrationMark } from "@/lib/calibration-marks-api"

const KINDS = ["ready", "pending"] as const

export function CalibrationMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("sample_pl_01")
  const [kind, setKind] = useState<string>("ready")
  const [origin, setOrigin] = useState("fixture://calibration-mark/")
  const save = useMutation({
    mutationFn: () => saveCalibrationMark(buildCalibrationWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("sample_pl_01")
      setKind("ready")
      setOrigin("fixture://calibration-mark/")
      void cache.invalidateQueries({ queryKey: ["calibration-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-calibration-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Gotowość próbki jako katalog HITL. Bez MAE SQL i bez float.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika kalibracji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Gotowość próbki</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="calibration-ready"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://calibration-mark/…)"
        ariaLabel="Pochodzenie znacznika kalibracji"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik kalibracji
      </Button>
    </form>
  )
}
