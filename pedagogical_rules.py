"""Načítanie spoločných verziovaných pedagogických pravidiel AI tútorov.

Pravidlá sa pripájajú k pôvodným odborným inštrukciám. Zdrojové texty nemeníme.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

RULES_PATH = Path(__file__).resolve().with_name("tutor_rules.txt")
VALID_MODES = {"explanation": "EXPLANATION", "dialogue": "DIALOGUE"}


def read_sections(path: Path = RULES_PATH) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    sections: dict[str, list[str]] = {}
    current = None
    for line in raw.splitlines():
        marker = line.strip()
        if marker in ("[COMMON]", "[EXPLANATION]", "[DIALOGUE]"):
            current = marker[1:-1]
            if current in sections:
                raise ValueError(f"Zdvojená sekcia pedagogických pravidiel: {current}")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    for key in ("COMMON", "EXPLANATION", "DIALOGUE"):
        if key not in sections or not "\n".join(sections[key]).strip():
            raise ValueError(f"Prázdna alebo chýbajúca sekcia v {path.name}: {key}")
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def rules_digest(path: Path = RULES_PATH) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def add_pedagogical_rules(base_instructions: str, mode: str, path: Path = RULES_PATH) -> str:
    if mode not in VALID_MODES:
        raise ValueError(f"Neznámy režim: {mode}")
    sections = read_sections(path)
    return (base_instructions.strip() + "\n\n"
            + "=== SPOLOČNÉ PEDAGOGICKÉ PRAVIDLÁ v1.1 ===\n"
            + sections["COMMON"] + "\n\n"
            + sections[VALID_MODES[mode]] + "\n")
