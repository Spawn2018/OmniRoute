import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import type { TableViewRecord } from "@/components/data-table/types"

type ViewManagerProps = {
  views: TableViewRecord[]
  activeViewId: string | null
  draftName: string
  onDraftNameChange: (name: string) => void
  onSelectView: (viewId: string) => void
  onSave: () => void
  onReset: () => void
  busy?: boolean
}

export function ViewManager({
  views,
  activeViewId,
  draftName,
  onDraftNameChange,
  onSelectView,
  onSave,
  onReset,
  busy = false,
}: ViewManagerProps) {
  return (
    <div className="flex flex-wrap items-end gap-2">
      <label className="space-y-1">
        <span className="text-xs text-muted-foreground">Widok</span>
        <select
          className="flex h-8 min-w-40 rounded-md border border-input bg-card px-2 text-sm"
          value={activeViewId ?? ""}
          onChange={(e) => {
            if (e.target.value) {
              onSelectView(e.target.value)
            }
          }}
        >
          <option value="">Bieżący (niezapisany)</option>
          {views.map((view) => (
            <option key={view.id} value={view.id}>
              {view.name}
            </option>
          ))}
        </select>
      </label>
      <label className="space-y-1">
        <span className="text-xs text-muted-foreground">Nazwa przy zapisie</span>
        <Input
          value={draftName}
          onChange={(e) => onDraftNameChange(e.target.value)}
          placeholder="np. Operacyjny"
          className="h-8 w-44"
        />
      </label>
      <Button type="button" size="sm" onClick={onSave} disabled={busy || !draftName.trim()}>
        Zapisz widok
      </Button>
      <Button type="button" size="sm" variant="outline" onClick={onReset} disabled={busy}>
        Reset
      </Button>
    </div>
  )
}
