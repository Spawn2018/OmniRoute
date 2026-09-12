import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createNamedPlaceMark,
  makeNamedPlaceMarkPayload,
} from "@/lib/named-place-marks-api"

const TERMS_VERSIONS = [
  { value: "2020", label: "Incoterms 2020" },
  { value: "2010", label: "Incoterms 2010" },
] as const

export function NamedPlaceMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("npm_dap_waw")
  const [place, setPlace] = useState("Warszawa")
  const [version, setVersion] = useState("2020")
  const [ref, setRef] = useState("fixture://named-place-mark/")
  const save = useMutation({
    mutationFn: () =>
      createNamedPlaceMark(makeNamedPlaceMarkPayload(code, place, version, ref)),
    onSuccess: () => {
      setCode("npm_dap_waw")
      setPlace("Warszawa")
      setVersion("2020")
      setRef("fixture://named-place-mark/")
      void qc.invalidateQueries({
        queryKey: ["named-place-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-npm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code named place"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        named_place
        <input
          aria-label="named_place text"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setPlace(e.target.value)}
          required
          value={place}
        />
      </label>
      <label className="text-xs">
        terms_version
        <select
          aria-label="terms_version 2020 or 2010"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setVersion(e.target.value)}
          value={version}
        >
          {TERMS_VERSIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref named place"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik miejsca nazwanego
      </Button>
    </form>
  )
}
