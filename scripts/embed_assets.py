#!/usr/bin/env python3
"""Embed real image assets into a single HTML file.

How to use:
1) Put your files in a folder called `assets/` at the repo root.
   Example names:
   - assets/background.jpg
   - assets/object-clock.png
   - assets/object-suitcase.png
   - assets/object-gramophone.png
   - assets/object-phone.png
   - assets/doll.png
2) Run:
      python3 scripts/embed_assets.py
3) It will generate:
      index-real-images.html
"""

from __future__ import annotations
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
OUTPUT_HTML = ROOT / "index-real-images.html"


ASSET_FILES = {
    "background": "background.jpg",
    "clock": "object-clock.png",
    "suitcase": "object-suitcase.png",
    "gramophone": "object-gramophone.png",
    "phone": "object-phone.png",
    "doll": "doll.png",
}


def ensure_assets_exist() -> None:
    missing = []
    for key, file_name in ASSET_FILES.items():
        path = ASSETS_DIR / file_name
        if not path.exists():
            missing.append(str(path.relative_to(ROOT)))
    if missing:
        raise FileNotFoundError(
            "Faltan imágenes en la carpeta assets. Deben existir estas rutas:\n"
            + "\n".join(f" - {p}" for p in missing)
        )


def to_data_url(path: Path) -> str:
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(path.suffix.lower(), "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_html(assets: dict[str, str]) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Restas Vintage</title>
  <style>
    :root {{
      --bg-warm: #d9c2a3;
      --panel: rgba(255, 249, 240, 0.92);
      --wood: #8d5d3b;
      --brown-dark: #3f2617;
      --green: #2d745f;
      --gold: #e7b84b;
      --red: #b54432;
      --blue: #0d5f88;
      --button-green: #35a95d;
      --button-blue: #1e7cc0;
      --button-gold: #eab64f;
      --shadow: rgba(0, 0, 0, 0.22);
    }}

    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0; width: 100%; height: 100%; font-family: Arial, Helvetica, sans-serif;
      background: var(--bg-warm);
    }}
    body {{ overflow: hidden; }}

    .game {{
      width: 100vw; height: 100vh; position: relative; display: flex; flex-direction: column;
      background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.15)),
                  url(\"{assets['background']}\") center center / cover no-repeat;
    }}

    .topbar {{
      position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 10px; padding: 12px 18px; background: rgba(58, 34, 23, 0.78); color: white;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }}

    .title {{ margin: 0; font-size: clamp(1.2rem, 3vw, 2rem); font-weight: 700; letter-spacing: 0.04em; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
    .badge {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18); border-radius: 999px; padding: 8px 12px; font-size: clamp(0.8rem,2vw,1rem); font-weight: 600; }}
    .timer {{ color: #ffe38b; font-weight: 900; }}
    .timer.warning {{ color: #ff7f7f; animation: pulse 0.5s infinite; }}
    @keyframes pulse {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.12); }} }}

    .board {{
      position: relative; z-index: 1; display: grid; grid-template-columns: 170px minmax(0, 1fr);
      gap: 16px; width: min(1120px, calc(100% - 24px)); margin: 16px auto 0; flex: 1; min-height: 0;
    }}

    .side {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 12px; padding: 12px 6px; }}
    .doll-wrap {{ width: 100%; display: flex; justify-content: center; align-items: center; min-height: 180px; }}
    .doll {{
      width: 120px; height: 170px; display: flex; align-items: center; justify-content: center;
      filter: drop-shadow(2px 6px 4px rgba(0,0,0,0.35)); transition: transform 0.3s ease;
      user-select: none; background-image: url(\"{assets['doll']}\"); background-size: contain; background-repeat: no-repeat; background-position: center;
    }}
    .doll.celebrate {{ animation: celebrate 0.7s ease; }}
    .doll.fall {{ animation: fall 0.6s ease forwards; }}
    .doll.standup {{ animation: standup 0.5s ease; }}
    @keyframes celebrate {{ 0%,100% {{ transform: translateY(0) rotate(0deg); }} 25% {{ transform: translateY(-16px) rotate(-7deg); }} 50% {{ transform: translateY(-22px) rotate(7deg); }} 75% {{ transform: translateY(-12px) rotate(-4deg); }} }}
    @keyframes fall {{ 0% {{ transform: rotate(0deg) translateY(0); }} 100% {{ transform: rotate(80deg) translateY(36px); }} }}
    @keyframes standup {{ 0% {{ transform: rotate(80deg) translateY(36px); }} 100% {{ transform: rotate(0deg) translateY(0); }} }}

    .progress {{ width: 100%; height: 18px; background: rgba(255,255,255,0.35); border-radius: 999px; overflow: hidden; border: 1px solid rgba(0,0,0,0.12); box-shadow: inset 0 2px 4px rgba(0,0,0,0.12); }}
    .progress-fill {{ height: 100%; width: 10%; background: linear-gradient(90deg, #51b765, #2f8d55); border-radius: inherit; transition: width 0.3s ease; display: flex; align-items: center; justify-content: center; font-size: 0.62rem; color: white; font-weight: 700; }}

    .panel {{
      background: var(--panel); border-radius: 22px; border: 4px solid var(--wood);
      box-shadow: 0 8px 25px var(--shadow); padding: clamp(12px, 2.8vw, 24px);
      display: flex; flex-direction: column; gap: 16px; min-width: 0;
    }}

    .instructions {{
      display: flex; align-items: center; justify-content: space-between; gap: 10px;
      background: #fff2cb; border: 2px solid #d7b56c; border-radius: 12px; padding: 10px 12px;
      font-size: clamp(0.85rem, 2vw, 1.02rem); line-height: 1.4; color: #3d2c1f; text-align: left;
    }}
    .instructions span {{ flex: 1; }}
    .speak-btn {{ border: none; width: 40px; height: 40px; border-radius: 50%; background: var(--green); color: white; font-size: 1.2rem; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }}
    .speak-btn:hover {{ filter: brightness(1.05); }}

    .operation {{ text-align: center; font-size: clamp(2.1rem, 7vw, 5rem); font-weight: 900; letter-spacing: 0.04em; line-height: 1.1; color: #2c231d; }}
    .operation .num {{ color: var(--red); }}
    .operation .op {{ color: var(--blue); }}

    .objects {{ width: 100%; min-height: 120px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: center; background: rgba(214,196,163,0.75); border: 2px solid rgba(71,46,25,0.2); border-radius: 16px; padding: 14px; overflow: auto; }}
    .object {{
      width: 80px; height: 80px; background: rgba(255,255,255,0.85); border-radius: 14px; border: 2px solid rgba(85,56,34,0.42); display: grid; place-items: center; cursor: grab; user-select: none; box-shadow: 0 4px 8px rgba(0,0,0,0.12); transition: transform 0.15s ease, opacity 0.15s ease;
      overflow: hidden;
    }}
    .object img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
    .object:hover {{ transform: translateY(-2px) scale(1.02); }}
    .object.dragging {{ opacity: 0.6; transform: scale(1.12); cursor: grabbing; }}
    .object.used {{ opacity: 0.25; pointer-events: none; filter: grayscale(1); }}

    .count {{ text-align: center; font-weight: 800; font-size: clamp(1rem,2.6vw,1.5rem); color: var(--blue); }}

    .dropzone {{
      width: min(360px, 100%); height: 110px; margin: 0 auto; border: 3px dashed #513927; border-radius: 18px;
      background: linear-gradient(135deg, #a56d3f, #75471f); color: white; display: grid; place-items: center; text-align: center; font-size: clamp(0.9rem, 2.5vw, 1.15rem); font-weight: 800; box-shadow: inset 0 3px 10px rgba(0,0,0,0.2); transition: transform 0.15s ease, outline 0.15s ease;
    }}
    .dropzone.drag-over {{ transform: scale(1.02); outline: 4px solid rgba(255, 232, 140, 0.8); }}

    .feedback {{ min-height: 32px; text-align: center; font-weight: 900; font-size: clamp(1.1rem, 2.5vw, 1.6rem); letter-spacing: 0.04em; }}
    .feedback.success {{ color: #1d8b47; }}
    .feedback.error {{ color: #b33a33; }}

    .actions {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }}
    .btn {{ border: none; border-radius: 12px; padding: 12px 18px; min-width: 150px; font-size: clamp(0.9rem, 2vw, 1rem); font-weight: 800; letter-spacing: 0.04em; color: white; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.18); transition: transform 0.15s ease, filter 0.15s ease; }}
    .btn:hover {{ transform: translateY(-1px); filter: brightness(1.04); }}
    .btn.verify {{ background: var(--button-green); }}
    .btn.retry {{ background: var(--button-gold); color: #2a1a12; }}
    .btn.next {{ background: var(--button-blue); }}
    .hidden {{ display: none !important; }}

    .progress-bar {{ width: 100%; height: 16px; background: rgba(0,0,0,0.12); border-radius: 999px; overflow: hidden; border: 1px solid rgba(0,0,0,0.15); }}
    .progress-bar > div {{ width: 10%; height: 100%; background: linear-gradient(90deg, #42b26a, #2a8d56); transition: width 0.25s ease; }}

    .confetti {{ position: fixed; width: 12px; height: 18px; pointer-events: none; z-index: 40; animation: confetti-fall 1.8s ease-in forwards; }}
    @keyframes confetti-fall {{ 0% {{ opacity: 1; transform: translateY(-20px) rotate(0deg); }} 100% {{ opacity: 0; transform: translateY(100vh) rotate(720deg); }} }}

    .modal {{ position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px; }}
    .modal.show {{ display: flex; }}
    .modal-card {{ background: #fff9f0; width: min(480px, 100%); border-radius: 18px; border: 4px solid var(--brown-dark); box-shadow: 0 12px 30px rgba(0,0,0,0.26); padding: 22px 20px 18px; text-align: center; }}
    .modal-card h2 {{ margin: 0 0 12px; font-size: clamp(1.6rem, 5vw, 2.2rem); color: #2d251f; }}
    .modal-card p {{ margin: 0 0 18px; font-size: clamp(1rem, 2.4vw, 1.2rem); color: #2c2c2c; }}

    @media (max-width: 780px) {{
      body {{ overflow: auto; }}
      .game {{ min-height: 100vh; height: auto; }}
      .board {{ grid-template-columns: 1fr; width: min(760px, calc(100% - 18px)); }}
      .side {{ order: 2; padding-top: 0; }}
      .panel {{ order: 1; }}
      .doll {{ width: 90px; height: 130px; }}
      .objects {{ min-height: 100px; }}
      .object {{ width: 62px; height: 62px; }}
    }}

    @media (max-width: 480px) {{
      .topbar {{ justify-content: center; text-align: center; }}
      .stats {{ justify-content: center; }}
      .instructions {{ flex-direction: column; }}
      .btn {{ min-width: 120px; }}
      .dropzone {{ height: 96px; }}
    }}
  </style>
</head>
<body>
  <div class=\"game\">
    <header class=\"topbar\">
      <h1 class=\"title\">🎓 Restas Vintage</h1>
      <div class=\"stats\">
        <div class=\"badge\">Pregunta: <strong id=\"questionLabel\">1</strong>/10</div>
        <div class=\"badge\">Tiempo: <strong id=\"timer\" class=\"timer\">60</strong>s</div>
        <div class=\"badge\">Puntos: <strong id=\"score\">0</strong></div>
      </div>
    </header>

    <div class=\"board\">
      <aside class=\"side\">
        <div class=\"doll-wrap\">
          <div id=\"doll\" class=\"doll\" aria-label=\"Protagonista\"></div>
        </div>
        <div class=\"progress\" aria-hidden=\"true\">
          <div id=\"progressFill\" class=\"progress-fill\">10%</div>
        </div>
      </aside>

      <section class=\"panel\">
        <div class=\"instructions\">
          <span id=\"instructionsText\">Observa la resta. Arrastra los objetos al contenedor y luego presiona Verificar.</span>
          <button id=\"speakBtn\" class=\"speak-btn\" type=\"button\" aria-label=\"Escuchar instrucciones\">🔊</button>
        </div>

        <div id=\"operation\" class=\"operation\">
          <span id=\"numA\" class=\"num\">7</span>
          <span class=\"op\">−</span>
          <span id=\"numB\" class=\"num\">3</span>
          <span class=\"op\">= ?</span>
        </div>

        <div id=\"objects\" class=\"objects\" aria-label=\"Objetos para arrastrar\"></div>

        <div id=\"count\" class=\"count\">Objetos restantes: <span id=\"remaining\">7</span></div>

        <div id=\"dropzone\" class=\"dropzone\" aria-label=\"Zona para arrastrar objetos\">🗃️<br>Arrastra aquí</div>

        <div id=\"feedback\" class=\"feedback\" aria-live=\"polite\"></div>

        <div class=\"actions\">
          <button id=\"verifyBtn\" class=\"btn verify\" type=\"button\">Verificar ✓</button>
          <button id=\"retryBtn\" class=\"btn retry hidden\" type=\"button\">Intentar de nuevo</button>
          <button id=\"nextBtn\" class=\"btn next hidden\" type=\"button\">Siguiente →</button>
        </div>

        <div class=\"progress-bar\" aria-hidden=\"true\"><div id=\"sessionBar\"></div></div>
      </section>
    </div>
  </div>

  <div id=\"modal\" class=\"modal\" aria-live=\"polite\">
    <div class=\"modal-card\">
      <h2>🎉 ¡Sesión terminada!</h2>
      <p id=\"finalText\">Obtuviste 0/10.</p>
      <button id=\"restartBtn\" class=\"btn verify\" type=\"button\">Jugar de nuevo 🔄</button>
    </div>
  </div>

  <script>
    const state = {{
      question: 1,
      score: 0,
      time: 60,
      timerId: null,
      currentA: 0,
      currentB: 0,
      left: 0,
      used: 0,
      answered: false,
      readyForNext: false,
    }};

    const assetMap = {{
      clock: \"{assets['clock']}\",
      suitcase: \"{assets['suitcase']}\",
      gramophone: \"{assets['gramophone']}\",
      phone: \"{assets['phone']}\",
      doll: \"{assets['doll']}\",
    }};

    const objects = [
      {{ image: assetMap.clock, alt: 'Reloj' }},
      {{ image: assetMap.suitcase, alt: 'Maleta' }},
      {{ image: assetMap.gramophone, alt: 'Gramófono' }},
      {{ image: assetMap.phone, alt: 'Teléfono' }}
    ];

    const els = {{
      questionLabel: document.getElementById('questionLabel'),
      timer: document.getElementById('timer'),
      score: document.getElementById('score'),
      numA: document.getElementById('numA'),
      numB: document.getElementById('numB'),
      remaining: document.getElementById('remaining'),
      objects: document.getElementById('objects'),
      feedback: document.getElementById('feedback'),
      progressFill: document.getElementById('progressFill'),
      sessionBar: document.getElementById('sessionBar'),
      doll: document.getElementById('doll'),
      verifyBtn: document.getElementById('verifyBtn'),
      retryBtn: document.getElementById('retryBtn'),
      nextBtn: document.getElementById('nextBtn'),
      modal: document.getElementById('modal'),
      finalText: document.getElementById('finalText'),
      dropzone: document.getElementById('dropzone')
    }};

    function rand(min, max) {{
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }}

    function setFeedback(text, type) {{
      els.feedback.textContent = text;
      els.feedback.className = 'feedback';
      if (type) els.feedback.classList.add(type);
    }}

    function resetDoll() {{
      els.doll.classList.remove('celebrate', 'fall', 'standup');
      void els.doll.offsetWidth;
      els.doll.classList.add('standup');
      setTimeout(() => els.doll.classList.remove('standup'), 500);
    }}

    function createQuestion() {{
      state.answered = false;
      state.readyForNext = false;
      state.time = 60;
      state.currentA = state.question <= 5 ? rand(2, 5) : rand(5, 10);
      state.currentB = rand(1, state.currentA);
      state.left = state.currentA;
      state.used = 0;

      els.numA.textContent = state.currentA;
      els.numB.textContent = state.currentB;
      els.remaining.textContent = state.left;
      els.questionLabel.textContent = state.question;
      els.timer.textContent = state.time;
      els.timer.classList.remove('warning');
      els.feedback.textContent = '';
      els.feedback.className = 'feedback';
      els.objects.innerHTML = '';
      els.verifyBtn.classList.remove('hidden');
      els.retryBtn.classList.add('hidden');
      els.nextBtn.classList.add('hidden');

      const selected = objects[Math.floor(Math.random() * objects.length)];
      for (let i = 0; i < state.currentA; i++) {{
        const obj = document.createElement('div');
        obj.className = 'object';
        obj.draggable = true;
        obj.setAttribute('aria-label', selected.alt);
        const img = document.createElement('img');
        img.src = selected.image;
        img.alt = selected.alt;
        obj.appendChild(img);

        obj.addEventListener('dragstart', (e) => {{
          if (state.answered) return;
          obj.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
        }});
        obj.addEventListener('dragend', () => obj.classList.remove('dragging'));
        obj.addEventListener('click', () => addToRest(obj));
        els.objects.appendChild(obj);
      }}

      const progressPercent = (state.question / 10) * 100;
      els.progressFill.style.width = `${{progressPercent}}%`;
      els.progressFill.textContent = `${{state.question}}/10`;
      els.sessionBar.style.width = `${{progressPercent}}%`;
      startTimer();
    }}

    function addToRest(obj) {{
      if (state.answered) return;
      if (obj.classList.contains('used')) return;
      if (state.used >= state.currentB) return;

      obj.classList.add('used');
      state.used += 1;
      state.left -= 1;
      els.remaining.textContent = state.left;
    }}

    function verifyAnswer() {{
      if (state.answered) return;
      state.answered = true;
      clearInterval(state.timerId);

      const correct = state.used === state.currentB && state.left === state.currentA - state.currentB;

      if (correct) {{
        state.score += 1;
        els.score.textContent = state.score;
        setFeedback('✓ ¡Correcto!', 'success');
        els.doll.classList.remove('fall', 'standup');
        void els.doll.offsetWidth;
        els.doll.classList.add('celebrate');
        createConfetti();
        els.verifyBtn.classList.add('hidden');
        els.nextBtn.classList.remove('hidden');
        state.readyForNext = true;
      }} else {{
        setFeedback('✗ Inténtalo de nuevo', 'error');
        els.doll.classList.remove('celebrate', 'standup');
        void els.doll.offsetWidth;
        els.doll.classList.add('fall');
        els.verifyBtn.classList.add('hidden');
        els.retryBtn.classList.remove('hidden');
      }}
    }}

    function retryQuestion() {{
      resetDoll();
      state.answered = false;
      state.time = 60;
      state.used = 0;
      state.left = state.currentA;
      els.remaining.textContent = state.left;
      document.querySelectorAll('.object').forEach((obj) => obj.classList.remove('used'));
      els.retryBtn.classList.add('hidden');
      els.verifyBtn.classList.remove('hidden');
      els.feedback.textContent = '';
      els.feedback.className = 'feedback';
      startTimer();
    }}

    function nextQuestion() {{
      if (state.question >= 10) {{
        finishGame();
        return;
      }}
      state.question += 1;
      createQuestion();
    }}

    function finishGame() {{
      clearInterval(state.timerId);
      els.finalText.textContent = `Obtuviste ${{state.score}} de 10 respuestas correctas.`;
      els.modal.classList.add('show');
    }}

    function startTimer() {{
      clearInterval(state.timerId);
      els.timer.textContent = state.time;
      els.timer.classList.remove('warning');

      state.timerId = setInterval(() => {{
        if (state.answered) return;
        state.time -= 1;
        els.timer.textContent = state.time;
        if (state.time <= 10) els.timer.classList.add('warning');
        if (state.time <= 0) {{
          clearInterval(state.timerId);
          verifyAnswer();
        }}
      }}, 1000);
    }}

    function createConfetti() {{
      const colors = ['#e74c3c', '#f1c40f', '#2ecc71', '#3498db', '#ec4899'];
      for (let i = 0; i < 40; i++) {{
        const piece = document.createElement('div');
        piece.className = 'confetti';
        piece.style.left = `${{Math.random() * 100}}vw`;
        piece.style.top = '-20px';
        piece.style.background = colors[Math.floor(Math.random() * colors.length)];
        piece.style.transform = `rotate(${{Math.random() * 360}}deg)`;
        document.body.appendChild(piece);
        setTimeout(() => piece.remove(), 1800);
      }}
    }}

    function setupDropZone() {{
      const zone = els.dropzone;
      zone.addEventListener('dragover', (e) => {{ e.preventDefault(); zone.classList.add('drag-over'); }});
      zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
      zone.addEventListener('drop', (e) => {{
        e.preventDefault(); zone.classList.remove('drag-over');
        const dragging = document.querySelector('.object.dragging');
        if (dragging) addToRest(dragging);
      }});
      zone.addEventListener('click', () => {{
        const firstUnused = document.querySelector('.object:not(.used)');
        if (firstUnused) addToRest(firstUnused);
      }});
    }}

    function speakInstructions() {{
      const text = 'Observa la resta. Arrastra los objetos al contenedor y luego presiona Verificar.';
      if (!('speechSynthesis' in window)) {{
        alert('La lectura en voz alta no está disponible en este navegador.');
        return;
      }}
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'es-MX';
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      window.speechSynthesis.speak(utterance);
    }}

    document.getElementById('speakBtn').addEventListener('click', speakInstructions);
    els.verifyBtn.addEventListener('click', verifyAnswer);
    els.retryBtn.addEventListener('click', retryQuestion);
    els.nextBtn.addEventListener('click', nextQuestion);
    document.getElementById('restartBtn').addEventListener('click', () => {{
      els.modal.classList.remove('show');
      state.question = 1;
      state.score = 0;
      els.score.textContent = '0';
      createQuestion();
    }});

    setupDropZone();
    createQuestion();
  </script>
</body>
</html>
"""


def main() -> None:
    ensure_assets_exist()
    assets = {name: to_data_url(ASSETS_DIR / file_name) for name, file_name in ASSET_FILES.items()}
    OUTPUT_HTML.write_text(build_html(assets), encoding="utf-8")
    print(f"Archivo generado: {OUTPUT_HTML.relative_to(ROOT)}")
    print("Abre ese archivo en el navegador para ver el juego con tus imágenes reales.")


if __name__ == "__main__":
    main()
