import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createMailAcceptMark,
  makeMailAcceptMarkPayload,
} from "@/lib/mail-accept-marks-api"

const ACCEPT_KINDS = [
  { value: "mailto", label: "Mailto" },
  { value: "confirm", label: "Confirm" },
  { value: "reject", label: "Reject" },
  { value: "other", label: "Inne" },
] as const

export function MailAcceptMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("mac_mailto_01")
  const [kind, setKind] = useState("mailto")
  const [ref, setRef] = useState("fixture://mail-accept-mark/")
  const save = useMutation({
    mutationFn: () => createMailAcceptMark(makeMailAcceptMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("mac_mailto_01")
      setKind("mailto")
      setRef("fixture://mail-accept-mark/")
      void qc.invalidateQueries({ queryKey: ["mail-accept-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-rose-700/30 bg-rose-50/20 p-3 dark:bg-rose-950/10"
      data-mac="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code mail accept"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        accept_kind
        <select
          aria-label="accept_kind mailto confirm reject"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {ACCEPT_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref mail accept"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz accept
      </Button>
    </form>
  )
}
