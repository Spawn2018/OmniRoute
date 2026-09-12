import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createOffboardingMark,
  makeOffboardingPayload,
} from "@/lib/offboarding-marks-api"

const OFFBOARD_KINDS = [
  { key: "offboard", tip: "offboard" },
  { key: "export", tip: "export danych" },
  { key: "revoke", tip: "revoke dostepu" },
  { key: "other", tip: "inny" },
] as const

export function OffboardingComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("ob_export_01")
  const [kind, setKind] = useState("export")
  const [ref, setRef] = useState("fixture://offboarding-mark/")
  const write = useMutation({
    mutationFn: () =>
      createOffboardingMark(makeOffboardingPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ob_export_01")
      setKind("export")
      setRef("fixture://offboarding-mark/")
      void client.invalidateQueries({
        queryKey: ["offboarding-marks", props.organizationId],
      })
    },
  })

  return (
    <aside className="bg-muted/15 p-3" data-ob="composer">
      <h2 className="text-sm font-semibold">Znacznik offboarding (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Tryb offboardingu. Bez wipe ciphertext i bez kasowania konta.
      </p>
      <form
        className="grid gap-2"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) write.mutate()
        }}
      >
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code offboard"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          offboard_kind
          <select
            aria-label="offboard_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {OFFBOARD_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref offboard"
          value={ref}
          onChange={setRef}
        />
        {write.error ? <CatalogError error={write.error} /> : null}
        <Button disabled={!props.organizationId || write.isPending} type="submit">
          Zapisz znacznik offboarding
        </Button>
      </form>
    </aside>
  )
}
