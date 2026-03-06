#!/bin/bash
# security-scan.sh
# Scans the codebase for security vulnerabilities

set -e

MODE="${1:---mode=full}"
SEVERITY="${2:---severity=high}"

echo "=== AI Polish Text Expert Security Scanner ==="
echo "Mode: $MODE"
echo "Severity: $SEVERITY"
echo ""

# Check for secrets in code
if [[ "$MODE" == "--mode=secrets" || "$MODE" == "--mode=full" ]]; then
  echo "[*] Scanning for hardcoded secrets..."
  if command -v gitleaks &> /dev/null; then
    gitleaks detect --source . --verbose
  else
    echo "[!] gitleaks not found, skipping secret scan"
  fi
fi

# Static Application Security Testing
if [[ "$MODE" == "--mode=sast" || "$MODE" == "--mode=full" ]]; then
  echo "[*] Running SAST analysis..."
  if command -v bandit &> /dev/null; then
    bandit -r . -ll 2>/dev/null || true
  else
    echo "[!] bandit not found, skipping SAST scan"
  fi
fi

echo ""
echo "[+] Security scan complete."
