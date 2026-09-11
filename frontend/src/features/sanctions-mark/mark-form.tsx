import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildSanctionsMarkWrite, saveSanctionsMark } from "@/lib/sanctions-marks-api"

const LISTS = [
  { id: "ofac", title: "OFAC" },
  { id: "eu", title: "EU consolidated" },
  { id: "un", title: "UN Security Council" },
  { id: "other", title: "other" },
] as const

export function SanctionsMarkEditor(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [markCode, setMarkCode] = useState("ofac_01")
  const [listKind, setListKind] = useState("ofac")
  const [sourceRef, setSourceRef] = useState("fixture://sanctions-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveSanctionsMark(
        buildSanctionsMarkWrite({ code: markCode, kind: listKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("ofac_01")
      setListKind("ofac")
      setSourceRef("fixture://sanctions-mark/")
      void client.invalidateQueries({ queryKey: ["sanctions-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex max-w-md flex-col gap-3"
      data-sanctions-mark="editor"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Etykieta listy sankcji w katalogu HITL. Bez live scrape i bez screeningu HTTP.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika sanctions"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(event) => setMarkCode(event.target.value)}
          required
          value={markCode}
        />
      </label>
      <label className="grid gap-1 text-xs">
        list_kind
        <select
          aria-label="Rodzaj listy sankcji"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(event) => setListKind(event.target.value)}
          value={listKind}
        >
          {LISTS.map((row) => (
            <option key={row.id} value={row.id}>
              {row.title}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://sanctions-mark/…)"
        ariaLabel="Pochodzenie znacznika sanctions"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit">
        Zapisz sanctions
      </Button>
    </form>
  )
}
