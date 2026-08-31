import { MAIN_CONTENT_ID, SKIP_TO_MAIN_LABEL } from "@/lib/a11y"

export function SkipToMain() {
  return (
    <a
      href={`#${MAIN_CONTENT_ID}`}
      className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:rounded-md focus:border focus:border-border focus:bg-card focus:px-3 focus:py-1.5 focus:text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    >
      {SKIP_TO_MAIN_LABEL}
    </a>
  )
}
