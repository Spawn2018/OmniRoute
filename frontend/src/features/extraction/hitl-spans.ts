import type { ExtractionCandidate } from "@/lib/extractions-api"

export type HitlTextSpan = {
  start: number
  end: number
  text: string
}

function nextMatch(haystack: string, needle: string, from: number): HitlTextSpan | null {
  if (needle.length === 0) {
    return null
  }
  const start = haystack.indexOf(needle, from)
  if (start < 0) {
    return null
  }
  return { start, end: start + needle.length, text: needle }
}

export function hitlPreviewSpans(preview: string, candidates: ExtractionCandidate[]): HitlTextSpan[] {
  const spans: HitlTextSpan[] = []
  const occupied: Array<{ start: number; end: number }> = []

  function overlaps(start: number, end: number): boolean {
    return occupied.some((span) => start < span.end && end > span.start)
  }

  for (const candidate of candidates) {
    for (const needle of [candidate.code, candidate.amount_text, candidate.currency]) {
      let from = 0
      while (from < preview.length) {
        const match = nextMatch(preview, needle, from)
        if (match === null) {
          break
        }
        if (!overlaps(match.start, match.end)) {
          spans.push(match)
          occupied.push(match)
          break
        }
        from = match.end
      }
    }
  }
  return spans.sort((a, b) => a.start - b.start)
}

export function hitlPreviewSegments(
  preview: string,
  spans: HitlTextSpan[],
): Array<{ text: string; highlight: boolean }> {
  const segments: Array<{ text: string; highlight: boolean }> = []
  let cursor = 0
  for (const span of spans) {
    if (span.start > cursor) {
      segments.push({ text: preview.slice(cursor, span.start), highlight: false })
    }
    segments.push({ text: preview.slice(span.start, span.end), highlight: true })
    cursor = span.end
  }
  if (cursor < preview.length) {
    segments.push({ text: preview.slice(cursor), highlight: false })
  }
  return segments
}

export function isPdfBase64(documentBase64: string): boolean {
  try {
    const head = atob(documentBase64.slice(0, 24))
    return head.startsWith("%PDF")
  } catch {
    return false
  }
}
