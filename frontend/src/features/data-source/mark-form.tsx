import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildDataSourceWrite,
  saveDataSource,
} from "@/lib/data-sources-api"

export function DataSourceSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ds_openmeteo_01")
  const [license, setLicense] = useState("CC-BY-4.0")
  const [rights, setRights] = useState("weather read-only")
  const [origin, setOrigin] = useState("fixture://data-source/")
  const save = useMutation({
    mutationFn: () =>
      saveDataSource(
        buildDataSourceWrite({ code, license, rights, origin }),
      ),
    onSuccess: () => {
      setCode("ds_openmeteo_01")
      setLicense("CC-BY-4.0")
      setRights("weather read-only")
      setOrigin("fixture://data-source/")
      void cache.invalidateQueries({
        queryKey: ["data-sources", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-data-source="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL slownik zrodla danych (kod + licencja + zakres praw). Live ingest i
        22 dostepy bez bramy zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://data-source/…)"
        ariaLabel="Pochodzenie zrodla danych"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod zrodla (snake 2–32)</span>
        <input
          aria-label="Kod zrodla danych"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Etykieta licencji (2–64)</span>
        <input
          aria-label="Etykieta licencji"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setLicense(change.target.value)}
          required
          value={license}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Zakres praw (2–128)</span>
        <input
          aria-label="Zakres praw"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setRights(change.target.value)}
          required
          value={rights}
        />
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz zrodlo danych
      </Button>
    </form>
  )
}
