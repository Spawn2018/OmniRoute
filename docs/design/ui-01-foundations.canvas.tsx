import {
  Button,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Code,
  Divider,
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
  Toggle,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type Density = "comfortable" | "compact" | "condensed";

const RATE_ROWS: { lane: string; integer: string; fraction: string; currency: string }[] = [
  { lane: "CNSHA–PLGDY 40HC", integer: "1 850", fraction: "00", currency: "USD" },
  { lane: "DEHAM–PLGDY 40HC", integer: "420", fraction: "50", currency: "EUR" },
  { lane: "NLRTM–PLGDY 20GP", integer: "89", fraction: "00", currency: "EUR" },
  { lane: "SGSIN–PLGDY 40HC", integer: "12 040", fraction: "00", currency: "USD" },
];

export default function UiFoundations() {
  const [dark, setDark] = useCanvasState("ui-01-dark", false);
  const [density, setDensity] = useCanvasState<Density>("ui-01-density", "compact");
  const [focusDemo, setFocusDemo] = useCanvasState("ui-01-focus", false);

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>Fundamenty UI — tokeny, gęstość, Money</H1>
        <Text tone="secondary">
          Stan docelowy po ADR-0003. Canvas nie jest kodem produktu. Tokeny
          OKLCH zapisane jako wartości docelowe; kolory na ekranie biorą się z
          motywu hosta (zakaz hex w canvasie).
        </Text>
      </Stack>

      <Row gap={16} wrap>
        <Stat value="OKLCH" label="przestrzeń tokenów" />
        <Stat value="3" label="tryby gęstości" />
        <Stat value="4.5:1" label="próg kontrastu AA" />
        <Stat value="IBM Plex Sans" label="cyfry tabelaryczne" />
      </Row>

      <Callout tone="info" title="Dziś w repo vs ten canvas">
        `frontend/src/index.css` trzyma tokeny hex, jeden motyw, dwa tryby
        gęstości. Brak wyrównania kwot do przecinka. Ten ekran pokazuje cel:
        luminance-first, dark od razu, condensed tylko na gridzie stawek.
      </Callout>

      <Row gap={12} align="center">
        <Text size="small" weight="semibold">
          Podgląd motywu
        </Text>
        <Toggle checked={dark} onChange={setDark} />
        <Text size="small" tone="secondary">
          {dark ? "ciemny (Evening)" : "jasny (Morning)"}
        </Text>
      </Row>

      <H2>Rampy OKLCH luminance-first</H2>
      <Text>
        Kanał L steruje motywem i kontrastem, C emfazą, H marką. Accent =
        zieleń spedycyjna (nie fiolet AI-slopu). Destructive pozostaje czerwony
        z L dobranym tak, żeby para z tłem trzymała AA w obu motywach.
      </Text>

      <Grid columns={2} gap={16}>
        <TokenRamp
          title="Jasny — L wysokie na tle"
          tokens={[
            { name: "background", value: "oklch(0.97 0.004 95)", role: "tło aplikacji", contrast: "—" },
            { name: "card", value: "oklch(0.995 0.002 95)", role: "powierzchnia", contrast: "—" },
            { name: "foreground", value: "oklch(0.22 0.01 95)", role: "tekst", contrast: "12.4:1" },
            { name: "muted-fg", value: "oklch(0.45 0.01 95)", role: "etykiety", contrast: "7.1:1" },
            { name: "accent", value: "oklch(0.42 0.09 165)", role: "akcja / status OK", contrast: "5.8:1" },
            { name: "destructive", value: "oklch(0.48 0.16 25)", role: "błąd / odrzucenie", contrast: "5.2:1" },
          ]}
        />
        <TokenRamp
          title="Ciemny — L niskie na tle"
          tokens={[
            { name: "background", value: "oklch(0.18 0.01 95)", role: "tło aplikacji", contrast: "—" },
            { name: "card", value: "oklch(0.22 0.01 95)", role: "powierzchnia", contrast: "—" },
            { name: "foreground", value: "oklch(0.93 0.008 95)", role: "tekst", contrast: "13.1:1" },
            { name: "muted-fg", value: "oklch(0.72 0.01 95)", role: "etykiety", contrast: "7.4:1" },
            { name: "accent", value: "oklch(0.78 0.08 165)", role: "akcja / status OK", contrast: "8.6:1" },
            { name: "destructive", value: "oklch(0.72 0.14 25)", role: "błąd / odrzucenie", contrast: "6.1:1" },
          ]}
        />
      </Grid>

      <Text size="small" tone="tertiary">
        Kontrast policzony względem `background` tej samej rampy, WCAG 2.2 AA
        (tekst ≥ 4.5:1). Bramka: test snapshotu par tokenów, nie opinia.
        Źródło: ADR-0003 · EN 301 549 klauzula 9.7 (preferencje użytkownika).
      </Text>

      <SurfacePreview dark={dark} />

      <H2>Trzy tryby gęstości — ten sam wiersz</H2>
      <Text>
        Comfortable i compact są globalne (shell, formularze, HITL). Condensed
        tylko na DataTableShell stawek — nie na całym layoucie. Wartości to
        padding wiersza, nie osobny silnik tabeli.
      </Text>

      <Row gap={8} wrap>
        {(["comfortable", "compact", "condensed"] as Density[]).map((item) => (
          <span key={item}>
            <Pill active={density === item} onClick={() => setDensity(item)}>
              {item}
            </Pill>
          </span>
        ))}
      </Row>

      <Grid columns={3} gap={12}>
        <DensitySample mode="comfortable" active={density === "comfortable"} />
        <DensitySample mode="compact" active={density === "compact"} />
        <DensitySample mode="condensed" active={density === "condensed"} />
      </Grid>

      <H2>Typografia i cyfry tabelaryczne</H2>
      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H3>Stack</H3>
          <Text>
            IBM Plex Sans — pełne tabular figures, lining-nums, odróżnialne
            1 / l / I. Fallback: Segoe UI, system-ui.
          </Text>
          <Text>
            CSS: <Code>font-variant-numeric: lining-nums tabular-nums</Code> na
            każdej kolumnie liczbowej. Tailwind v4 ma utility `tabular-nums` —
            ręczna klasa w `index.css` do usunięcia (duplikat).
          </Text>
        </Stack>
        <Card>
          <CardHeader>Porównanie szerokości cyfr</CardHeader>
          <CardBody>
            <Stack gap={6}>
              <Text size="small" tone="secondary">
                proportional (źle — kolumna „tańczy”)
              </Text>
              <Text style={{ fontVariantNumeric: "proportional-nums" }}>
                1111.00 USD · 8888.00 USD
              </Text>
              <Text size="small" tone="secondary">
                tabular + lining (cel)
              </Text>
              <Text
                weight="medium"
                style={{ fontVariantNumeric: "lining-nums tabular-nums" }}
              >
                1111.00 USD · 8888.00 USD
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <H2>Money — wyrównanie do przecinka</H2>
      <Text>
        `amount: string` zostaje (zakaz float). Fiori Currency: kwota
        wyrównana do separatora dziesiętnego, zawsze trzyliterowy kod waluty,
        max 4 miejsca (kanon OmniRoute), locale formatuje grupowanie.
      </Text>

      <Table
        stickyHeader
        striped
        columnAlign={["left", "right"]}
        headers={["Relacja", "Stawka kupna"]}
        rows={RATE_ROWS.map((row) => [
          row.lane,
          <AlignedMoney
            integer={row.integer}
            fraction={row.fraction}
            currency={row.currency}
          />,
        ])}
      />
      <Text size="small" tone="tertiary">
        Przecinek (separator) stoi w jednej osi pionowej. Kod waluty za kwotą,
        stała szerokość. Źródło: SAP Fiori Currency · ADR-0003.
      </Text>

      <H2>Status = kolor plus ikona</H2>
      <Text>
        Sam kolor łamie WCAG 1.4.1. Każdy stan ma glif i etykietę tekstową.
      </Text>
      <Row gap={12} wrap>
        <StatusChip kind="ok" label="potwierdzone" />
        <StatusChip kind="warn" label="niepewne" />
        <StatusChip kind="err" label="odrzucone" />
        <StatusChip kind="wait" label="przetwarzanie" />
        <StatusChip kind="lock" label="brak uprawnień" />
      </Row>

      <H2>Pierścień fokusu</H2>
      <Text>
        `:focus-visible` 2px offset 2px, token `ring` = foreground (nie accent).
        Nie chować fokusu przy myszy (`:focus:not(:focus-visible)`).
      </Text>
      <Row gap={12} align="center">
        <Button
          variant={focusDemo ? "primary" : "secondary"}
          onClick={() => setFocusDemo(!focusDemo)}
        >
          {focusDemo ? "Fokus widoczny" : "Pokaż pierścień"}
        </Button>
        <FocusRingPreview on={focusDemo} />
      </Row>

      <Divider />
      <Text size="small" tone="tertiary">
        Źródło: audyt badania UI 2026-09-01 · ADR-0003 · nie implementacja w
        `frontend/`.
      </Text>
    </Stack>
  );
}

type TokenRow = {
  name: string;
  value: string;
  role: string;
  contrast: string;
};

function TokenRamp({ title, tokens }: { title: string; tokens: TokenRow[] }) {
  return (
    <Stack gap={8}>
      <H3>{title}</H3>
      <Table
        headers={["Token", "OKLCH", "Rola", "Kontrast"]}
        rows={tokens.map((token) => [
          token.name,
          token.value,
          token.role,
          token.contrast,
        ])}
        columnAlign={["left", "left", "left", "right"]}
      />
    </Stack>
  );
}

function SurfacePreview({ dark }: { dark: boolean }) {
  const theme = useHostTheme();
  const bg = dark ? theme.bg.chrome : theme.bg.editor;
  const fg = theme.text.primary;
  const muted = theme.text.secondary;
  const card = theme.bg.elevated;
  const line = theme.stroke.tertiary;

  return (
    <div
      style={{
        background: bg,
        color: fg,
        border: `1px solid ${line}`,
        borderRadius: 6,
        padding: 16,
      }}
    >
      <Row gap={12} justify="space-between" align="center">
        <Text weight="semibold">Pasek aplikacji</Text>
        <Text size="small" tone="secondary">
          {dark ? "Evening Horizon (cel)" : "Morning Horizon (cel)"}
        </Text>
      </Row>
      <div
        style={{
          marginTop: 12,
          background: card,
          border: `1px solid ${line}`,
          borderRadius: 6,
          padding: 12,
        }}
      >
        <Text size="small" style={{ color: muted }}>
          Karta · tło osobne od canvasu hosta, żeby ocenić parę L na L.
        </Text>
        <Text weight="medium">Stawki kupna — 4 wiersze widoczne</Text>
      </div>
    </div>
  );
}

function DensitySample({ mode, active }: { mode: Density; active: boolean }) {
  const pad =
    mode === "comfortable" ? "10px 12px" : mode === "compact" ? "5px 8px" : "1px 6px";
  const size = mode === "condensed" ? 12 : mode === "compact" ? 13 : 14;
  const rows = ["CNSHA–PLGDY", "DEHAM–PLGDY", "NLRTM–PLGDY"];
  const theme = useHostTheme();

  return (
    <div
      style={{
        border: `1px solid ${active ? theme.stroke.primary : theme.stroke.tertiary}`,
        borderRadius: 6,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "6px 8px",
          background: theme.fill.tertiary,
          fontSize: 11,
        }}
      >
        {mode}
        {mode === "condensed" ? " · tylko grid stawek" : ""}
      </div>
      {rows.map((lane) => (
        <div
          key={lane}
          style={{
            padding: pad,
            fontSize: size,
            fontVariantNumeric: "tabular-nums",
            borderTop: `1px solid ${theme.stroke.tertiary}`,
            display: "flex",
            justifyContent: "space-between",
            gap: 8,
          }}
        >
          <span>{lane}</span>
          <span>1 850.00</span>
        </div>
      ))}
    </div>
  );
}

function AlignedMoney({
  integer,
  fraction,
  currency,
}: {
  integer: string;
  fraction: string;
  currency: string;
}) {
  return (
    <span
      style={{
        display: "inline-grid",
        gridTemplateColumns: "minmax(4.5em, auto) auto auto",
        columnGap: 0,
        fontVariantNumeric: "lining-nums tabular-nums",
        justifyContent: "end",
      }}
    >
      <span style={{ textAlign: "right" }}>{integer}</span>
      <span>.{fraction}</span>
      <span style={{ marginLeft: 8, textAlign: "left" }}>{currency}</span>
    </span>
  );
}

function StatusChip({
  kind,
  label,
}: {
  kind: "ok" | "warn" | "err" | "wait" | "lock";
  label: string;
}) {
  const theme = useHostTheme();
  const glyph =
    kind === "ok"
      ? "OK"
      : kind === "warn"
        ? "!"
        : kind === "err"
          ? "X"
          : kind === "wait"
            ? "…"
            : "—";
  const tone =
    kind === "ok"
      ? theme.diff.insertedLine
      : kind === "err"
        ? theme.diff.removedLine
        : theme.fill.secondary;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "4px 8px",
        borderRadius: 4,
        background: tone,
        fontSize: 12,
      }}
    >
      <span
        aria-hidden="true"
        style={{
          width: 14,
          textAlign: "center",
          fontWeight: 600,
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {glyph}
      </span>
      <span>{label}</span>
    </span>
  );
}

function FocusRingPreview({ on }: { on: boolean }) {
  const theme = useHostTheme();
  return (
    <div
      style={{
        padding: "6px 12px",
        borderRadius: 6,
        border: `1px solid ${theme.stroke.tertiary}`,
        outline: on ? `2px solid ${theme.stroke.focused}` : "none",
        outlineOffset: 2,
        fontSize: 13,
      }}
    >
      Kontrolka z :focus-visible
    </div>
  );
}
