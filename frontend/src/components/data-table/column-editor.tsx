import {
  DndContext,
  PointerSensor,
  closestCenter,
  type DragEndEvent,
  useSensor,
  useSensors,
} from "@dnd-kit/core"
import {
  SortableContext,
  arrayMove,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { GripVertical } from "lucide-react"
import { cn } from "@/lib/utils"

type ColumnEditorProps = {
  columnIds: string[]
  labels: Record<string, string>
  visibility: Record<string, boolean>
  onVisibilityChange: (columnId: string, visible: boolean) => void
  onOrderChange: (orderedIds: string[]) => void
}

function SortableColumnRow({
  id,
  label,
  visible,
  onVisibilityChange,
}: {
  id: string
  label: string
  visible: boolean
  onVisibilityChange: (columnId: string, visible: boolean) => void
}) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id,
  })

  return (
    <div
      ref={setNodeRef}
      style={{ transform: CSS.Transform.toString(transform), transition }}
      className={cn(
        "flex items-center gap-2 rounded-md border border-border bg-card px-2 py-1.5",
        isDragging && "opacity-70",
      )}
    >
      <button
        type="button"
        className="text-muted-foreground hover:text-foreground"
        aria-label={`Przeciągnij kolumnę ${label}`}
        {...attributes}
        {...listeners}
      >
        <GripVertical className="size-3.5" />
      </button>
      <label className="flex flex-1 items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={visible}
          onChange={(e) => onVisibilityChange(id, e.target.checked)}
        />
        <span>{label}</span>
      </label>
    </div>
  )
}

export function ColumnEditor({
  columnIds,
  labels,
  visibility,
  onVisibilityChange,
  onOrderChange,
}: ColumnEditorProps) {
  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 4 } }))

  function onDragEnd(event: DragEndEvent) {
    const { active, over } = event
    if (!over || active.id === over.id) {
      return
    }
    const oldIndex = columnIds.indexOf(String(active.id))
    const newIndex = columnIds.indexOf(String(over.id))
    if (oldIndex < 0 || newIndex < 0) {
      return
    }
    onOrderChange(arrayMove(columnIds, oldIndex, newIndex))
  }

  return (
    <div className="space-y-2">
      <div className="text-xs font-medium text-muted-foreground">Kolumny (widoczność + kolejność)</div>
      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={onDragEnd}>
        <SortableContext items={columnIds} strategy={verticalListSortingStrategy}>
          <div className="space-y-1">
            {columnIds.map((id) => (
              <SortableColumnRow
                key={id}
                id={id}
                label={labels[id] ?? id}
                visible={visibility[id] !== false}
                onVisibilityChange={onVisibilityChange}
              />
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  )
}
