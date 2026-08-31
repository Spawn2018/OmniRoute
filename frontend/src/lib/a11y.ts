export const SKIP_TO_MAIN_LABEL = "Przejdź do treści"
export const MAIN_CONTENT_ID = "main-content"

export const OPERATOR_KEYBOARD_PATH = [
  { id: "skip-main", keys: "Tab", target: `#${MAIN_CONTENT_ID}` },
  { id: "command-palette", keys: "Control+k", target: "command-palette" },
  { id: "extract", keys: "Tab", target: "[data-operator-target=extract]" },
  { id: "hitl-accept", keys: "Tab", target: "[data-operator-target=accept]" },
  { id: "hitl-reject", keys: "Tab", target: "button" },
  { id: "density", keys: "Tab", target: "[data-table-density]" },
] as const
