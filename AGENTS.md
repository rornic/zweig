# AGENTS.md

Instructions for AI agents working in this repository.

## What this repo is

A self-hosted Claude Code plugin marketplace shipping two writing skills, `zweig-write` and `zweig-refine`. See README.md for what each does.

## Structure

- `.claude-plugin/plugin.json` — plugin manifest, the single source of truth for `version`.
- `.claude-plugin/marketplace.json` — marketplace listing. Does not duplicate `version`; plugin.json wins under strict mode.
- `skills/<name>/SKILL.md` — skill definition (YAML frontmatter + instructions).
- `skills/zweig-refine/EXAMPLE.md` — worked transcript of the refine loop.

## Making changes

- Run `claude plugin validate . --strict` before committing changes to either manifest.
- Bump `version` in `.claude-plugin/plugin.json` when a change should reach existing installs; users only get updates when it changes.
- Any non-trivial prose here (README, SKILL.md instructions) should go through this repo's own `zweig-write` and `zweig-refine` skills before it ships.
- Don't add a shared file that a `SKILL.md` instructs the model to `Read` at runtime: that `Read` call needs permission approval on every install, every time the skill fires, for every user. Content a skill always needs (style rules, cut criteria) must be inlined directly in that skill's own `SKILL.md`, even if that duplicates it across skills. Companion files (like `EXAMPLE.md`) are fine only for material a skill references but doesn't strictly require every run.
- Commit messages: lowercase conventional commits (e.g. `fix: ...`, `feat: ...`).
