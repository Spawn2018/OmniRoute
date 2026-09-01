import {
  Callout,
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
  useCanvasState,
} from "cursor/canvas";

type VariantId = "a" | "b";

type ChargeLine = {
  code: string;
  name: string;
  source: "statyczna" | "dynamiczna";
  buy: string;
  sell: string;
  margin: string;
  currency: string;
};

const VARIANT_A: ChargeLine[] = [
  {
    code: "OFR",
    name: "Fracht oceaniczny 40HC",
    source: "statyczna",
    buy: "1850.00",
    sell: "2100.00",
    margin: "250.00",
    currency: "USD",
  },
  {
    code: "BAF",
    name: "Bunker",
    source: "dynamiczna",
    buy: "120.00",
    sell: "135.00",
    margin: "15.00",
    currency: "USD",
  },
  {
    code: "THC",
    name: "THC pochodzenie SHA",
    source: "statyczna",
    buy: "145.00",
    sell: "170.00",
    margin: "25.00",
    currency: "EUR",
  },
];

const VARIANT_B: ChargeLine[] = [
  {
    code: "OFR",
    name: "Fracht oceaniczny 40HC (express)",
    source: "statyczna",
    buy: "2420.00",
    sell: "2680.00",
    margin: "260.00",
    currency: "USD",
  },
  {
    code: "BAF",
    name: "Bunker",
    source: "dynamiczna",
    buy: "120.00",
    sell: "135.00",
    margin: "15.00",
    currency: "USD",
  },
  {
    code: "THC",
    name: "THC pochodzenie SHA",
    source: "statyczna",
    buy: "145.00",
    sell: "170.00",
    margin: "25.00",
    currency: "EUR",
  },
];

export default function UiQuotation() {
  const [picked, setPicked] = useCanvasState<VariantId>("ui-05-picked", "a");

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>Oferta — warianty i charge</H1>
        <Text tone="secondary">
          Freightos side-by-side (cena vs tranzyt) plus unikalny układ OmniRoute:
          kupno, sprzedaż i marża na jednym rekordzie `charge`. LLM nie liczy
          `margin()`.
        </Text>
      </Stack>

      <Row gap={16} wrap>
        <Stat value="SHA–GDY 40HC" label="relacja" />
        <Stat value="2" label="warianty oferty" />
        <Stat value="charge" label="jedyna prawda o marży" />
      </Row>

      <Callout tone="info" title="Zasada 3">
        Nie ma osobnej kolumny „narzut” poza `charge`. Wariant A i B to dwa
        zestawy wierszy, nie dwa silniki wyceny. SQL składa ofertę z bieżącego
        `rate_line`; Python nie sumuje w pętli.
      </Callout>

      <Grid columns={2} gap={16}>
        <VariantCard
          id="a"
          title="A · ekonomiczny"
          transit="32 dni"
          eta="3–7 paź"
          picked={picked === "a"}
          onPick={() => setPicked("a")}
          lines={VARIANT_A}
          sellUsd="2235.00"
          note="TAKAL 1 połączenie · cutoff SHA śr 16:00"
        />
        <VariantCard
          id="b"
          title="B · express"
          transit="24 dni"
          eta="25 wrz – 1 paź"
          picked={picked === "b"}
          onPick={() => setPicked("b")}
          lines={VARIANT_B}
          sellUsd="2815.00"
          note="bezpośredni · cutoff SHA pn 12:00"
        />
      </Grid>

      <H2>Rozbicie `charge` — wariant {picked.toUpperCase()}</H2>
      <Text>
        Każdy wiersz = jeden rekord. Kupno z `rate_line` (source_ref). Sprzedaż
        wpisuje operator albo reguła tenanta — nie model. Marża =
        `margin(buy, sell)` po stronie serwera, tu tylko prezentacja.
      </Text>

      <ChargeTable lines={picked === "a" ? VARIANT_A : VARIANT_B} />

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H3>Statyczna vs dynamiczna</H3>
          <Table
            headers={["Typ", "Skąd", "UI"]}
            rows={[
              ["statyczna", "rate_line + source_ref", "zwykła kwota, wersja niemutowalna"],
              [
                "dynamiczna",
                "kanał / indeks (BAF)",
                "glif ~ + etykieta „zmienna”; nie optimistic",
              ],
            ]}
          />
        </Stack>
        <Stack gap={8}>
          <H3>Czego tu nie ma (jeszcze)</H3>
          <Text>
            Port i kontrahent wejdą w Q3 po M-05 i M-10. Porównanie odpowiedzi
            armatorów to Fala 3 (M-31). Ten canvas pokazuje układ kolumn, nie
            silnik live.
          </Text>
        </Stack>
      </Grid>
    </Stack>
  );
}

function VariantCard({
  title,
  transit,
  eta,
  picked,
  onPick,
  lines,
  sellUsd,
  note,
}: {
  id: VariantId;
  title: string;
  transit: string;
  eta: string;
  picked: boolean;
  onPick: () => void;
  lines: ChargeLine[];
  sellUsd: string;
  note: string;
}) {
  const staticCount = lines.filter((line) => line.source === "statyczna").length;
  const liveCount = lines.length - staticCount;

  return (
    <button
      type="button"
      onClick={onPick}
      style={{
        display: "block",
        width: "100%",
        textAlign: "left",
        padding: 0,
        border: "none",
        background: "transparent",
        cursor: "pointer",
        color: "inherit",
      }}
    >
      <Stack gap={8}>
        <Row gap={8} align="center">
          <H3>{title}</H3>
          {picked ? (
            <Pill active size="sm">
              wybrany
            </Pill>
          ) : (
            <Pill size="sm">wybierz</Pill>
          )}
        </Row>
        <Row gap={16}>
          <Stat value={sellUsd} label="sprzedaż USD (OFR+BAF)" />
          <Stat value={transit} label="tranzyt" />
        </Row>
        <Text size="small" tone="secondary">
          ETA {eta} · {note}
        </Text>
        <Text size="small">
          {staticCount} stałe · {liveCount} zmienne · {lines.length} pozycje charge
        </Text>
      </Stack>
    </button>
  );
}

function ChargeTable({ lines }: { lines: ChargeLine[] }) {
  return (
    <Table
      stickyHeader
      striped
      headers={["Kod", "Nazwa", "Źródło", "Kupno", "Sprzedaż", "Marża", "Waluta"]}
      columnAlign={["left", "left", "left", "right", "right", "right", "left"]}
      rowTone={lines.map((line) => (line.source === "dynamiczna" ? "warning" : "success"))}
      rows={lines.map((line) => [
        line.code,
        line.name,
        line.source === "dynamiczna" ? "~ dynamiczna" : "statyczna",
        line.buy,
        line.sell,
        line.margin,
        line.currency,
      ])}
    />
  );
}
