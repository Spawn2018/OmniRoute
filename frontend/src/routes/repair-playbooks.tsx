import { createFileRoute } from "@tanstack/react-router"
import { RepairPlaybookDesk } from "@/features/repair-playbook/catalog-page"

export const Route = createFileRoute("/repair-playbooks")({
  component: RepairPlaybookDesk,
})
