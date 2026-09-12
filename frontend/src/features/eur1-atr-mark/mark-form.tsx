import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createEur1AtrMark, makeEur1AtrPayload } from "@/lib/eur1-atr-marks-api"

const CERT_OPTIONS = [
  { value: "eur1", label: "EUR.1 — swiadectwo ruchu" },
  { value: "atr", label: "ATR — Turcja / unia celna" },
  { value: "origin", label: "origin — deklaracja pochodzenia" },
  { value: "other", label: "other — pozostale" },
] as const

const EMPTY_CODE = "eur1_manual_01"
const EMPTY_REF = "tenant:manual://eur1-atr/"

export function Eur1AtrComposer(props: { organizationId: string | null }) {
  const queryClient = useQueryClient()
  const [markCode, setMarkCode] = useState(EMPTY_CODE)
  const [certKind, setCertKind] = useState<string>("eur1")
  const [sourceRef, setSourceRef] = useState(EMPTY_REF)

  const save = useMutation({
    mutationFn: () => createEur1AtrMark(makeEur1AtrPayload(markCode, certKind, sourceRef)),
    onSuccess: () => {
      setMarkCode(EMPTY_CODE)
      setCertKind("eur1")
      setSourceRef(EMPTY_REF)
      void queryClient.invalidateQueries({
        queryKey: ["eur1-atr-marks", props.organizationId],
      })
    },
  })

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!props.organizationId) return
    save.mutate()
  }

  return (
    <fieldset className="rounded-lg border bg-muted/20 p-4">
      <legend className="px-1 text-sm font-semibold">Nowy wpis EUR.1 / ATR</legend>
      <form className="mt-2 grid gap-3 md:grid-cols-2" data-eur1="composer" onSubmit={onSubmit}>
        <p className="md:col-span-2 text-xs text-muted-foreground">
          Zapis HITL. Zakaz EUR.1 live i ATR scrape.
        </p>
        <label className="flex flex-col gap-1 text-xs">
          <span>mark_code</span>
          <input
            aria-label="mark_code swiadectwa"
            className="h-9 rounded-md border bg-background px-2 font-mono text-sm"
            onChange={(event) => setMarkCode(event.target.value)}
            required
            value={markCode}
          />
        </label>
        <label className="flex flex-col gap-1 text-xs">
          <span>cert_kind</span>
          <select
            aria-label="cert_kind swiadectwa"
            className="h-9 rounded-md border bg-background px-2 text-sm"
            onChange={(event) => setCertKind(event.target.value)}
            value={certKind}
          >
            {CERT_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
        <div className="md:col-span-2">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref swiadectwa"
            value={sourceRef}
            onChange={setSourceRef}
          />
        </div>
        {save.error ? (
          <div className="md:col-span-2">
            <CatalogError error={save.error} />
          </div>
        ) : null}
        <div className="md:col-span-2">
          <Button disabled={!props.organizationId || save.isPending} type="submit">
            Dodaj swiadectwo do katalogu
          </Button>
        </div>
      </form>
    </fieldset>
  )
}
