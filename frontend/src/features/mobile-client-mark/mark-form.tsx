import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createMobileClientMark,
  makeMobileClientMarkPayload,
} from "@/lib/mobile-client-marks-api"

const CLIENT_KINDS = [
  { value: "ios", label: "iOS" },
  { value: "android", label: "Android" },
  { value: "ota", label: "OTA" },
  { value: "other", label: "Inne" },
] as const

export function MobileClientMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("mcm_ios_01")
  const [kind, setKind] = useState("ios")
  const [ref, setRef] = useState("fixture://mobile-client-mark/")
  const save = useMutation({
    mutationFn: () => createMobileClientMark(makeMobileClientMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("mcm_ios_01")
      setKind("ios")
      setRef("fixture://mobile-client-mark/")
      void qc.invalidateQueries({ queryKey: ["mobile-client-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-mcm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code mobile client"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        client_kind
        <select
          aria-label="client_kind ios android ota"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {CLIENT_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref mobile client"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik klienta mobilnego
      </Button>
    </form>
  )
}
