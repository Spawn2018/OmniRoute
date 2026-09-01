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
  useHostTheme,
} from "cursor/canvas";

type VisionTab = "watchtower" | "timeline" | "portals";

const EXCEPTIONS = [
  { id: "EX-441", shipment: "SHA-GDY-1042", issue: "dwell SHA 38 h (SLA 24 h)", mode: "ocean" },
  { id: "EX-442", shipment: "HAM-GDY-0881", issue: "ETA ±18 h, brak AIS 6 h", mode: "ocean" },
  { id: "EX-443", shipment: "KZ-PL-2201", issue: "handoff Khorgos opóźniony 12 h", mode: "rail" },
];

const SHIPMENTS = [
  { id: "SHA-GDY-1042", lane: "CNSHA–PLGDY", eta: "3 paź ±2 d", status: "w morzu" },
  { id: "HAM-GDY-0881", lane: "DEHAM–PLGDY", eta: "4 wrz ±18 h", status: "wyjątek" },
  { id: "KZ-PL-2201", lane: "CNXIU–PLGDY", eta: "12 wrz ±3 d", status: "kolej" },
];

const MILESTONES = [
  { t: "01 wrz 08:00", mode: "droga", label: "podjęcie SHA CY", dwell: "—" },
  { t: "01 wrz 22:00", mode: "ocean", label: "załadunek MD1", dwell: "14 h" },
  { t: "02 wrz 12:00", mode: "ocean", label: "WOD SHA", dwell: "—" },
  { t: "03 paź 06:00", mode: "ocean", label: "ETA GDY (niepewne ±2 d)", dwell: "—" },
  { t: "03 paź 18:00", mode: "droga", label: "dostawa Gdynia DC", dwell: "—" },
];

export default function UiVision() {
  const [tab, setTab] = useCanvasState<VisionTab>("ui-06-tab", "watchtower");
  const [portal, setPortal] = useCanvasState<"klient" | "przewoźnik">("ui-06-portal", "klient");

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>Wizja — watchtower, oś czasu, portale</H1>
        <Text tone="secondary">
          Trzy ekrany bez backendu. M-05 Geografia jest Q1. Przesyłka / tracking
          to Fala 5 (M-35–M-37). Portale to Fala 10. Nie startować przed
          danymi.
        </Text>
      </Stack>

      <Callout tone="danger" title="Jawnie niezaimplementowane">
        Mapa to leniwy chunk trasy, wyłączony z budżetu initial JS (gate 250 kB
        gzip). Silnik mapy ~200 kB — własny budżet. Ten canvas jest makietą, nie
        transzą kolejki Q.
      </Callout>

      <Row gap={8} wrap>
        <span>
          <Pill active={tab === "watchtower"} onClick={() => setTab("watchtower")}>
            Watchtower
          </Pill>
        </span>
        <span>
          <Pill active={tab === "timeline"} onClick={() => setTab("timeline")}>
            Oś multimodalna
          </Pill>
        </span>
        <span>
          <Pill active={tab === "portals"} onClick={() => setTab("portals")}>
            Portale
          </Pill>
        </span>
      </Row>

      {tab === "watchtower" ? <Watchtower /> : null}
      {tab === "timeline" ? <Timeline /> : null}
      {tab === "portals" ? <Portals portal={portal} onPortal={setPortal} /> : null}
    </Stack>
  );
}

function Watchtower() {
  return (
    <Stack gap={16}>
      <Row gap={16} wrap>
        <Stat value="3" label="przesyłki na mapie" />
        <Stat value="3" label="wyjątki" tone="warning" />
        <Stat value="lazy" label="chunk mapy" />
      </Row>
      <Grid columns="1.4fr 1fr" gap={16}>
        <MapSchematic />
        <Stack gap={12}>
          <H2>Panel wyjątków</H2>
          <Table
            headers={["ID", "Przesyłka", "Problem"]}
            rows={EXCEPTIONS.map((item) => [item.id, item.shipment, item.issue])}
            rowTone={["warning", "danger", "warning"]}
          />
          <H3>Lista przesyłek</H3>
          <Table
            headers={["Przesyłka", "Relacja", "ETA", "Status"]}
            rows={SHIPMENTS.map((item) => [item.id, item.lane, item.eta, item.status])}
          />
        </Stack>
      </Grid>
      <Text size="small" tone="tertiary">
        Wzór: Flexport watchtower (mapa + lista + wyjątki) i project44 VOC
        (jedna powierzchnia, bez przełączania modału). ETA zawsze z zakresem
        niepewności — nie pojedyncza data udająca pewność.
      </Text>
    </Stack>
  );
}

function MapSchematic() {
  const theme = useHostTheme();
  return (
    <div
      style={{
        border: `1px solid ${theme.stroke.tertiary}`,
        borderRadius: 6,
        padding: 12,
        background: theme.bg.elevated,
        minHeight: 280,
      }}
    >
      <Text size="small" tone="tertiary">
        Schemat, nie silnik mapy
      </Text>
      <H3>Pasy SHA → GDY / HAM → GDY / XIU → GDY</H3>
      <svg viewBox="0 0 360 180" width="100%" height="180" aria-label="Schemat pasów multimodalnych">
        <rect x="8" y="8" width="344" height="164" fill="none" stroke={theme.stroke.tertiary} />
        <path
          d="M40 120 C 120 40, 220 40, 320 70"
          fill="none"
          stroke={theme.stroke.primary}
          strokeWidth="2"
        />
        <path
          d="M80 150 C 140 130, 240 110, 320 90"
          fill="none"
          stroke={theme.accent.primary}
          strokeWidth="2"
        />
        <path
          d="M50 50 C 140 30, 200 80, 310 50"
          fill="none"
          stroke={theme.stroke.secondary}
          strokeWidth="2"
          strokeDasharray="6 4"
        />
        <circle cx="40" cy="120" r="4" fill={theme.accent.primary} />
        <circle cx="320" cy="70" r="4" fill={theme.accent.primary} />
        <text x="28" y="140" fill={theme.text.secondary} fontSize="10">
          SHA
        </text>
        <text x="300" y="58" fill={theme.text.secondary} fontSize="10">
          GDY
        </text>
        <text x="70" y="168" fill={theme.text.tertiary} fontSize="10">
          ocean
        </text>
        <text x="120" y="24" fill={theme.text.tertiary} fontSize="10">
          kolej (przerywana)
        </text>
      </svg>
      <Text size="small">
        Wyjątek HAM–GDY: brak AIS. Kolor pasa + etykieta tekstowa, nie sam kolor.
      </Text>
    </div>
  );
}

function Timeline() {
  return (
    <Stack gap={12}>
      <H2>Oś czasu SHA-GDY-1042</H2>
      <Text>
        Segmenty per mode, handoff jako kamień, dwell w węźle, ETA z jawnym
        zakresem. Jeden widok — droga / ocean / kolej bez zmiany ekranu.
      </Text>
      <Table
        headers={["Czas", "Mode", "Zdarzenie", "Dwell"]}
        rows={MILESTONES.map((item) => [item.t, item.mode, item.label, item.dwell])}
        rowTone={MILESTONES.map((item) =>
          item.label.includes("niepewne") ? "warning" : "info",
        )}
      />
      <Callout tone="info" title="Niepewność jest feature">
        „3 paź ±2 d” zostaje na osi, dopóki AIS nie potwierdzi. HAX G10: nie
        spłaszczaj do pojedynczej daty, żeby UI wyglądał pewniej niż dane.
      </Callout>
    </Stack>
  );
}

function Portals({
  portal,
  onPortal,
}: {
  portal: "klient" | "przewoźnik";
  onPortal: (v: "klient" | "przewoźnik") => void;
}) {
  return (
    <Stack gap={12}>
      <Row gap={8}>
        <span>
          <Pill active={portal === "klient"} onClick={() => onPortal("klient")}>
            Portal klienta
          </Pill>
        </span>
        <span>
          <Pill active={portal === "przewoźnik"} onClick={() => onPortal("przewoźnik")}>
            Portal przewoźnika
          </Pill>
        </span>
      </Row>
      {portal === "klient" ? (
        <Stack gap={8}>
          <H2>Klient — status, dokumenty, komunikacja</H2>
          <Table
            headers={["Przesyłka", "Status", "Dokument", "Widoczne"]}
            rows={[
              ["SHA-GDY-1042", "w morzu · ETA 3 paź ±2 d", "draft B/L", "tak"],
              ["HAM-GDY-0881", "wyjątek · brak AIS", "—", "tak"],
            ]}
          />
          <Text>
            Uproszczona powierzchnia: zero marży, zero HITL, zero stawek kupna.
            Branded tracking page (wzór project44) — osobna trasa, osobny bundle.
          </Text>
        </Stack>
      ) : (
        <Stack gap={8}>
          <H2>Przewoźnik — przydział, potwierdzenia, tracking</H2>
          <Table
            headers={["Zlecenie", "Lane", "Benchmark", "Akcja"]}
            rows={[
              ["C-2201", "SHA–GDY", "p50 dwell 22 h", "potwierdź podjęcie"],
              ["C-2208", "HAM–GDY", "AIS luka 6 h", "wgraj pozycję"],
            ]}
          />
          <Text>
            Carrier-centric: benchmark per lane, nie dashboard spedytora.
            Uprawnienia FGA osobnego tenanta-przewoźnika.
          </Text>
        </Stack>
      )}
      <Text size="small" tone="tertiary">
        Zależności: M-05 porty → M-35 zlecenie → M-36 tracking → M-61+ portal.
        Print B/L i listu przewozowego = osobny leftover U-print, nie ten ekran.
      </Text>
    </Stack>
  );
}
