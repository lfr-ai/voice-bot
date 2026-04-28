# Agents and automation

This repository does not include hosted agent definitions. Use these notes as
guidance for creating Copilot/agent instructions for repository maintenance.

- Use `ci.yml` and `codeql-analysis.yml` in `.github/workflows/` for CI-based scans.
- Add `agents/` directory with `*.agent.md` instructions to provide custom
  Copilot or automation agents (optional).

See `.github/` for existing workflows and `Taskfile.yml` for local task targets.
