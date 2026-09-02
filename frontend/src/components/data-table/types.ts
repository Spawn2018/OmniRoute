export type TableDensity = "compact" | "comfortable" | "condensed"

export type TableViewConfig = {
  column_order: string[]
  column_visibility: Record<string, boolean>
  filters: Record<string, string>
  sorting: Array<{ id: string; desc: string }>
  density: TableDensity
}

export type TableViewRecord = {
  id: string
  organization_id: string
  user_id: string
  table_key: string
  name: string
  config: TableViewConfig
}

export const DEFAULT_TABLE_VIEW_CONFIG: TableViewConfig = {
  column_order: [],
  column_visibility: {},
  filters: {},
  sorting: [],
  density: "compact",
}

export function resolveTableDensity(raw: string | undefined, allowCondensed: boolean): TableDensity {
  if (raw === "comfortable") {
    return "comfortable"
  }
  if (raw === "condensed" && allowCondensed) {
    return "condensed"
  }
  return "compact"
}

export function rowPadClass(density: TableDensity): string {
  if (density === "condensed") {
    return "py-0.5"
  }
  if (density === "compact") {
    return "py-1"
  }
  return "py-2"
}

export function rowEstimatePx(density: TableDensity): number {
  if (density === "condensed") {
    return 24
  }
  if (density === "compact") {
    return 32
  }
  return 40
}

export function mergeColumnOrder(preferred: string[], allIds: string[]): string[] {
  const remaining = new Set(allIds)
  const ordered: string[] = []
  for (const id of preferred) {
    if (remaining.has(id)) {
      ordered.push(id)
      remaining.delete(id)
    }
  }
  for (const id of allIds) {
    if (remaining.has(id)) {
      ordered.push(id)
    }
  }
  return ordered
}
