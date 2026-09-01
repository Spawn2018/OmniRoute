import {
  Button,
  Callout,
  Checkbox,
  Grid,
  H1,
  H2,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  TextInput,
  useCanvasState,
} from "cursor/canvas";

type GridState = "dane" | "ładowanie" | "pusty" | "błąd" | "403";
type Density = "compact" | "condensed";

type RateRow = {
  id: string;
  lane: string;
  eq: string;
  buyInteger: string;
  buyFraction: string;
  currency: string;
  source: string;
  status: "aktywna" | "superseded";
  supersededBy: string | null;
};

const ALL_ROWS: RateRow[] = [
  {
    id: "rl-1001",
    lane: "CNSHA–PLGDY",
    eq: "40HC",
    buyInteger: "1 850",
    buyFraction: "00",
    currency: "USD",
    source: "MAERSK-SHA-0926",
    status: "aktywna",
    supersededBy: null,
  },
  {
    id: "rl-0988",
    lane: "CNSHA–PLGDY",
    eq: "40HC",
    buyInteger: "1 920",
    buyFraction: "00",
    currency: "USD",
    source: "MAERSK-SHA-0826",
    status: "superseded",
    supersededBy: "rl-1001",
  },
  {
    id: "rl-1102",
    lane: "DEHAM–PLGDY",
    eq: "40HC",
    buyInteger: "420",
    buyFraction: "50",
    currency: "EUR",
    source: "HAPAG-HAM-0926",
    status: "aktywna",
    supersededBy: null,
  },
  {
    id: "rl-1103",
    lane: "NLRTM–PLGDY",
    eq: "20GP",
    buyInteger: "89",
    buyFraction: "00",
    currency: "EUR",
    source: "MSC-RTM-0926",
    status: "aktywna",
    supersededBy: null,
  },
  {
    id: "rl-1201",
    lane: "SGSIN–PLGDY",
    eq: "40HC",
    buyInteger: "12 040",
    buyFraction: "00",
    currency: "USD",
    source: "ONE-SIN-0926",
    status: "aktywna",
    supersededBy: null,
  },
];

const COLS = [
  { id: "lane", label: "Relacja", pinned: true },
  { id: "eq", label: "Sprzęt", pinned: true },
  { id: "buy", label: "Kupno", pinned: false },
  { id: "source", label: "source_ref", pinned: false },
  { id: "status", label: "Wersja", pinned: false },
];

export default function UiDataGrid() {
  const [state, setState] = useCanvasState<GridState>("ui-03-state", "dane");
  const [density, setDensity] = useCanvasState<Density>("ui-03-density", "condensed");
  const [filter, setFilter] = useCanvasState("ui-03-filter", "ocean");
  const [laneQuery, setLaneQuery] = useCanvasState("ui-03-lane", "");
  const [view, setView] = useCanvasState("ui-03-view", "operacyjny");
  const [editor, setEditor] = useCanvasState("ui-03-editor", false);
  const [hidden, setHidden] = useCanvasState<string[]>("ui-03-hidden", []);
  const [editing, setEditing] = useCanvasState<string | null>("ui-03-edit", null);
  const [draftBuy, setDraftBuy] = useCanvasState("ui-03-draft-buy", "1850.00");

  const visibleCols = COLS.filter((col) => !hidden.includes(col.id));
  const filtered = ALL_ROWS.filter((row) => {
    if (filter === "aktywne" && row.status !== "aktywna") {
      return false;
    }
    if (laneQuery.trim() !== "" && !row.lane.toLowerCase().includes(laneQuery.toLowerCase())) {
      return false;
    }
    return true;
  });

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>Grid stawek — 50k wierszy, jeden silnik</H1>
        <Text tone="secondary">
          DataTableShell z zachowaniami Fiori (freeze, wirtualizacja, edycja w
          miejscu), bez czterech osobnych komponentów tabeli. ADR-0002 zakazuje
          drugiego grid engine.
        </Text>
      </Stack>

      <Row gap={16} wrap>
        <Stat value="50 000" label="wierszy (wirtualnie)" />
        <Stat value=">500" label="próg virtualizer" />
        <Stat value={density} label="gęstość grida" />
        <Stat value="URL" label="filtry zsynchronizowane" />
      </Row>

      <Callout tone="danger" title="Optimistic UI zakazane na kwocie">
        Filtr, kolejność kolumn, zapis widoku — natychmiast. Zmiana stawki to
        nowy `rate_line` + `superseded_by`, czekamy na 201. Nigdy patch w miejscu
        na kwocie.
      </Callout>

      <Row gap={8} wrap>
        {(["dane", "ładowanie", "pusty", "błąd", "403"] as GridState[]).map((item) => (
          <span key={item}>
            <Pill active={state === item} onClick={() => setState(item)}>
              {item}
            </Pill>
          </span>
        ))}
      </Row>

      <Row gap={8} wrap align="center">
        <Text size="small" weight="semibold">
          Filtry (URL `?mode=ocean&lane=`)
        </Text>
        <span>
          <Pill active={filter === "ocean"} onClick={() => setFilter("ocean")}>
            ocean
          </Pill>
        </span>
        <span>
          <Pill active={filter === "aktywne"} onClick={() => setFilter("aktywne")}>
            tylko aktywne
          </Pill>
        </span>
        <TextInput
          value={laneQuery}
          onChange={setLaneQuery}
          placeholder="Relacja…"
          style={{ width: 160 }}
        />
        <span>
          <Pill
            active={density === "condensed"}
            onClick={() => setDensity(density === "condensed" ? "compact" : "condensed")}
          >
            {density}
          </Pill>
        </span>
        <Button variant="secondary" onClick={() => setEditor(!editor)}>
          Kolumny
        </Button>
        <span>
          <Pill active={view === "operacyjny"} onClick={() => setView("operacyjny")}>
            widok: operacyjny
          </Pill>
        </span>
        <span>
          <Pill active={view === "audyt"} onClick={() => setView("audyt")}>
            widok: audyt
          </Pill>
        </span>
      </Row>

      {editor ? (
        <Stack gap={8}>
          <H2>ColumnEditor</H2>
          <Text size="small" tone="secondary">
            Checkbox widoczności + kolejność (DnD w produkcie, tu toggle). Pin
            pierwszych dwóch kolumn nie zdejmuje się z edytora.
          </Text>
          {COLS.map((col) => (
            <div key={col.id}>
              <Checkbox
                checked={!hidden.includes(col.id)}
                disabled={col.pinned}
                label={`${col.label}${col.pinned ? " (przypięta)" : ""}`}
                onChange={(checked) => {
                  if (col.pinned) {
                    return;
                  }
                  setHidden(
                    checked ? hidden.filter((id) => id !== col.id) : [...hidden, col.id],
                  );
                }}
              />
            </div>
          ))}
        </Stack>
      ) : null}

      {state === "ładowanie" ? (
        <Callout tone="info" title="Szkielet > 1 s">
          Pięć wierszy-placeholderów tej samej wysokości co condensed. Bez
          layout shift. Ładowanie &lt; 1 s — bez skeletonu.
        </Callout>
      ) : null}

      {state === "pusty" ? (
        <Callout tone="neutral" title="Brak stawek dla filtra">
          Żaden `rate_line` nie pasuje do `mode=ocean` i relacji. Wyczyść filtr
          albo wgraj cennik do kolejki HITL. Nie „No data”.
        </Callout>
      ) : null}

      {state === "błąd" ? (
        <Callout tone="danger" title="Lista stawek nie wstała">
          503 z API. Ponów. Kwot nie zgadujemy z cache. Nie optimistic retry na
          zapisie.
        </Callout>
      ) : null}

      {state === "403" ? (
        <Callout tone="warning" title="Brak can_read_rate_lines">
          OpenFGA odmówił. Nie 404. Recenzent widzi HITL, nie katalog stawek —
          odwrotnie member.
        </Callout>
      ) : null}

      {state === "dane" ? (
        <Table
          stickyHeader
          striped
          headers={[
            ...visibleCols.map((col) => (col.pinned ? `${col.label} · pin` : col.label)),
            "Akcja",
          ]}
          columnAlign={visibleCols.map((col) => (col.id === "buy" ? "right" : "left"))}
          rowTone={filtered.map((row) =>
            row.status === "superseded" ? "neutral" : "success",
          )}
          rows={filtered.map((row) => {
            const cells: Array<string | ReturnType<typeof Text>> = [];
            for (const col of visibleCols) {
              if (col.id === "lane") {
                cells.push(row.lane);
              } else if (col.id === "eq") {
                cells.push(row.eq);
              } else if (col.id === "buy") {
                cells.push(`${row.buyInteger}.${row.buyFraction} ${row.currency}`);
              } else if (col.id === "source") {
                cells.push(row.source);
              } else {
                cells.push(
                  row.status === "superseded"
                    ? `zastąpiona przez ${row.supersededBy}`
                    : "aktywna",
                );
              }
            }
            cells.push(
              row.status === "aktywna" ? (
                <Button
                  variant="ghost"
                  onClick={() => {
                    setEditing(row.id);
                    setDraftBuy(`${row.buyInteger.replace(" ", "")}.${row.buyFraction}`);
                  }}
                >
                  nowa wersja
                </Button>
              ) : (
                "—"
              ),
            );
            return cells;
          })}
        />
      ) : null}

      {editing !== null && state === "dane" ? (
        <Stack gap={8}>
          <H2>Edycja w miejscu = nowy rekord</H2>
          <Text>
            Wiersz `{editing}` zostaje niemutowalny. Zapis tworzy `rate_line` z
            `superseded_by` wskazującym stary id. `source_ref` obowiązkowy.
          </Text>
          <Grid columns={3} gap={12}>
            <Stack gap={4}>
              <Text size="small" tone="secondary">
                Kupno (string, nie float)
              </Text>
              <TextInput value={draftBuy} onChange={setDraftBuy} />
            </Stack>
            <Stack gap={4}>
              <Text size="small" tone="secondary">
                source_ref
              </Text>
              <Text>MAERSK-SHA-0926</Text>
            </Stack>
            <Row gap={8} align="end">
              <Button variant="primary" onClick={() => setEditing(null)}>
                Zapisz nową wersję
              </Button>
              <Button variant="ghost" onClick={() => setEditing(null)}>
                Anuluj
              </Button>
            </Row>
          </Grid>
        </Stack>
      ) : null}

      <H2>Zasady 5 i 6 na wierszu</H2>
      <Grid columns={2} gap={16}>
        <Stack gap={6}>
          <Text weight="semibold">source_ref</Text>
          <Text>
            Klik z kolumny otwiera szkic HITL albo plik źródłowy. Wiersz bez
            pochodzenia nie wchodzi — API to blokuje, UI nie oferuje „pustego”
            zapisu.
          </Text>
        </Stack>
        <Stack gap={6}>
          <Text weight="semibold">superseded_by</Text>
          <Text>
            Zastąpiony wiersz zostaje w gridzie przy widoku audyt, wyszarza
            kwotę, linkuje do następcy. Widok operacyjny ukrywa go filtrem
            `aktywne`.
          </Text>
        </Stack>
      </Grid>

      <Text size="small" tone="tertiary">
        Wirtualizacja: DOM trzyma ~30 wierszy przy 50k. Pin: `lane` + `eq`
        freeze. ViewManager persystuje JSON w `table_view` (RLS), nie sam
        localStorage. Źródło: ADR-0002 + ADR-0003.
      </Text>
    </Stack>
  );
}
