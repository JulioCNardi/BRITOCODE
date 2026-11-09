"""Transpila e executa código BRITOCODE com stdin/stdout capturados."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from britocode import ErroMeme, transpilar

_LEIA_INI = re.compile(r"Eu_Tenho_Quantos_Anos_Gente\?\s*\(")
_STR_RE = re.compile(r'"(?:\\.|[^"\\])*"')
_ID_RE = re.compile(r"[A-Za-z_À-ÿ][\wÀ-ÿ]*")


def _args_leia(fonte: str, inicio: int) -> str | None:
    """Conteúdo entre parênteses de um Eu_Tenho_Quantos_Anos_Gente?, respeitando strings."""
    i = inicio
    n = len(fonte)
    profundidade = 1
    while i < n and profundidade:
        c = fonte[i]
        if c == '"':
            m = _STR_RE.match(fonte, i)
            if not m:
                return None
            i = m.end()
            continue
        if c == "(":
            profundidade += 1
        elif c == ")":
            profundidade -= 1
            if profundidade == 0:
                return fonte[inicio:i]
        i += 1
    return None


def _desescapar(texto: str) -> str:
    return (
        texto.replace("\\\\", "\0")
        .replace('\\"', '"')
        .replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace("\0", "\\")
    )


def pedidos_entrada(fonte: str) -> list[str]:
    """Rótulos das linhas de stdin, na ordem dos Eu_Tenho_Quantos_Anos_Gente?."""
    pedidos: list[str] = []
    for m in _LEIA_INI.finditer(fonte):
        args = _args_leia(fonte, m.end())
        if args is None:
            continue
        args = args.strip()
        if not args:
            pedidos.append("valor")
            continue
        strings = _STR_RE.findall(args)
        prompt = None
        resto = args
        if strings:
            prompt = _desescapar(strings[0][1:-1])
            for s in strings:
                resto = resto.replace(s, "", 1)
        ids = _ID_RE.findall(resto)
        if ids:
            for i, nome in enumerate(ids):
                if i == 0 and prompt is not None:
                    pedidos.append(prompt.rstrip() or nome)
                else:
                    pedidos.append(nome)
        else:
            pedidos.append((prompt or "valor").rstrip())
    return pedidos


@dataclass
class ResultadoExecucao:
    codigo_py: str
    avisos: list[str]
    saida: str
    erro: str
    codigo_retorno: int | None


@dataclass
class Diagnostico:
    severidade: str
    etapa: str
    mensagem: str
    linha: int | None
    coluna: int | None
    detalhe: str


def _diagnostico(e: ErroMeme, severidade: str, fonte: str, nome: str) -> Diagnostico:
    return Diagnostico(
        severidade, e.etapa, e.mensagem, e.linha, e.coluna, e.formatar(fonte, nome)
    )


def diagnosticar(fonte: str, nome: str = "programa.brito") -> list[Diagnostico]:
    """Erros e avisos da linguagem, sem executar o programa."""
    if not fonte.strip():
        return []
    try:
        _, avisos = transpilar(fonte, nome)
    except ErroMeme as e:
        return [_diagnostico(e, "erro", fonte, nome)]
    return [_diagnostico(a, "aviso", fonte, nome) for a in avisos]


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
