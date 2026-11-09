"""BRITOCODE IDE — interface Streamlit estilo terminal CRT anos 80."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit_ace import st_ace

from britocode import ErroMeme
from web.britto_player import html_jogador
from web.britto_web import carregar_namespace
from web.ide_styles import injetar
from web.runner import (
    Diagnostico,
    diagnosticar,
    pedidos_entrada,
    rodar_brito,
    transpilar_fonte,
)

ROOT = Path(__file__).resolve().parent
EXEMPLOS_DIR = ROOT / "exemplos"

KEYWORDS = [
    ("Felipe / Smith", "início / fim do programa"),
    ("Red_bull, Jarbas, Porra, Katrina...", "tipos"),
    ("MinhaArte / Romero_Britto / Faz_Isso_Comigo_Não_Velho", "if / else / else if"),
    ("Quebro_VéiVai_Me_Dar_Injeção", "while"),
    ("VocêÉDeLá", "for"),
    ("Samu / Tô_No_SAMU", "declarar / chamar função"),
    ("vo_fica_pelado_aqui", "print"),
    ("Eu_Tenho_Quantos_Anos_Gente?", "input"),
    ("MeuBraço / Mata_papai / Ce_é_mo_playboy", "continue / break / return"),
]

STDIN_PADRAO = {
    "ola_mundo.brito": "",
    "fizzbuzz.brito": "",
    "tipos.brito": "",
    "primos.brito": "",
    "fatorial.brito": "5\n",
    "calculadora.brito": "10\n+\n3\n",
}


def listar_exemplos() -> list[Path]:
    return sorted(
        p for p in EXEMPLOS_DIR.glob("*.brito") if p.name != "britto_run.brito"
    )


@st.cache_data(max_entries=64, show_spinner=False)
def diagnosticar_cache(fonte: str, nome: str) -> list[Diagnostico]:
    return diagnosticar(fonte, nome)


def titlebar(arquivo: str = "") -> None:
    rotulo = "BRITOCODE TERMINAL v1.0"
    if arquivo:
        rotulo += f" :: {arquivo}"
    st.markdown(f'<div class="bc-titlebar">{html.escape(rotulo)}</div>', unsafe_allow_html=True)


def resumo_problemas(diags: list[Diagnostico]) -> tuple[str, str]:
    erros = sum(d.severidade == "erro" for d in diags)
    avisos = len(diags) - erros
    if erros:
        return "bc-status-erro", f"{erros} ERRO" + ("S" if erros > 1 else "")
    if avisos:
        return "bc-status-aviso", f"{avisos} AVISO" + ("S" if avisos > 1 else "")
    return "bc-status-ok", "OK"


def statusbar(extra: str = "", diags: list[Diagnostico] | None = None) -> None:
    txt = "C:\\BRITOCODE&gt;"
    if extra:
        txt += f" {html.escape(extra)}"
    if diags is not None:
        classe, rotulo = resumo_problemas(diags)
        txt += f'&nbsp;&nbsp;<span class="{classe}">{rotulo}</span>'
    else:
        txt += "&nbsp;&nbsp;READY"
    st.markdown(f'<div class="bc-statusbar">{txt}</div>', unsafe_allow_html=True)


def painel_problemas(diags: list[Diagnostico]) -> None:
    erros = sum(d.severidade == "erro" for d in diags)
    avisos = len(diags) - erros
    partes = [
        '<div class="bc-problems">',
        f'<div class="bc-problems-head">PROBLEMS [{erros} ERRO(S), {avisos} AVISO(S)]</div>',
    ]
    if not diags:
        partes.append('<div class="bc-problems-ok">&gt; 0 problemas. Pronto para rodar.</div>')
    for d in diags:
        icone = "[X]" if d.severidade == "erro" else "[!]"
        local = f"linha {d.linha}, coluna {d.coluna}" if d.linha is not None else "sem posição"
        trecho = d.detalhe.split("\n", 1)[1] if "\n" in d.detalhe else ""
        trecho_html = "<br>".join(
            html.escape(linha).replace(" ", "&nbsp;") for linha in trecho.split("\n")
        )
        partes.append(
            f'<div class="bc-problem {d.severidade}">'
            f"<strong>{icone} {html.escape(d.etapa)}</strong> "
            f'<span class="bc-loc">({local})</span><br>'
            f"{html.escape(d.mensagem)}"
            + (f'<div class="bc-trecho">{trecho_html}</div>' if trecho else "")
            + "</div>"
        )
    partes.append("</div>")
    st.markdown("".join(partes), unsafe_allow_html=True)


def anotacoes_ace(diags: list[Diagnostico]) -> list[dict]:
    return [
        {
            "row": d.linha - 1,
            "column": max((d.coluna or 1) - 1, 0),
            "text": f"{d.etapa}: {d.mensagem}",
            "type": "error" if d.severidade == "erro" else "warning",
        }
        for d in diags
        if d.linha is not None
    ]


def editor(nome: str, valor_inicial: str) -> tuple[str, list[Diagnostico]]:
    """Editor Ace com checagem ao vivo; devolve (fonte, diagnósticos)."""
    chave_texto = f"texto_{nome}"
    chave_ace = f"ace_{nome}"
    if chave_texto not in st.session_state:
        st.session_state[chave_texto] = valor_inicial

    atual = st.session_state.get(chave_ace)
    if atual is None:
        atual = st.session_state[chave_texto]
    diags = diagnosticar_cache(atual, nome)

    fonte = st_ace(
        value=st.session_state[chave_texto],
        language="c_cpp",
        theme="gob",
        keybinding="vscode",
        font_size=15,
        tab_size=4,
        show_gutter=True,
        min_lines=16,
        max_lines=28,
        annotations=anotacoes_ace(diags),
        auto_update=True,
        key=chave_ace,
    )
    if fonte is None:
        fonte = atual
    if fonte != atual:
        diags = diagnosticar_cache(fonte, nome)
    st.session_state[chave_texto] = fonte
    return fonte, diags


def painel_resultado(fonte: str, stdin: str, timeout: float, nome: str) -> None:
    with st.spinner("Transpilando..."):
        r = rodar_brito(fonte, stdin_texto=stdin, timeout=timeout, nome=nome)
    if r.erro and not r.codigo_py:
        st.error(r.erro)
        return
    tabs = st.tabs(["TERMINAL", "PYTHON", "STDERR"])
    with tabs[0]:
        st.code(r.saida if r.saida else "(sem saída)", language="text")
        if r.codigo_retorno is not None:
            st.caption(f"exit code {r.codigo_retorno}")
    with tabs[1]:
        st.code(r.codigo_py or "(vazio)", language="python")
    with tabs[2]:
        if r.erro:
            st.code(r.erro, language="text")
        else:
            st.caption("Nenhum erro de execução.")


def campo_entrada(fonte: str, nome: str, stdin_padrao: str) -> str:
    """Campo de entrada dinâmico conforme os Eu_Tenho_Quantos_Anos_Gente? do código."""
    pedidos = pedidos_entrada(fonte)
    n = len(pedidos)
    if n == 0:
        st.markdown(
            '<div class="bc-stdin">'
            '<div class="bc-stdin-head">ENTRADA</div>'
            '<div class="bc-stdin-ok">&gt; Este programa não pede entrada.</div>'
            "</div>",
            unsafe_allow_html=True,
        )
        return ""

    plural = "es" if n != 1 else ""
    linhas = "".join(
        f"<div>{i + 1} → {html.escape(rotulo)}</div>"
        for i, rotulo in enumerate(pedidos)
    )
    st.markdown(
        f'<div class="bc-stdin">'
        f'<div class="bc-stdin-head">ENTRADA · {n} valor{plural} '
        f"(uma resposta por linha)</div>"
        f'<div class="bc-stdin-map">{linhas}</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    chave = f"stdin_{nome}"
    if chave not in st.session_state:
        st.session_state[chave] = stdin_padrao.rstrip("\n")
    return st.text_area(
        "entrada",
        height=max(68, 28 + 22 * n),
        key=chave,
        placeholder="\n".join(pedidos),
        label_visibility="collapsed",
    )


def area_codigo(nome: str, valor_inicial: str, stdin_padrao: str) -> list[Diagnostico]:
    fonte, diags = editor(nome, valor_inicial)
    tem_erro = any(d.severidade == "erro" for d in diags)

    barra = st.container(horizontal=True)
    run = barra.button(
        "[ RUN ]",
        type="primary",
        key=f"run_{nome}",
        disabled=tem_erro,
        help="Corrija os erros em PROBLEMS para rodar." if tem_erro else None,
    )
    only = barra.button("[ TRANSPILE ]", key=f"tr_{nome}")
    stdin = campo_entrada(fonte, nome, stdin_padrao)

    painel_problemas(diags)

    if run:
        painel_resultado(fonte, stdin, 5.0, nome)
    elif only:
        try:
            py, _ = transpilar_fonte(fonte, nome)
            st.tabs(["PYTHON"])[0].code(py, language="python")
        except ErroMeme:
            st.caption("Não dá para transpilar: veja os erros em PROBLEMS.")
    return diags


def view_explorer() -> None:
    arquivos = listar_exemplos()
    nomes = [p.name for p in arquivos]
    if not nomes:
        st.warning("Nenhum .brito em exemplos/.")
        return

    if "ide_arquivo" not in st.session_state:
        st.session_state.ide_arquivo = nomes[0]

    escolha = st.sidebar.radio(
        "EXPLORER",
        nomes,
        index=nomes.index(st.session_state.ide_arquivo)
        if st.session_state.ide_arquivo in nomes
        else 0,
        key="explorer_radio",
    )
    st.session_state.ide_arquivo = escolha
    fonte_disk = (EXEMPLOS_DIR / escolha).read_text(encoding="utf-8")

    titlebar(escolha)
    st.markdown(
        f'<div class="bc-tab"><strong>{escolha}</strong></div>',
        unsafe_allow_html=True,
    )
    diags = area_codigo(escolha, fonte_disk, STDIN_PADRAO.get(escolha, ""))
    statusbar(escolha, diags)


def view_playground() -> None:
    titlebar("playground.brito")
    st.markdown(
        '<div class="bc-tab"><strong>playground.brito</strong> · unsaved</div>',
        unsafe_allow_html=True,
    )
    padrao = (
        "Felipe\n"
        "    Red_bull x = 3;\n"
        "    vo_fica_pelado_aqui(\"x =\", x);\n"
        "Smith\n"
    )
    diags = area_codigo("playground.brito", padrao, "")
    statusbar("playground.brito", diags)


def view_runner() -> None:
    titlebar("Britto Run")
    st.markdown(
        '<div class="bc-tab"><strong>Britto Run</strong> · exemplos/britto_run.brito</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Endless runner BRITOCODE. Espaço/clique = pular. "
        "Felipe (herói), Red_bull (chão), Romero (ar). "
        "Evite clicar na UI do Streamlit durante a partida."
    )
    try:
        _, codigo, avisos = carregar_namespace()
        st.session_state.britto_py = codigo
        for a in avisos:
            st.warning(a)
    except ErroMeme as e:
        fonte = (EXEMPLOS_DIR / "britto_run.brito").read_text(encoding="utf-8")
        st.error(e.formatar(fonte, "britto_run.brito"))
        return

    if st.button("[ REINICIAR ]", key="britto_remount"):
        st.session_state.britto_epoca = int(st.session_state.get("britto_epoca", 0)) + 1
        st.rerun()

    epoca = int(st.session_state.get("britto_epoca", 0))
    components.html(html_jogador(epoca=epoca, autoplay=True), height=320, scrolling=False)

    with st.expander("britto_run.brito"):
        st.code((EXEMPLOS_DIR / "britto_run.brito").read_text(encoding="utf-8"), language="c")
    with st.expander("Python gerado"):
        st.code(st.session_state.get("britto_py", ""), language="python")
    statusbar("britto_run.brito")


def view_docs() -> None:
    titlebar("Docs")
    st.markdown("### BRITOCODE")
    st.markdown(
        "Linguagem estilo C com keywords meméticas, transpilada para Python. "
        "Arquivos `.brito`. CLI: `python -m britocode programa.brito`."
    )
    st.markdown("#### Keywords")
    st.table({"BRITOCODE": [k[0] for k in KEYWORDS], "Significado": [k[1] for k in KEYWORDS]})
    st.markdown(
        """
```
Felipe
    vo_fica_pelado_aqui("Olá, BRITOCODE!");
Smith
```
        """
    )
    statusbar("docs")


def main() -> None:
    st.set_page_config(
        page_title="BRITOCODE",
        page_icon="▮",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    injetar()

    st.sidebar.markdown("### ░▒▓ BRITOCODE ▓▒░")
    st.sidebar.caption("workspace")
    atividade = st.sidebar.radio(
        "ACTIVITY",
        ["EXPLORER", "PLAYGROUND", "RUNNER", "DOCS"],
        label_visibility="collapsed",
        key="activity",
    )
    st.sidebar.markdown("---")

    if atividade == "EXPLORER":
        view_explorer()
    elif atividade == "PLAYGROUND":
        view_playground()
    elif atividade == "RUNNER":
        view_runner()
    else:
        view_docs()


if __name__ == "__main__":
    main()
