import { Link } from "@tanstack/react-router"
import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function TenantSessionNotice() {
  return (
    <div className="rounded-md border border-border bg-card p-3 text-sm">
      Ustaw identyfikatory sesji na stronie{" "}
      <Link className="underline" to="/session">
        Sesja
      </Link>
      .
    </div>
  )
}

export function CatalogError({ error }: { error: unknown }) {
  return (
    <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
      {(error as Error).message}
    </div>
  )
}

export function CatalogHeading({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="banner">
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </div>
  )
}

export function CatalogCreateForm({
  code,
  name,
  aliasesText,
  onCodeChange,
  onNameChange,
  onAliasesChange,
  codeLabel,
  nameLabel,
  aliasesLabel,
  codePlaceholder,
  namePlaceholder,
  aliasesPlaceholder,
  submitLabel,
  pending,
  disabled,
  onSubmit,
}: {
  code: string
  name: string
  aliasesText: string
  onCodeChange: (value: string) => void
  onNameChange: (value: string) => void
  onAliasesChange: (value: string) => void
  codeLabel: string
  nameLabel: string
  aliasesLabel: string
  codePlaceholder: string
  namePlaceholder: string
  aliasesPlaceholder: string
  submitLabel: string
  pending: boolean
  disabled: boolean
  onSubmit: () => void
}) {
  return (
    <form
      className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-4"
      onSubmit={(event) => {
        event.preventDefault()
        onSubmit()
      }}
    >
      <Input
        aria-label={codeLabel}
        placeholder={codePlaceholder}
        value={code}
        onChange={(event) => onCodeChange(event.target.value)}
        required
      />
      <Input
        aria-label={nameLabel}
        placeholder={namePlaceholder}
        value={name}
        onChange={(event) => onNameChange(event.target.value)}
        required
      />
      <Input
        aria-label={aliasesLabel}
        placeholder={aliasesPlaceholder}
        value={aliasesText}
        onChange={(event) => onAliasesChange(event.target.value)}
      />
      <Button type="submit" disabled={pending || disabled}>
        {submitLabel}
      </Button>
    </form>
  )
}

export function CatalogLoadedTable<TData>({
  loading,
  error,
  data,
  tableKey,
  columns,
  columnLabels,
  globalFilterPlaceholder,
}: {
  loading: boolean
  error: unknown
  data: TData[] | undefined
  tableKey: string
  // TanStack ColumnDef: wariancja TValue — `any` tylko na granicy API tabeli.
  columns: ColumnDef<TData, any>[]
  columnLabels: Record<string, string>
  globalFilterPlaceholder: string
}) {
  if (loading) {
    return <div className="text-sm text-muted-foreground">Ładowanie…</div>
  }
  if (error) {
    return <CatalogError error={error} />
  }
  if (data === undefined) {
    return null
  }
  return (
    <DataTableShell
      tableKey={tableKey}
      columns={columns}
      data={data}
      columnLabels={columnLabels}
      globalFilterPlaceholder={globalFilterPlaceholder}
    />
  )
}

export function ResolveTokenForm({
  label,
  placeholder,
  pending,
  resolved,
  onResolve,
}: {
  label: string
  placeholder: string
  pending: boolean
  resolved: string | null
  onResolve: (token: string) => void
}) {
  const [token, setToken] = useState("")

  return (
    <form
      className="flex gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        onResolve(token)
      }}
    >
      <Input
        aria-label={label}
        placeholder={placeholder}
        value={token}
        onChange={(event) => setToken(event.target.value)}
      />
      <Button type="submit" variant="outline" disabled={pending || !token}>
        Rozwiąż
      </Button>
      {resolved ? <div className="self-center font-mono text-xs">{resolved}</div> : null}
    </form>
  )
}
