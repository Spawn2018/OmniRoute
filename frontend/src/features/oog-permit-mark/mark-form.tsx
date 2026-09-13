import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { createOogPermitMark, makeOogPermitMarkPayload } from "@/lib/oog-permit-marks-api"

const PERMIT_KINDS = ["permit", "pilot", "route", "other"] as const

export function OogPermitMarkSave({ organizationId }: { organizationId: string | null }) {
  const queryClient = useQueryClient()
  const [code, setCode] = useState("opm_permit_01")
  const [kind, setKind] = useState("permit")
  const [origin, setOrigin] = useState("fixture://oog-permit-mark/")
  const write = useMutation({
    mutationFn: () => createOogPermitMark(makeOogPermitMarkPayload(code, kind, origin)),
    onSuccess: () => {
      setCode("opm_permit_01")
      setKind("permit")
      setOrigin("fixture://oog-permit-mark/")
      void queryClient.invalidateQueries({ queryKey: ["oog-permit-board", organizationId] })
    },
  })

  function submitPermit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (organizationId) write.mutate()
  }

  return (
    <form className="flex max-w-lg flex-col gap-4" data-oog-permit-mark="compose" onSubmit={submitPermit}>
      <p className="text-sm text-muted-foreground">
        Zezwolenie OOG to stance katalogu. Metry i urząd nie wchodzą do tego wiersza.
      </p>
      <label className="flex flex-col gap-1 text-sm">
        Kod zezwolenia (snake 2–32)
        <input
          aria-label="Kod znacznika zezwolenia OOG"
          className="h-9 rounded border px-2 font-mono"
          onChange={(event) => setCode(event.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Rodzaj zezwolenia
        <select
          aria-label="Rodzaj zezwolenia OOG"
          className="h-9 rounded border bg-background px-2"
          onChange={(event) => setKind(event.target.value)}
          value={kind}
        >
          {PERMIT_KINDS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://oog-permit-mark/…)"
        ariaLabel="Pochodzenie znacznika zezwolenia OOG"
        value={origin}
        onChange={setOrigin}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
      <button
        className="h-9 rounded border px-3 text-sm"
        disabled={!organizationId || write.isPending}
        type="submit"
      >
        Zapisz zezwolenie OOG
      </button>
    </form>
  )
}
