import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchOrganizationSettings,
  organizationSettingUpsertBody,
  upsertOrganizationSetting,
  type OrganizationSetting,
} from "@/lib/organization-settings-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<OrganizationSetting>()

const columns = [
  helper.accessor("setting_key", { header: "Klucz" }),
  helper.accessor("setting_value", { header: "Wartość" }),
]

const COLUMN_LABELS = {
  setting_key: "Klucz",
  setting_value: "Wartość",
}

export function OrganizationSettingCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [currency, setCurrency] = useState("EUR")
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["organization-settings", ctx.organizationId],
    queryFn: fetchOrganizationSettings,
    enabled: signedIn,
    retry: false,
  })

  const saveMutation = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "default_currency",
          settingValue: currency,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })

  return (
    <section className="space-y-3">
      <header>
        <h2 className="text-base font-semibold">Ustawienia tenanta</h2>
        <p className="text-xs text-muted-foreground">
          organization_setting M-03 · konfiguracja w bazie · nie env · nie sekrety
        </p>
      </header>

      {signedIn ? null : (
        <p className="text-sm">
          Najpierw ustaw tenant na stronie <Link className="underline" to="/session">Sesja</Link>.
        </p>
      )}

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveMutation.mutate()
        }}
      >
        <Input
          aria-label="Waluta domyślna ISO"
          placeholder="EUR"
          value={currency}
          onChange={(event) => setCurrency(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveMutation.isPending || !signedIn}>
          Zapisz walutę domyślną
        </Button>
      </form>

      {saveMutation.isError ? (
        <p className="text-sm text-destructive">{(saveMutation.error as Error).message}</p>
      ) : null}
      {query.isPending ? <p className="text-sm text-muted-foreground">Pobieranie ustawień…</p> : null}
      {query.isError ? <p className="text-sm text-destructive">{(query.error as Error).message}</p> : null}
      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.organizationSettings.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj ustawienia…"
        />
      ) : null}
    </section>
  )
}
