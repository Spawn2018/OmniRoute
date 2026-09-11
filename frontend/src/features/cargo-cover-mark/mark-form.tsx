import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCargoCoverMarkWrite, saveCargoCoverMark } from "@/lib/cargo-cover-marks-api"

const COVER_KINDS = [
  { token: "cargo", caption: "ładunek (cargo)" },
  { token: "liability", caption: "odpowiedzialność (liability)" },
  { token: "policy", caption: "polisa (policy)" },
  { token: "other", caption: "inny (other)" },
] as const

export function CargoCoverMarkForm(props: { organizationId: string | null }) {
  const queryClient = useQueryClient()
  const [code, setCode] = useState("cargo_01")
  const [cover, setCover] = useState("cargo")
  const [origin, setOrigin] = useState("fixture://cargo-cover-mark/")
  const mutation = useMutation({
    mutationFn: () =>
      saveCargoCoverMark(buildCargoCoverMarkWrite({ code, kind: cover, origin })),
    onSuccess: () => {
      setCode("cargo_01")
      setCover("cargo")
      setOrigin("fixture://cargo-cover-mark/")
      void queryClient.invalidateQueries({
        queryKey: ["cargo-cover-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-cargo-cover-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik cover ładunku jako dana HITL. Bez live insurance i bez kwoty polisy.
      </p>
      <label className="grid gap-1 text-xs">
        Kod cover (snake 2–32)
        <input
          aria-label="Kod znacznika cargo cover"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(event) => setCode(event.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        cover_kind
        <select
          aria-label="Rodzaj cargo cover"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(event) => setCover(event.target.value)}
          value={cover}
        >
          {COVER_KINDS.map((entry) => (
            <option key={entry.token} value={entry.token}>
              {entry.caption}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://cargo-cover-mark/…)"
        ariaLabel="Pochodzenie znacznika cargo cover"
        value={origin}
        onChange={setOrigin}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit">
        Zapisz cargo cover
      </Button>
    </form>
  )
}
