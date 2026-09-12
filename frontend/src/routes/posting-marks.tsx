import { createFileRoute } from "@tanstack/react-router"
import { PostingMarkBoard } from "@/features/posting-mark/catalog-page"

export const Route = createFileRoute("/posting-marks")({
  component: PostingMarkBoard,
})
