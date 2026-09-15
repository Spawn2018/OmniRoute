import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildShipperAwardMarkWrite, saveShipperAwardMark } from "@/lib/shipper-award-marks-api"

const CHOICES = ["go", "hold", "no_award", "other"] as const

export function ShipperAwardMarkSave(args: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("shipper_award_go_01")
  const [award, setAward] = useState("go")
  const [ref, setRef] = useState("fixture://shipper-award-mark/")
  const save = useMutation({
    mutationFn: () => saveShipperAwardMark(buildShipperAwardMarkWrite(code, award, ref)),
    onSuccess: () => {
      setCode("shipper_award_go_01")
      setAward("go")
      setRef("fixture://shipper-award-mark/")
      void qc.invalidateQueries({ queryKey: ["shipper-award-marks", args.organizationId] })
    },
  })

  return (
    <form
      className="grid max-w-lg gap-3"
      data-shipper-award-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Decyzja award załadowcy jako HITL — bez Alpega i bez SQL auto-award.
      </p>
      <label className="grid gap-1 text-xs">
        Kod
        <input
          aria-label="Kod award załadowcy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>award_kind</legend>
        {CHOICES.map((token) => (
          <label key={token} className="flex gap-2">
            <input
              checked={award === token}
              name="award-kind"
              onChange={() => setAward(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie award"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz award
      </Button>
    </form>
  )
}
