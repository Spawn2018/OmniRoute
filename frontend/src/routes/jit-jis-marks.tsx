import { createFileRoute } from "@tanstack/react-router"
import { JitJisBoard } from "@/features/jit-jis-mark/catalog-page"

export const Route = createFileRoute("/jit-jis-marks")({
  component: JitJisBoard,
})
