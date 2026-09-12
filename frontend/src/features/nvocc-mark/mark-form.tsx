import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createNvoccMark,
  makeNvoccMarkPayload,
} from "@/lib/nvocc-marks-api"

const ROLE_CHOICES = [
  { value: "nvocc", label: "NVOCC" },
  { value: "house", label: "House B/L" },
  { value: "master", label: "Master B/L" },
  { value: "other", label: "Inne" },
] as const

export function NvoccMarkComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [markCode, setMarkCode] = useState("nv_manual_01")
  const [role, setRole] = useState("nvocc")
  const [sourceRef, setSourceRef] = useState("fixture://nvocc-mark/")
  const save = useMutation({
    mutationFn: () =>
      createNvoccMark(makeNvoccMarkPayload(markCode, role, sourceRef)),
    onSuccess: () => {
      setMarkCode("nv_manual_01")
      setRole("nvocc")
      setSourceRef("fixture://nvocc-mark/")
      void client.invalidateQueries({
        queryKey: ["nvocc-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-3 rounded border border-dashed border-slate-600/40 p-4"
      data-nv="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <header>
        <h2 className="text-sm font-semibold tracking-wide">Dodaj rolę NVOCC</h2>
        <p className="text-[11px] text-muted-foreground">
          Tylko HITL — bez ocean live i bez flagi na party.
        </p>
      </header>
      <label className="block text-xs">
        mark_code
        <input
          aria-label="mark_code nvocc role"
          className="mt-1 h-9 w-full rounded-sm border border-slate-500/40 bg-background px-2 font-mono text-sm"
          onChange={(e) => setMarkCode(e.target.value)}
          required
          value={markCode}
        />
      </label>
      <label className="block text-xs">
        nvocc_kind
        <select
          aria-label="nvocc_kind house master"
          className="mt-1 h-9 w-full rounded-sm border border-slate-500/40 bg-background px-2 text-sm"
          onChange={(e) => setRole(e.target.value)}
          value={role}
        >
          {ROLE_CHOICES.map((choice) => (
            <option key={choice.value} value={choice.value}>
              {choice.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref nvocc role"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button
        disabled={!props.organizationId || save.isPending}
        type="submit"
        variant="outline"
      >
        Zapisz rolę NVOCC
      </Button>
    </form>
  )
}
