"""Erros e avisos com posição no código."""


class ErroMeme(Exception):
    etapa = "Erro"

    def __init__(self, mensagem, linha=None, coluna=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna

    def formatar(self, fonte=None, arquivo="<fonte>"):
        """Mensagem com trecho do código e setinha na posição."""
        local = arquivo
        if self.linha is not None:
            local += f":{self.linha}:{self.coluna}"
        texto = f"{self.etapa} em {local}: {self.mensagem}"
        if fonte is not None and self.linha is not None:
            linhas = fonte.split("\n")
            if 1 <= self.linha <= len(linhas):
                trecho = linhas[self.linha - 1].replace("\t", " ")
                num = str(self.linha)
                margem = " " * len(num)
                seta = " " * max((self.coluna or 1) - 1, 0) + "^"
                texto += f"\n  {num} | {trecho}\n  {margem} | {seta}"
        return texto


class ErroLexico(ErroMeme):
    etapa = "Erro léxico"


class ErroSintatico(ErroMeme):
    etapa = "Erro sintático"


class ErroSemantico(ErroMeme):
    etapa = "Erro semântico"


class Aviso(ErroMeme):
    """Aviso que não interrompe a transpilação."""

    etapa = "Aviso"
