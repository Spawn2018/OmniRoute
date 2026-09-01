import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"

type HitlPdfViewerProps = {
  pdfBase64: string
  highlightTexts: readonly string[]
}

type OverlayBox = {
  left: number
  top: number
  width: number
  height: number
}

export default function HitlPdfViewer({ pdfBase64, highlightTexts }: HitlPdfViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [page, setPage] = useState(1)
  const [pageCount, setPageCount] = useState(1)
  const [boxes, setBoxes] = useState<OverlayBox[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function renderPage(): Promise<void> {
      const pdfjs = await import("pdfjs-dist")
      const worker = await import("pdfjs-dist/build/pdf.worker.min.mjs?url")
      pdfjs.GlobalWorkerOptions.workerSrc = worker.default
      const bytes = Uint8Array.from(atob(pdfBase64), (ch) => ch.charCodeAt(0))
      const pdf = await pdfjs.getDocument({ data: bytes }).promise
      if (cancelled) {
        return
      }
      const current = Math.min(Math.max(page, 1), pdf.numPages)
      setPageCount(pdf.numPages)
      const pdfPage = await pdf.getPage(current)
      const viewport = pdfPage.getViewport({ scale: 1.15 })
      const canvas = canvasRef.current
      if (canvas === null) {
        return
      }
      canvas.width = viewport.width
      canvas.height = viewport.height
      const canvasContext = canvas.getContext("2d")
      if (canvasContext === null) {
        return
      }
      await pdfPage.render({ canvas, canvasContext, viewport }).promise
      const content = await pdfPage.getTextContent()
      const needles = highlightTexts.filter((text) => text.length > 0)
      const next: OverlayBox[] = []
      for (const item of content.items) {
        if (!("str" in item) || typeof item.str !== "string" || !("transform" in item)) {
          continue
        }
        if (!needles.some((needle) => item.str.includes(needle))) {
          continue
        }
        const transform = item.transform as number[]
        const [vx, vy] = viewport.convertToViewportPoint(transform[4] ?? 0, transform[5] ?? 0)
        const height = Math.abs((transform[3] ?? 8) * viewport.scale)
        const width = "width" in item && typeof item.width === "number" ? item.width * viewport.scale : 24
        next.push({ left: vx, top: vy - height, width, height })
      }
      if (!cancelled) {
        setBoxes(next)
        setError(null)
      }
    }

    void renderPage().catch(() => {
      if (!cancelled) {
        setError("Nie udało się pokazać PDF")
      }
    })
    return () => {
      cancelled = true
    }
  }, [highlightTexts, page, pdfBase64])

  if (error !== null) {
    return <p className="text-xs text-destructive">{error}</p>
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <Button
          type="button"
          size="sm"
          variant="outline"
          disabled={page <= 1}
          onClick={() => setPage((current) => current - 1)}
        >
          Poprzednia
        </Button>
        <span>
          Strona {page} / {pageCount}
        </span>
        <Button
          type="button"
          size="sm"
          variant="outline"
          disabled={page >= pageCount}
          onClick={() => setPage((current) => current + 1)}
        >
          Następna
        </Button>
      </div>
      <div className="relative max-h-80 overflow-auto">
        <canvas ref={canvasRef} className="block max-w-full" />
        {boxes.map((box, index) => (
          <span
            key={`${box.left}-${box.top}-${index}`}
            data-hitl-span="pdf"
            className="pointer-events-none absolute bg-accent/30"
            style={{
              left: box.left,
              top: box.top,
              width: box.width,
              height: box.height,
            }}
          />
        ))}
      </div>
    </div>
  )
}
