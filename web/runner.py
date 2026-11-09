"""Transpila e executa código BRITOCODE com stdin/stdout capturados."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from britocode import ErroMeme, transpilar


@dataclass
class ResultadoExecucao:
    codigo_py: str
    avisos: list[str]
    saida: str
    erro: str
    codigo_retorno: int | None


def transpilar_fonte(fonte: str, nome: str = "programa.brito") -> tuple[str, list[str]]:
    codigo, avisos = transpilar(fonte, nome)
    return codigo, [a.formatar(fonte, nome) for a in avisos]


def executar_python(
    codigo_py: str,
    stdin_texto: str = "",
    timeout: float = 5.0,
) -> tuple[str, str, int | None]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".py", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(codigo_py)
        caminho = tmp.name
    try:
        proc = subprocess.run(
            [sys.executable, caminho],
            input=stdin_texto,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return "", f"Tempo esgotado ({timeout:.0f}s). Loop ou esperando input?", None
    finally:
        Path(caminho).unlink(missing_ok=True)


def rodar_brito(
    fonte: str,
    stdin_texto: str = "",
    timeout: float = 5.0,
    nome: str = "programa.brito",
) -> ResultadoExecucao:
    try:
        codigo_py, avisos = transpilar_fonte(fonte, nome)
    except ErroMeme as e:
        return ResultadoExecucao("", [], "", e.formatar(fonte, nome), None)
    saida, stderr, rc = executar_python(codigo_py, stdin_texto, timeout)
    return ResultadoExecucao(codigo_py, avisos, saida, stderr.strip(), rc)


# alias compat
rodar_meme = rodar_brito
