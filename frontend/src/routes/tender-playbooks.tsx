import { createFileRoute } from "@tanstack/react-router"
import { PlayDesk } from "@/features/tender-playbook/catalog-page"

export const Route = createFileRoute("/tender-playbooks")({
  component: PlayDesk,
})
