"""CSS estilo terminal CRT anos 80 (fósforo verde) para o Streamlit BRITOCODE."""

CRT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&display=swap');

:root {
  --crt-bg: #0a0f0a;
  --crt-bg2: #0f1a0f;
  --crt-fg: #33ff66;
  --crt-dim: #1f8f3f;
  --crt-amber: #ffb000;
  --crt-red: #ff4040;
  --crt-glow: 0 0 4px currentColor;
  --crt-title: 'VT323', 'Share Tech Mono', monospace;
  --crt-mono: 'Share Tech Mono', Consolas, 'Courier New', monospace;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background-color: var(--crt-bg) !important;
  color: var(--crt-fg) !important;
  font-family: var(--crt-mono) !important;
}
[data-testid="stAppViewContainer"] {
  background: radial-gradient(ellipse at center, #0d1a0d 0%, var(--crt-bg) 75%) !important;
  animation: crt-flicker 6s infinite;
}
[data-testid="stAppViewContainer"]::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 999999;
  background:
    repeating-linear-gradient(to bottom, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px, rgba(0,0,0,0.28) 3px),
    radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,0.55) 100%);
}
@keyframes crt-flicker {
  0%, 100% { opacity: 1; }
  48% { opacity: 1; }
  50% { opacity: 0.97; }
  52% { opacity: 1; }
}
@keyframes crt-blink { 50% { opacity: 0; } }

[data-testid="stHeader"] {
  background: var(--crt-bg) !important;
  border-bottom: 1px solid var(--crt-dim) !important;
}
[data-testid="stSidebar"] {
  background-color: var(--crt-bg2) !important;
  border-right: 2px solid var(--crt-dim) !important;
}
[data-testid="stSidebar"] * {
  color: var(--crt-fg) !important;
  font-family: var(--crt-title) !important;
  font-size: 1.15rem !important;
}
[data-testid="stSidebar"] h3 { font-size: 1.6rem !important; text-shadow: var(--crt-glow); }
.block-container { padding-top: 4.5rem !important; max-width: 100% !important; }

h1, h2, h3, h4 {
  color: var(--crt-fg) !important;
  font-family: var(--crt-title) !important;
  text-shadow: var(--crt-glow);
  letter-spacing: 1px;
}
.stMarkdown p, .stMarkdown li, .stCaption, label, [data-testid="stCaptionContainer"] {
  color: var(--crt-fg) !important;
  font-family: var(--crt-mono) !important;
}
[data-testid="stCaptionContainer"] { color: var(--crt-dim) !important; }
a { color: var(--crt-amber) !important; }
hr { border-color: var(--crt-dim) !important; }
::selection { background: var(--crt-fg); color: var(--crt-bg); }

/* inputs */
div[data-baseweb="textarea"] textarea,
.stTextArea textarea,
.stTextInput input {
  background: #000 !important;
  color: var(--crt-fg) !important;
  caret-color: var(--crt-fg) !important;
  font-family: var(--crt-mono) !important;
  border: 1px solid var(--crt-dim) !important;
  border-radius: 0 !important;
  text-shadow: var(--crt-glow);
}
.stTextInput input::placeholder { color: var(--crt-dim) !important; }
div[data-baseweb="input"], div[data-baseweb="base-input"] {
  background: #000 !important;
  border-radius: 0 !important;
  border: none !important;
}

/* botões */
.stButton > button {
  background: transparent !important;
  color: var(--crt-fg) !important;
  border: 2px solid var(--crt-fg) !important;
  border-radius: 0 !important;
  font-family: var(--crt-title) !important;
  font-size: 1.25rem !important;
  letter-spacing: 1px;
  text-shadow: var(--crt-glow);
  box-shadow: 0 0 6px rgba(51,255,102,0.35);
}
.stButton > button p {
  font-family: var(--crt-title) !important;
  font-size: 1.25rem !important;
  white-space: nowrap;
}
.stButton > button:hover:enabled {
  background: var(--crt-fg) !important;
  color: var(--crt-bg) !important;
  text-shadow: none;
}
.stButton > button[kind="primary"] {
  color: var(--crt-amber) !important;
  border-color: var(--crt-amber) !important;
  box-shadow: 0 0 6px rgba(255,176,0,0.35);
}
.stButton > button[kind="primary"]:hover:enabled {
  background: var(--crt-amber) !important;
  color: var(--crt-bg) !important;
}
.stButton > button:disabled {
  color: var(--crt-dim) !important;
  border-color: var(--crt-dim) !important;
  box-shadow: none;
  text-shadow: none;
  opacity: 0.6;
}

/* código */
[data-testid="stCode"], [data-testid="stCode"] pre, pre, code {
  background: #000 !important;
  color: var(--crt-fg) !important;
  font-family: var(--crt-mono) !important;
  border-radius: 0 !important;
}
[data-testid="stCode"] { border: 1px dashed var(--crt-dim) !important; }
[data-testid="stCode"] span { color: var(--crt-fg) !important; }
[data-testid="stCode"] .token.keyword,
[data-testid="stCode"] .token.builtin { color: var(--crt-amber) !important; }
[data-testid="stCode"] .token.string { color: #9dff9d !important; }
[data-testid="stCode"] .token.comment { color: var(--crt-dim) !important; }
.stMarkdown code { border: none !important; color: var(--crt-amber) !important; }

/* abas */
[data-baseweb="tab-list"], [role="tablist"] {
  border-bottom: 1px solid var(--crt-dim) !important;
  gap: 4px;
}
[data-baseweb="tab"], [role="tab"] {
  background: transparent !important;
  color: var(--crt-dim) !important;
  font-family: var(--crt-title) !important;
  border-radius: 0 !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 12px !important;
}
[role="tab"] * { color: inherit !important; }
[role="tab"] p { font-family: var(--crt-title) !important; font-size: 1.2rem !important; }
[role="tab"][aria-selected="true"] {
  background: var(--crt-fg) !important;
  color: var(--crt-bg) !important;
}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"],
[role="tab"] .react-aria-SelectionIndicator { display: none !important; }

/* radios, tabelas, alertas, expanders */
[role="radiogroup"] label div:first-child { border-color: var(--crt-fg) !important; }
table, th, td {
  border: 1px solid var(--crt-dim) !important;
  color: var(--crt-fg) !important;
  background: #000 !important;
  font-family: var(--crt-mono) !important;
}
th { color: var(--crt-amber) !important; }
[data-testid="stAlert"] > div, [data-testid="stAlertContainer"] {
  background: #000 !important;
  border-radius: 0 !important;
  border: 1px solid var(--crt-amber) !important;
  color: var(--crt-amber) !important;
}
[data-testid="stAlert"] * { color: inherit !important; font-family: var(--crt-mono) !important; }
[data-testid="stExpander"] details {
  border: 1px solid var(--crt-dim) !important;
  border-radius: 0 !important;
  background: #000 !important;
}
[data-testid="stExpander"] summary p { font-family: var(--crt-title) !important; font-size: 1.2rem !important; }
[data-testid="stSpinner"] * { color: var(--crt-fg) !important; }

/* barras próprias */
.bc-titlebar {
  background: var(--crt-fg);
  color: var(--crt-bg);
  padding: 2px 12px;
  font-family: var(--crt-title);
  font-size: 1.3rem;
  letter-spacing: 2px;
  box-shadow: 0 0 10px rgba(51,255,102,0.5);
  margin: -1rem -1rem 0.75rem -1rem;
}
.bc-statusbar {
  border-top: 1px solid var(--crt-dim);
  color: var(--crt-fg);
  padding: 4px 10px;
  font-family: var(--crt-title);
  font-size: 1.2rem;
  text-shadow: var(--crt-glow);
  margin: 0.75rem -1rem -1rem -1rem;
}
.bc-statusbar::after {
  content: "\\2588";
  margin-left: 6px;
  animation: crt-blink 1s steps(1) infinite;
}
.bc-status-ok { color: var(--crt-fg); }
.bc-status-aviso { color: var(--crt-amber); }
.bc-status-erro { color: var(--crt-red); animation: crt-blink 1.2s steps(1) infinite; }
.bc-tab {
  font-family: var(--crt-title);
  font-size: 1.2rem;
  color: var(--crt-dim);
  padding: 2px 4px;
  border-bottom: 1px dashed var(--crt-dim);
  margin-bottom: 8px;
}
.bc-tab strong { color: var(--crt-fg); font-weight: normal; text-shadow: var(--crt-glow); }
.bc-tab::before { content: "> "; color: var(--crt-fg); }

/* editor ace (iframe) */
iframe[title="streamlit_ace.streamlit_ace"] {
  border: 2px solid var(--crt-dim) !important;
  box-shadow: 0 0 12px rgba(51,255,102,0.25);
  background: #000;
}

/* entrada (stdin) */
.bc-stdin {
  border: 1px solid var(--crt-dim);
  background: #000;
  margin: 8px 0 4px 0;
  font-family: var(--crt-mono);
}
.bc-stdin-head {
  font-family: var(--crt-title);
  font-size: 1.2rem;
  padding: 2px 10px;
  border-bottom: 1px solid var(--crt-dim);
  color: var(--crt-fg);
  letter-spacing: 1px;
}
.bc-stdin-map {
  padding: 6px 10px;
  color: var(--crt-amber);
  font-size: 0.9rem;
  line-height: 1.45;
}
.bc-stdin-ok {
  padding: 6px 10px;
  color: var(--crt-dim);
}

/* painel PROBLEMS */
.bc-problems {
  border: 1px solid var(--crt-dim);
  background: #000;
  margin: 8px 0;
  font-family: var(--crt-mono);
}
.bc-problems-head {
  font-family: var(--crt-title);
  font-size: 1.2rem;
  padding: 2px 10px;
  border-bottom: 1px solid var(--crt-dim);
  color: var(--crt-fg);
  letter-spacing: 1px;
}
.bc-problems-ok { padding: 6px 10px; color: var(--crt-fg); text-shadow: var(--crt-glow); }
.bc-problem { padding: 6px 10px; border-left: 4px solid; margin: 6px; }
.bc-problem.erro { border-color: var(--crt-red); color: var(--crt-red); }
.bc-problem.aviso { border-color: var(--crt-amber); color: var(--crt-amber); }
.bc-problem .bc-loc { opacity: 0.8; }
.bc-trecho {
  margin: 4px 0 0 0;
  padding: 4px 8px;
  border-top: 1px dashed currentColor;
  white-space: pre;
  overflow-x: auto;
  font-size: 0.85rem;
}
</style>
"""


def injetar() -> None:
    import streamlit as st
    st.markdown(CRT_CSS, unsafe_allow_html=True)
