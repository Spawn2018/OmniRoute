import { createFileRoute } from "@tanstack/react-router"
import { LanguageCodeMarkBoard } from "@/features/language-code-mark/catalog-page"

export const Route = createFileRoute("/language-code-marks")({
  component: LanguageCodeMarkBoard,
})
