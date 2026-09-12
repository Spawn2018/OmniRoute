import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createLanguageCodeMark,
  makeLanguageCodeMarkPayload,
} from "@/lib/language-code-marks-api"

const LOCALE_KINDS = [
  { value: "pl", label: "PL" },
  { value: "en", label: "EN" },
  { value: "de", label: "DE" },
  { value: "other", label: "Inne" },
] as const

export function LanguageCodeMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("lcm_pl_docs")
  const [kind, setKind] = useState("pl")
  const [ref, setRef] = useState("fixture://language-code-mark/")
  const save = useMutation({
    mutationFn: () =>
      createLanguageCodeMark(makeLanguageCodeMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("lcm_pl_docs")
      setKind("pl")
      setRef("fixture://language-code-mark/")
      void qc.invalidateQueries({
        queryKey: ["language-code-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-lcm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code language code"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        locale_kind
        <select
          aria-label="locale_kind pl en de other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {LOCALE_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref language code"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik kodu jezyka
      </Button>
    </form>
  )
}
