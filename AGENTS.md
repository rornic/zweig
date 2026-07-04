# AGENTS.md

Instructions for AI agents working in this repository.

## What this repo is

A self-hosted plugin marketplace for both Claude Code and Codex CLI, shipping two writing skills, `zweig-write` and `zweig-refine`. Both plugin formats share the same `skills/` directory. See README.md for what each skill does.

## Structure

- `.claude-plugin/plugin.json` — Claude Code plugin manifest, the single source of truth for that plugin's `version`.
- `.claude-plugin/marketplace.json` — Claude Code marketplace listing. Does not duplicate `version`; plugin.json wins under strict mode.
- `.codex-plugin/plugin.json` — Codex plugin manifest, mirrors `.claude-plugin/plugin.json` plus a `skills` field pointing at `./skills/`.
- `.agents/plugins/marketplace.json` — Codex marketplace listing, referencing this repo's plugin at `./` (path resolution to the repo root needs Codex CLI >= 0.142.0; older versions reject that path and need a subdirectory workaround instead).
- `skills/<name>/SKILL.md` — skill definition (YAML frontmatter + instructions), shared by both plugin formats.
- `skills/zweig-refine/EXAMPLE.md` — worked transcript of the refine loop.
- `.github/workflows/release.yml` — manual `workflow_dispatch` (Actions tab, choose patch/minor/major) that bumps both `plugin.json` versions, commits, tags `vX.Y.Z`, and creates the GitHub release. Pushes straight to `main`; there's no branch protection to route around.

## Making changes

- Run `claude plugin validate . --strict` before committing changes to either Claude manifest.
- Cut a release with the `.github/workflows/release.yml` workflow (Actions tab, pick patch/minor/major) when a change should reach existing installs; it bumps both `plugin.json` versions, tags, and creates the GitHub release together.
- Any non-trivial prose here (README, SKILL.md instructions) should go through this repo's own `zweig-write` and `zweig-refine` skills before it ships.
- Don't add a shared file that a `SKILL.md` instructs the model to `Read` at runtime: that `Read` call needs permission approval on every install, every time the skill fires, for every user. Content a skill always needs (style rules, cut criteria) must be inlined directly in that skill's own `SKILL.md`, even if that duplicates it across skills. Companion files (like `EXAMPLE.md`) are fine only for material a skill references but doesn't strictly require every run.
- Commit messages: lowercase conventional commits (e.g. `fix: ...`, `feat: ...`).
