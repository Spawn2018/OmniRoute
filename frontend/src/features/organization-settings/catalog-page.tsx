import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
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
  const [prefix, setPrefix] = useState("OR-Q")
  const [template, setTemplate] = useState("plain")
  const [defaultN, setDefaultN] = useState("3")
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

  const savePrefix = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "quotation_number_prefix",
          settingValue: prefix,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })

  const saveDefaultN = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "inquiry_default_n",
          settingValue: defaultN,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveTemplate = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "quotation_print_template",
          settingValue: template,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Ustawienia tenanta"
        subtitle="organization_setting M-03 · konfiguracja w bazie · nie env · nie sekrety"
      />

      {signedIn ? null : <TenantSessionNotice />}

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

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          savePrefix.mutate()
        }}
      >
        <Input
          aria-label="Prefiks numeru oferty"
          placeholder="OR-Q"
          value={prefix}
          onChange={(event) => setPrefix(event.target.value)}
          required
        />
        <Button type="submit" disabled={savePrefix.isPending || !signedIn}>
          Zapisz prefiks numeru
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveTemplate.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          quotation_print_template
          <select
            aria-label="Szablon oferty"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={template}
            onChange={(event) => setTemplate(event.target.value)}
          >
            <option value="plain">plain</option>
            <option value="letter">letter</option>
          </select>
        </label>
        <Button type="submit" disabled={saveTemplate.isPending || !signedIn}>
          Zapisz szablon oferty
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveDefaultN.mutate()
        }}
      >
        <Input
          aria-label="Domyślna liczba zapytań"
          placeholder="3"
          value={defaultN}
          onChange={(event) => setDefaultN(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveDefaultN.isPending || !signedIn}>
          Zapisz inquiry_default_n
        </Button>
      </form>

      {saveMutation.isError ? <CatalogError error={saveMutation.error} /> : null}
      {savePrefix.isError ? <CatalogError error={savePrefix.error} /> : null}
      {saveTemplate.isError ? <CatalogError error={saveTemplate.error} /> : null}
      {saveDefaultN.isError ? <CatalogError error={saveDefaultN.error} /> : null}

      <CatalogLoadedTable
        loading={query.isLoading}
        error={query.error}
        data={query.data}
        tableKey={BUSINESS_LISTS.organizationSettings.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj ustawienia…"
      />
    </div>
  )
}
