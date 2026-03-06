# Compliance Checker Agent

## Description
Agent ensuring compliance with Polish language standards and legal regulations (RODO/GDPR).

## Capabilities
- Polish punctuation and grammar rule verification
- GDPR/RODO compliance checking
- Sensitive data detection in text
- Compliance report generation

## Triggers
- Before publishing text
- On demand via `/compliance-check` command

## Configuration
```json
{
  "agent": "compliance-checker",
  "rules": ["GDPR", "polish-language-act"],
  "strictMode": true
}
```
