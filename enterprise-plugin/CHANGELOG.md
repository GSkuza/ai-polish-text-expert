# Changelog

All notable changes to **AI Polish Text Expert** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial project structure
- Enterprise plugin scaffold

---

## [1.0.0] - 2026-03-06

### Added
- Plugin manifest (`.claude-plugin/plugin.json`)
- Commands: `status`, `logs`
- Agents: `security-reviewer`, `performance-tester`, `compliance-checker`
- Skills: `code-reviewer`, `pdf-processor`
- Hook configurations: `hooks.json`, `security-hooks.json`
- MCP server definitions (`.mcp.json`)
- LSP server configurations (`.lsp.json`)
- Utility scripts: `security-scan.sh`, `format-code.py`, `deploy.js`
- Default plugin settings (`settings.json`)
- MIT License
