"""Jogador HTML/JS fluido — Britto Run (temática BRITOCODE)."""

from __future__ import annotations


def html_jogador(*, epoca: int = 0, autoplay: bool = True) -> str:
    auto = "true" if autoplay else "false"
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<style>
  html, body {{ margin: 0; background: #1e1e1e; overflow: hidden; font-family: Consolas, 'Courier New', monospace; }}
  #wrap {{ position: relative; width: 600px; height: 300px; }}
  canvas {{ display: block; width: 600px; height: 300px; border-radius: 4px; border: 1px solid #3c3c3c; cursor: pointer; }}
  #hud {{
    position: absolute; left: 10px; top: 8px; color: #111; font-size: 13px;
    text-shadow: 0 0 4px #fff; pointer-events: none; z-index: 2;
  }}
  #msg {{
    display: none; position: absolute; inset: 0; align-items: center; justify-content: center;
    flex-direction: column; gap: 8px; background: rgba(0,0,0,.55); color: #fff;
    text-align: center; z-index: 3; padding: 1rem; font-size: 14px;
  }}
  #msg button {{
    pointer-events: auto; cursor: pointer; padding: 8px 14px; font: inherit;
    border: 0; border-radius: 4px; background: #007acc; color: #fff;
  }}
</style>
</head>
<body>
<div id="wrap">
  <canvas id="c" width="800" height="400"></canvas>
  <div id="hud">Britto Run · metros: 0 · Espaço/clique = MinhaArte (pular)</div>
  <div id="msg"><div id="msgText"></div><button id="btnRestart" type="button">Rodar de novo</button></div>
</div>
<script>
(function () {{
  const EPOCA = {epoca};
  const AUTOPLAY = {auto};
  const canvas = document.getElementById("c");
  const ctx = canvas.getContext("2d");
  const hud = document.getElementById("hud");
  const msg = document.getElementById("msg");
  const msgText = document.getElementById("msgText");
  const btnRestart = document.getElementById("btnRestart");

  let player_x, player_y, grav, no_chao, ox, ot, seed, vivo, metros, spawn_cd, frames;
  let rodando = false;
  let last = 0;
  const STEP = 1000 / 60;

  function resetar() {{
    player_x = 80; player_y = 300; grav = 0; no_chao = 1;
    seed = 42; vivo = 1; metros = 0; spawn_cd = 0; frames = 0;
    ox = Array(8).fill(-1);
    ot = Array(8).fill(0);
    msg.style.display = "none";
  }}

  function pular() {{
    if (vivo === 1 && no_chao === 1) {{ grav = -17; no_chao = 0; }}
  }}

  function tick() {{
    if (vivo === 0) return;
    grav = grav + 1;
    player_y = player_y + grav;
    if (player_y >= 300) {{ player_y = 300; grav = 0; no_chao = 1; }}

    for (let i = 0; i < 8; i++) {{
      if (ot[i] !== 0) {{
        ox[i] = ox[i] - 5;
        if (ox[i] < -60) ot[i] = 0;
      }}
    }}

    spawn_cd = spawn_cd + 1;
    if (spawn_cd >= 45) {{
      spawn_cd = 0;
      seed = (seed * 17 + 23) % 100;
      for (let i = 0; i < 8; i++) {{
        if (ot[i] === 0) {{
          ox[i] = 820;
          ot[i] = seed < 55 ? 1 : 2;
          break;
        }}
      }}
    }}

    for (let i = 0; i < 8; i++) {{
      if (ot[i] === 1) {{
        if (ox[i] < player_x + 45 && ox[i] + 55 > player_x && player_y > 240) vivo = 0;
      }} else if (ot[i] === 2) {{
        if (ox[i] < player_x + 45 && ox[i] + 50 > player_x && player_y < 250) vivo = 0;
      }}
    }}

    frames = frames + 1;
    if (frames % 60 === 0) metros = metros + 1;
  }}

  function desenhar() {{
    ctx.fillStyle = "#2d2d30";
    ctx.fillRect(0, 0, 800, 400);
    // chão
    ctx.fillStyle = "#007acc";
    ctx.fillRect(0, 300, 800, 100);
    // Felipe
    ctx.fillStyle = "#ce9178";
    ctx.fillRect(player_x, player_y - 70, 45, 70);
    ctx.fillStyle = "#dcdcaa";
    ctx.font = "12px Consolas";
    ctx.fillText("F", player_x + 16, player_y - 40);
    for (let i = 0; i < 8; i++) {{
      if (ot[i] === 1) {{
        // Red_bull (chão)
        ctx.fillStyle = "#c586c0";
        ctx.fillRect(ox[i], 255, 55, 45);
        ctx.fillStyle = "#fff";
        ctx.fillText("Rb", ox[i] + 12, 282);
      }} else if (ot[i] === 2) {{
        // Romero (ar)
        ctx.fillStyle = "#4ec9b0";
        ctx.fillRect(ox[i], 175, 50, 18);
        ctx.fillStyle = "#1e1e1e";
        ctx.fillText("Ro", ox[i] + 12, 188);
      }}
    }}
    hud.textContent = "Britto Run · metros: " + metros + " · Espaço/clique = pular";
    if (vivo === 0) {{
      msgText.innerHTML = "Compile error: Smith fechou o arquivo.<br/>Você andou " + metros + " m · MinhaArte é tentar de novo";
      msg.style.display = "flex";
      rodando = false;
    }}
  }}

  function loop(ts) {{
    if (!rodando) {{ desenhar(); return; }}
    if (!last) last = ts;
    let acc = ts - last;
    if (acc > 200) acc = 200;
    while (acc >= STEP) {{
      tick();
      acc -= STEP;
      if (vivo === 0) break;
    }}
    last = ts - acc;
    desenhar();
    if (rodando) requestAnimationFrame(loop);
  }}

  function iniciar() {{
    resetar();
    rodando = true;
    last = 0;
    requestAnimationFrame(loop);
  }}

  canvas.addEventListener("pointerdown", function () {{
    if (!rodando && vivo === 1) iniciar();
    else pular();
    canvas.focus({{ preventScroll: true }});
  }});
  window.addEventListener("keydown", function (e) {{
    if (e.code === "Space" || e.key === " ") {{
      e.preventDefault();
      if (!rodando && vivo === 1) iniciar();
      else pular();
    }}
  }});
  btnRestart.addEventListener("click", function (e) {{
    e.stopPropagation();
    iniciar();
  }});

  resetar();
  desenhar();
  if (AUTOPLAY) iniciar();
  void EPOCA;
}})();
</script>
</body>
</html>
"""
