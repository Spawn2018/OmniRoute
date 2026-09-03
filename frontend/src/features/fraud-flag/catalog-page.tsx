import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listFraudFlags, saveFraudFlag } from "@/lib/fraud-flags-api"
import { getTenantContext } from "@/lib/tenant"

const KINDS = ["billing", "document", "other"] as const

function readFlagForm(form: HTMLFormElement) {
  const box = new FormData(form)
  const text = (key: string) => String(box.get(key) ?? "").trim()
  return {
    party_id: text("party_id"),
    flag_kind: text("flag_kind"),
    source_ref: text("source_ref"),
  }
}

function FlagFields() {
  return (
    <ol className="flex flex-wrap gap-3 p-0">
      <li>
        <input className="w-56 border px-1 text-xs" name="party_id" required />
      </li>
      <li>
        <select className="border px-1 text-xs" defaultValue="billing" name="flag_kind">
          {KINDS.map((kind) => (
            <option key={kind} value={kind}>
              {kind}
            </option>
          ))}
        </select>
      </li>
      <li>
        <input className="w-56 border px-1 text-xs" defaultValue="fixture://fraud-flag/" name="source_ref" required />
      </li>
      <li>
        <Button type="submit">Zapisz flagę</Button>
      </li>
    </ol>
  )
}

function FlagSaveForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const save = useMutation({
    mutationFn: saveFraudFlag,
    onSuccess: () => {
      void client.invalidateQueries({ queryKey: ["fraud-flags", args.organizationId] })
    },
  })
  return (
    <form
      data-fraud-flag="form"
      onSubmit={(event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const form = event.currentTarget
        save.mutate(readFlagForm(form), { onSuccess: () => form.reset() })
      }}
    >
      <fieldset disabled={save.isPending || !args.organizationId}>
        <FlagFields />
      </fieldset>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}


function FlagRows(args: { organizationId: string | null }) {
  const rows = useQuery({
    queryKey: ["fraud-flags", args.organizationId],
    queryFn: listFraudFlags,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <ul data-fraud-flag="rows">
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="text-xs">
            {row.flag_kind} {row.party_id}{" "}
            <Link className="underline" to="/parties">
              kontrahent
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function FraudFlagPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  return (
    <section className="flex flex-col gap-3" data-fraud-flag="board">
      <CatalogHeading
        title="Oszustwo"
        subtitle="fraud_flag M-54 · tabela na kontrahencie · nie kwota · nie scoring osoby"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <FlagSaveForm organizationId={ctx.organizationId} /> : null}
      {ready ? <FlagRows organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
