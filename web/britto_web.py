"""Carrega a lógica BRITOCODE de Britto Run."""

from __future__ import annotations

from pathlib import Path

from britocode import transpilar

ROOT = Path(__file__).resolve().parent.parent
LOGIC = ROOT / "exemplos" / "britto_run.brito"


def carregar_namespace(caminho: Path | None = None) -> tuple[dict, str, list]:
    path = caminho or LOGIC
    fonte = path.read_text(encoding="utf-8")
    codigo, avisos = transpilar(fonte, path.name)
    ns: dict = {"__name__": "britto_run"}
    exec(compile(codigo, str(path), "exec"), ns)
    return ns, codigo, avisos
