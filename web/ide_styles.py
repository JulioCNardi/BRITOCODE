"""CSS estilo Visual Studio Code Dark+ para o Streamlit BRITOCODE."""

VSCODE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
  background-color: #1e1e1e !important;
  color: #cccccc !important;
}
[data-testid="stHeader"] { background: #3c3c3c !important; }
[data-testid="stSidebar"] {
  background-color: #252526 !important;
  border-right: 1px solid #1e1e1e !important;
}
[data-testid="stSidebar"] * { color: #cccccc !important; }
.block-container { padding-top: 1rem !important; max-width: 100% !important; }

h1, h2, h3, .stMarkdown p, .stCaption, label { color: #cccccc !important; }
a { color: #3794ff !important; }

div[data-baseweb="textarea"] textarea,
.stTextArea textarea {
  background-color: #1e1e1e !important;
  color: #d4d4d4 !important;
  font-family: 'IBM Plex Mono', Consolas, 'Courier New', monospace !important;
  font-size: 13px !important;
  border: 1px solid #3c3c3c !important;
  border-radius: 0 !important;
  line-height: 1.45 !important;
}
.stTextInput input {
  background: #3c3c3c !important;
  color: #cccccc !important;
  border: 1px solid #3c3c3c !important;
  border-radius: 2px !important;
  font-family: 'IBM Plex Mono', Consolas, monospace !important;
}

.stButton > button {
  background: #0e639c !important;
  color: #fff !important;
  border: 1px solid #007acc !important;
  border-radius: 2px !important;
  font-family: system-ui, sans-serif !important;
}
.stButton > button:hover { background: #1177bb !important; border-color: #1c97ea !important; }

[data-testid="stCode"], pre, code {
  background: #1e1e1e !important;
  color: #d4d4d4 !important;
  font-family: 'IBM Plex Mono', Consolas, monospace !important;
  border: 1px solid #3c3c3c !important;
}

hr { border-color: #3c3c3c !important; }

.bc-titlebar {
  background: #3c3c3c;
  color: #cccccc;
  padding: 6px 12px;
  font-size: 12px;
  font-family: system-ui, sans-serif;
  border-bottom: 1px solid #1e1e1e;
  margin: -1rem -1rem 0.75rem -1rem;
}
.bc-statusbar {
  background: #007acc;
  color: #fff;
  padding: 2px 10px;
  font-size: 12px;
  font-family: system-ui, sans-serif;
  margin: 0.75rem -1rem -1rem -1rem;
}
.bc-tab {
  font-size: 12px;
  color: #969696;
  padding: 4px 10px;
  border-bottom: 1px solid #3c3c3c;
  margin-bottom: 8px;
}
.bc-tab strong { color: #fff; font-weight: 500; }
</style>
"""


def injetar() -> None:
    import streamlit as st
    st.markdown(VSCODE_CSS, unsafe_allow_html=True)
