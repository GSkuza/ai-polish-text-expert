# Security Reviewer Agent

## Description
Agent responsible for reviewing code for security vulnerabilities in the context of Polish text processing.

## Capabilities
- Static code analysis
- Detection of SQL injection, XSS, and other vulnerabilities
- Generates security reports

## Triggers
- On every Pull Request
- On demand via `/security-review` command

## Configuration
```json
{
  "agent": "security-reviewer",
  "autoTrigger": true,
  "severity": ["critical", "high", "medium"]
}
```
