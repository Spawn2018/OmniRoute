import { Button } from "@/components/ui/button"
import type { OperatorDecideStatus } from "@/lib/operator-decisions-api"

export function DecideStatusButtons(args: {
  acceptLabel: string
  disabled?: boolean
  onDecide: (status: OperatorDecideStatus) => void
}) {
  return (
    <span className="flex flex-wrap gap-1">
      <Button
        type="button"
        disabled={args.disabled}
        onClick={() => args.onDecide("accepted")}
      >
        {args.acceptLabel}
      </Button>
      <Button type="button" disabled={args.disabled} onClick={() => args.onDecide("changed")}>
        Zmień
      </Button>
      <Button type="button" disabled={args.disabled} onClick={() => args.onDecide("rejected")}>
        Odrzuć
      </Button>
    </span>
  )
}
