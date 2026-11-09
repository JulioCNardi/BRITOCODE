"""BRITOCODE IDE — interface Streamlit estilo Visual Studio Code."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from britocode import ErroMeme
from web.britto_player import html_jogador
from web.britto_web import carregar_namespace
from web.ide_styles import injetar
from web.runner import rodar_brito, transpilar_fonte

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
    "primos.brito": "17\n",
    "fatorial.brito": "5\n",
    "calculadora.brito": "10\n+\n3\n",
}


def listar_exemplos() -> list[Path]:
    return sorted(
        p for p in EXEMPLOS_DIR.glob("*.brito") if p.name != "britto_run.brito"
    )


def titlebar(arquivo: str = "") -> None:
    rotulo = f"{arquivo} — BRITOCODE" if arquivo else "BRITOCODE"
    st.markdown(f'<div class="bc-titlebar">{rotulo}</div>', unsafe_allow_html=True)


def statusbar(extra: str = "") -> None:
    txt = "BRITOCODE  ·  UTF-8  ·  .brito"
    if extra:
        txt += f"  ·  {extra}"
    st.markdown(f'<div class="bc-statusbar">{txt}</div>', unsafe_allow_html=True)


def painel_resultado(fonte: str, stdin: str, timeout: float, nome: str) -> None:
    with st.spinner("Transpilando..."):
        r = rodar_brito(fonte, stdin_texto=stdin, timeout=timeout, nome=nome)
    for aviso in r.avisos:
        st.warning(aviso)
    if r.erro and not r.codigo_py:
        st.error(r.erro)
        return
    tabs = st.tabs(["TERMINAL", "PYTHON", "PROBLEMS"])
    with tabs[0]:
        st.code(r.saida if r.saida else "(sem saída)", language="text")
        if r.codigo_retorno is not None:
            st.caption(f"exit code {r.codigo_retorno}")
    with tabs[1]:
        st.code(r.codigo_py or "(vazio)", language="python")
    with tabs[2]:
        if r.erro:
            st.error(r.erro)
        else:
            st.caption("Nenhum problema.")


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
    caminho = EXEMPLOS_DIR / escolha
    fonte_disk = caminho.read_text(encoding="utf-8")

    titlebar(escolha)
    st.markdown(
        f'<div class="bc-tab"><strong>{escolha}</strong></div>',
        unsafe_allow_html=True,
    )

    key_ed = f"editor_{escolha}"
    if key_ed not in st.session_state:
        st.session_state[key_ed] = fonte_disk

    c1, c2, c3 = st.columns([1, 1, 3])
    run = c1.button("▶ Run", type="primary", key="btn_run")
    only = c2.button("Transpile", key="btn_tr")

    fonte = st.text_area(
        "editor",
        height=360,
        key=key_ed,
        label_visibility="collapsed",
    )
    stdin = st.text_input(
        "stdin",
        value=STDIN_PADRAO.get(escolha, ""),
        key=f"stdin_{escolha}",
        placeholder="stdin (uma linha por input)",
    )

    if run:
        painel_resultado(fonte, stdin, 5.0, escolha)
    elif only:
        try:
            py, avisos = transpilar_fonte(fonte, escolha)
            for a in avisos:
                st.warning(a)
            st.tabs(["PYTHON"])[0].code(py, language="python")
        except ErroMeme as e:
            st.error(e.formatar(fonte, escolha))

    statusbar(escolha)


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
    if "pg_fonte" not in st.session_state:
        st.session_state.pg_fonte = padrao
    c1, c2, _ = st.columns([1, 1, 3])
    run = c1.button("▶ Run", type="primary", key="pg_run")
    only = c2.button("Transpile", key="pg_tr")
    fonte = st.text_area("pg", height=360, key="pg_fonte", label_visibility="collapsed")
    stdin = st.text_input("pg_stdin", value="", key="pg_stdin", placeholder="stdin")
    if run:
        painel_resultado(fonte, stdin, 5.0, "playground.brito")
    elif only:
        try:
            py, avisos = transpilar_fonte(fonte, "playground.brito")
            for a in avisos:
                st.warning(a)
            st.code(py, language="python")
        except ErroMeme as e:
            st.error(e.formatar(fonte, "playground.brito"))
    statusbar("playground")


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

    if st.button("Reiniciar quadro", key="britto_remount"):
        st.session_state.britto_epoca = int(st.session_state.get("britto_epoca", 0)) + 1
        st.rerun()

    epoca = int(st.session_state.get("britto_epoca", 0))
    components.html(html_jogador(epoca=epoca, autoplay=True), height=320, scrolling=False)

    with st.expander("britto_run.brito"):
        st.code((EXEMPLOS_DIR / "britto_run.brito").read_text(encoding="utf-8"), language="c")
    with st.expander("Python gerado"):
        st.code(st.session_state.get("britto_py", ""), language="python")
    statusbar("Britto Run")


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
        page_icon="⬛",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    injetar()

    st.sidebar.markdown("### BRITOCODE")
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
