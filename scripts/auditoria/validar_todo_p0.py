#!/usr/bin/env python3
"""Ejecuta todas las auditorías P0 y muestra resumen final."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()

CHECKS = [
    ("JSON dashboard", "scripts/auditoria/validar_json_dashboard.py"),
    ("CSV indicadores", "scripts/auditoria/validar_csv_indicadores.py"),
    ("Indicadores P0", "scripts/auditoria/validar_indicadores_p0.py"),
]


def run_check(label: str, rel_script: str) -> tuple[str, bool]:
    script = ROOT / rel_script
    if not script.exists():
        print(f"\n[{label}] ERROR")
        print(f"- no existe script: {rel_script}")
        return label, False

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    print(f"\n[{label}]")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())

    return label, result.returncode == 0


def main() -> int:
    results = [run_check(label, script) for label, script in CHECKS]

    print("\nResumen final")
    for label, ok in results:
        print(f"- {label}: {'OK' if ok else 'ERROR'}")

    general_ok = all(ok for _, ok in results)
    print(f"- Resultado general: {'OK' if general_ok else 'ERROR'}")
    return 0 if general_ok else 1


if __name__ == "__main__":
    sys.exit(main())
