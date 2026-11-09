# BRITOCODE

Linguagem estilo C com palavras-chave meméticas (Felipe … Smith), transpilada para Python.

Arquivos-fonte usam a extensão **`.brito`**. Precisa de Python 3.10+. O núcleo do transpilador não tem dependências.

## Como usar

```
python -m britocode programa.brito        # gera programa.py
python -m britocode programa.brito -r     # gera e roda
python -m britocode programa.brito -m     # só mostra o Python
python -m britocode programa.brito -o out.py
python -m britocode programa.brito --tokens
python -m britocode programa.brito --arvore
```

Testes: `python -m unittest -v`

Exemplos em [exemplos/](exemplos/): `ola_mundo`, `fatorial`, `fizzbuzz`, `primos`, `calculadora`, `tipos`, `britto_run` (lógica do jogo).

### IDE (Streamlit, visual VS Code)

```
pip install -r requirements.txt
streamlit run app_streamlit.py
```

Explorer de `.brito`, playground, **Britto Run** (endless runner no navegador) e docs.

## Palavras-chave

| BRITOCODE | Equivale a | Python |
|---|---|---|
| `Felipe` / `Smith` | início / fim | — |
| `Red_bull` / `Jarbas` / `Porra` / `Katrina`… | tipos | `int` / `float` / `str`… |
| `MinhaArte` / `Romero_Britto` / `Faz_Isso_Comigo_Não_Velho` | if / else / else if | `if` / `else` / `elif` |
| `Quebro_VéiVai_Me_Dar_Injeção` | while | `while` |
| `VocêÉDeLá` | for | `for` / `while` |
| `Samu` / `Tô_No_SAMU` | def / chamada | `def` / `nome(...)` |
| `vo_fica_pelado_aqui` | print | `print` |
| `Eu_Tenho_Quantos_Anos_Gente?` | input | `input` |
| `MeuBraço` / `Mata_papai` / `Ce_é_mo_playboy` | continue / break / return | idem |

Keywords com ou sem acento; maiúsculas/minúsculas contam.

## Sintaxe

Comandos com `;`, blocos `{ }`, comentários `//` e `/* */`.

```
Felipe
    Red_bull xs[3] = {1, 2, 3};
    vo_fica_pelado_aqui(xs[0]);
Smith
```

Vetores 1D com tamanho literal. Sem ponteiros, structs ou `do-while`.

## API Python

```python
from britocode import transpilar
codigo, avisos = transpilar(open("programa.brito", encoding="utf-8").read())
```

## Por dentro

```
.brito → lexer → parser → semântico → gerador → .py
```

| Arquivo | Fase |
|---|---|
| [britocode/lexer.py](britocode/lexer.py) | léxico |
| [britocode/parser.py](britocode/parser.py) | sintático |
| [britocode/arvore.py](britocode/arvore.py) | AST |
| [britocode/semantico.py](britocode/semantico.py) | tipos / escopos |
| [britocode/gerador.py](britocode/gerador.py) | Python |
| [britocode/erros.py](britocode/erros.py) | erros |
| [britocode/\_\_main\_\_.py](britocode/__main__.py) | CLI |
