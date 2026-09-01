export function catalogCreateBody(args: {
  code: string
  name: string
  aliasesText: string
}): { code: string; name: string; aliases: string[] } {
  const aliases = args.aliasesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  return { code: args.code.trim(), name: args.name.trim(), aliases }
}
