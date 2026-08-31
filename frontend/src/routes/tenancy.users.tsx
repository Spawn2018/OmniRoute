import { createFileRoute } from "@tanstack/react-router"
import { UsersPage } from "@/features/tenancy/users-page"

export const Route = createFileRoute("/tenancy/users")({
  component: UsersPage,
})
