import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildExtractionPromptMarkWrite, saveExtractionPromptMark } from "@/lib/extraction-prompt-marks-api"

const CHOICES = ["extract", "system", "other"] as const

export function ExtractionPromptMarkSave(args: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("extract_prompt_01")
  const [kind, setKind] = useState("extract")
  const [ref, setRef] = useState("fixture://extraction-prompt-mark/")
  const save = useMutation({
    mutationFn: () => saveExtractionPromptMark(buildExtractionPromptMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("extract_prompt_01")
      setKind("extract")
      setRef("fixture://extraction-prompt-mark/")
      void qc.invalidateQueries({ queryKey: ["extraction-prompt-marks", args.organizationId] })
    },
  })

  return (
    <form
      className="grid max-w-lg gap-3"
      data-extraction-prompt-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wersja promptu ekstrakcji jako HITL — bez Instructor i bez bajtów w bazie.
      </p>
      <label className="grid gap-1 text-xs">
        Kod
        <input
          aria-label="Kod promptu ekstrakcji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        prompt_kind
        <select
          aria-label="Rodzaj promptu"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {CHOICES.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie promptu"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz prompt
      </Button>
    </form>
  )
}
