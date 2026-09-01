import {
  Button,
  Callout,
  Checkbox,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  TextArea,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type FieldState = "potwierdzone" | "niepewne" | "przetwarzanie";

type Candidate = {
  id: string;
  code: string;
  amount: string;
  currency: string;
  confidence: number;
  span: string;
  state: FieldState;
  selected: boolean;
};

const INITIAL: Candidate[] = [
  {
    id: "c1",
    code: "OFR",
    amount: "1850.00",
    currency: "USD",
    confidence: 0.94,
    span: "OCEAN FREIGHT USD 1,850 / 40HC",
    state: "potwierdzone",
    selected: true,
  },
  {
    id: "c2",
    code: "BAF",
    amount: "120.00",
    currency: "USD",
    confidence: 0.61,
    span: "BAF USD 120 subject to change",
    state: "niepewne",
    selected: true,
  },
  {
    id: "c3",
    code: "THC",
    amount: "145.00",
    currency: "EUR",
    confidence: 0.38,
    span: "THC origin EUR 145",
    state: "niepewne",
    selected: false,
  },
];

export default function UiHitl() {
  const [activeId, setActiveId] = useCanvasState("ui-04-active", "c2");
  const [busy, setBusy] = useCanvasState("ui-04-busy", false);
  const [rejectOpen, setRejectOpen] = useCanvasState("ui-04-reject", false);
  const [reason, setReason] = useCanvasState("ui-04-reason", "");
  const [rows, setRows] = useCanvasState<Candidate[]>("ui-04-rows", INITIAL);
  const [outcome, setOutcome] = useCanvasState<"draft" | "accepted" | "rejected">(
    "ui-04-outcome",
    "draft",
  );

  const active = rows.find((row) => row.id === activeId) ?? rows[0];
  const selectedCount = rows.filter((row) => row.selected).length;

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>HITL — PDF, spany, accept</H1>
        <Text tone="secondary">
          Obywatel pierwszej klasy, nie chatbot. Dziś split istnieje
          (`hitl-review-split.tsx`), brak confidence per pole, brak akcji
          zbiorczych, brak ścieżki odrzucenia z uzasadnieniem.
        </Text>
      </Stack>

      <Row gap={16} wrap>
        <Stat value="propozycja AI" label="Art. 50 — zawsze widoczna" />
        <Stat value={`${selectedCount}/${rows.length}`} label="zaznaczone do accept" />
        <Stat
          value={outcome}
          label="stan szkicu"
          tone={
            outcome === "accepted" ? "success" : outcome === "rejected" ? "danger" : "warning"
          }
        />
      </Row>

      <Callout tone="warning" title="Zasada 8 + HAX G10">
        Nic z ekstrakcji nie idzie do `rate_line` bez accept. Przy confidence
        &lt; 0.7 system dopytuje (disambiguation), nie zgaduje. Optimistic
        accept zakazany.
      </Callout>

      <Grid columns="1.1fr 1fr" gap={16}>
        <PdfPane activeSpan={active.span} />
        <Stack gap={12}>
          <Row gap={8} align="center">
            <H2>Recenzja kandydatów</H2>
            <Pill active size="sm">
              propozycja AI
            </Pill>
          </Row>
          <Text size="small" tone="secondary">
            source_ref `MAERSK-SHA-0926` · szkic `ed-4401` · nie zapisuj bez
            człowieka.
          </Text>
          {rows.map((row) => (
            <div key={row.id}>
              <CandidateRow
                row={row}
                active={row.id === activeId}
                onFocus={() => setActiveId(row.id)}
                onToggle={(checked) =>
                  setRows(
                    rows.map((item) =>
                      item.id === row.id ? { ...item, selected: checked } : item,
                    ),
                  )
                }
              />
            </div>
          ))}
          <Row gap={8} wrap>
            <Button
              variant="primary"
              disabled={busy || selectedCount === 0 || outcome !== "draft"}
              onClick={() => {
                setBusy(true);
                setOutcome("accepted");
                setBusy(false);
              }}
            >
              Akceptuj zaznaczone
            </Button>
            <Button
              variant="secondary"
              disabled={outcome !== "draft"}
              onClick={() => setRejectOpen(!rejectOpen)}
            >
              Odrzuć szkic
            </Button>
            <Button variant="ghost" disabled={outcome !== "draft"}>
              Zaznacz pewne ≥ 0.9
            </Button>
          </Row>
          {rejectOpen ? (
            <Stack gap={8}>
              <H3>Ścieżka odrzucenia</H3>
              <Text size="small">
                Powód obowiązkowy. Szkic zostaje w kolejce ze statusem
                rejected — nie kasujemy źródła.
              </Text>
              <TextArea
                value={reason}
                onChange={setReason}
                placeholder="Np. zły cennik, zła relacja, halucynacja THC…"
                rows={3}
              />
              <Button
                variant="primary"
                disabled={reason.trim() === ""}
                onClick={() => {
                  setOutcome("rejected");
                  setRejectOpen(false);
                }}
              >
                Potwierdź odrzucenie
              </Button>
            </Stack>
          ) : null}
        </Stack>
      </Grid>

      {outcome === "accepted" ? (
        <Callout tone="success" title="Accept → rate_line w jednej transakcji HTTP">
          Orchestracja API (1.3). ExtractionService nie importuje rates. Kupno
          z OFR 1850.00 USD czeka w katalogu stawek. BAF 120.00 USD — operator
          potwierdził mimo 0.61.
        </Callout>
      ) : null}
      {outcome === "rejected" ? (
        <Callout tone="danger" title="Szkic odrzucony">
          Powód: {reason.trim() === "" ? "(brak)" : reason}. PDF zostaje. Nie
          ma `rate_line`.
        </Callout>
      ) : null}

      <H2>Stany per źródło</H2>
      <Table
        headers={["Stan", "UI", "Zapis"]}
        rows={[
          ["przetwarzanie", "szkielet pól, label Art. 50", "brak"],
          ["niepewne", "glif ! + confidence < 0.7, pole edytowalne", "tylko po accept"],
          ["potwierdzone", "glif OK, gotowe do zbiorczego accept", "rate_line po 201"],
        ]}
      />
    </Stack>
  );
}

function PdfPane({ activeSpan }: { activeSpan: string }) {
  const theme = useHostTheme();
  const lines = [
    "MAERSK SPOT · SHA–GDY · SEP 2026",
    "20GP / 40HC / 40NOR",
    "OCEAN FREIGHT USD 1,850 / 40HC",
    "BAF USD 120 subject to change",
    "THC origin EUR 145",
    "Validity 01–30 Sep 2026",
  ];

  return (
    <div
      style={{
        border: `1px solid ${theme.stroke.tertiary}`,
        borderRadius: 6,
        padding: 12,
        background: theme.bg.elevated,
        minHeight: 320,
      }}
    >
      <Text size="small" tone="tertiary">
        Podgląd PDF (lazy pdf.js · poza initial chunk)
      </Text>
      <H3>MAERSK-SHA-0926.pdf</H3>
      <Stack gap={4}>
        {lines.map((line) => {
          const hot = line.includes(activeSpan.slice(0, 12)) || line === activeSpan;
          return (
            <div
              key={line}
              style={{
                fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
                fontSize: 12,
                padding: "4px 6px",
                background: hot ? theme.fill.secondary : "transparent",
                outline: hot ? `2px solid ${theme.stroke.focused}` : "none",
              }}
            >
              {line}
            </div>
          );
        })}
      </Stack>
      <Text size="small" tone="secondary">
        Klik pola po prawej podświetla span. Container query: na wąskim panelu
        PDF nad formularzem, nie obok.
      </Text>
    </div>
  );
}

function CandidateRow({
  row,
  active,
  onFocus,
  onToggle,
}: {
  row: Candidate;
  active: boolean;
  onFocus: () => void;
  onToggle: (checked: boolean) => void;
}) {
  const theme = useHostTheme();
  const confPct = Math.round(row.confidence * 100);

  return (
    <button
      type="button"
      onClick={onFocus}
      style={{
        display: "block",
        width: "100%",
        textAlign: "left",
        padding: 8,
        borderRadius: 6,
        border: `1px solid ${active ? theme.stroke.primary : theme.stroke.tertiary}`,
        background: active ? theme.fill.quaternary : theme.bg.elevated,
        color: theme.text.primary,
        cursor: "pointer",
      }}
    >
      <Row gap={8} align="center">
        <Checkbox checked={row.selected} onChange={onToggle} />
        <Text weight="semibold">{row.code}</Text>
        <Text style={{ fontVariantNumeric: "tabular-nums" }}>
          {row.amount} {row.currency}
        </Text>
        <Pill size="sm" active={row.state === "potwierdzone"}>
          {row.state} {confPct}%
        </Pill>
      </Row>
    </button>
  );
}
