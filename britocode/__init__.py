"""BRITOCODE: transpilador da linguagem memética para Python."""

from .erros import Aviso, ErroLexico, ErroMeme, ErroSemantico, ErroSintatico
from .gerador import Gerador
from .lexer import Lexer, preparar_fonte
from .parser import Parser
from .semantico import Analisador

__version__ = "1.0.0"


def transpilar(fonte, nome_arquivo=None):
    """Código BRITOCODE (.brito) -> (python, avisos). Levanta ErroMeme se houver erro."""
    fonte = preparar_fonte(fonte)
    tokens = Lexer(fonte).tokens()
    programa = Parser(tokens).programa()
    avisos = Analisador().analisar(programa)
    codigo = Gerador().gerar(programa, nome_arquivo)
    return codigo, avisos


__all__ = [
    "transpilar", "preparar_fonte", "Lexer", "Parser", "Analisador", "Gerador",
    "ErroMeme", "ErroLexico", "ErroSintatico", "ErroSemantico", "Aviso",
]
