# shadcn/ui Integration

## Why shadcn

- Full component ownership — code lives in your repo
- Predictable composition via Radix primitives
- Tailwind v4 semantic tokens (oklch color space)
- No version lock-in; upgrade incrementally

## Integration Points

| What | Where |
|------|-------|
| shadcn config | `frontend/components.json` |
| UI primitives | `frontend/src/presentation/components/ui/` |
| cn() helper | `frontend/src/lib/utils.ts` |
| Theme tokens | `frontend/src/presentation/styles/tailwind.css` |
| Structural CSS | `frontend/src/presentation/styles/` |

## Adding Components

```bash
bun run ui:add <component>   # Add a shadcn component
bun run ui:info              # Check component diff/health
```

## Theming

- All colors use oklch in CSS variables (`:root` and `.dark`)
- Modify tokens in `tailwind.css` under `:root` / `.dark`
- Prefer semantic utilities (`bg-primary`) over raw colors
- Single `--radius` source of truth: `0.625rem`

## Production Guardrails

- Keep `components.json` aliases in sync with `tsconfig.json` paths
- Use shadcn UI primitives before reaching for custom implementations
- Always scaffold with the CLI, never copy-paste from docs
- Run `bun run ui:info` for health checks after upgrades
