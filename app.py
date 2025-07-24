from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Minecraft §x Цветной Текст</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Jockey+One&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            background: #1e1e1e;
            border-radius: 12px;
            padding: 30px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #bb86fc;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 14px;
            color: #aaa;
            margin-bottom: 30px;
        }
        .color-preview {
            width: 100%;
            height: 100px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: background 0.3s;
        }
        .sliders {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }
        .slider-group label {
            display: flex;
            justify-content: space-between;
        }
        input[type="range"] {
            width: 100%;
        }
        .text-input {
            margin: 20px 0;
        }
        .text-input label {
            display: block;
            margin-bottom: 8px;
        }
        .text-input input {
            width: 100%;
            padding: 12px;
            border: 1px solid #333;
            border-radius: 6px;
            background: #2d2d2d;
            color: white;
            font-size: 16px;
        }
        .chat-preview {
            margin-top: 20px;
            padding: 15px;
            background: #2d2d2d;
            border-radius: 6px;
            min-height: 60px;
            font-family: 'Jockey One', sans-serif;
            font-size: 22px;
            letter-spacing: 1px;
            word-break: break-word;
            border: 1px solid #444;
        }
        .format-options {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 15px 0;
        }
        .format-options label {
            font-size: 14px;
        }
        .format-options code {
            background: #333;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 12px;
        }
        .output {
            margin-top: 20px;
            padding: 15px;
            background: #2d2d2d;
            border-radius: 6px;
            font-family: monospace;
            word-break: break-all;
            position: relative;
        }
        .output button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #bb86fc;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        .output button:hover {
            background: #a370d8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>RGBO → Minecraft §x</h1>
        <p class="subtitle">Создай цветной и форматированный текст для Minecraft</p>

        <div class="color-preview" id="preview"></div>

        <div class="sliders">
            <div class="slider-group">
                <label>R: <span id="r-value">255</span></label>
                <input type="range" min="0" max="255" value="255" id="r" oninput="update()">
            </div>
            <div class="slider-group">
                <label>G: <span id="g-value">255</span></label>
                <input type="range" min="0" max="255" value="255" id="g" oninput="update()">
            </div>
            <div class="slider-group">
                <label>B: <span id="b-value">255</span></label>
                <input type="range" min="0" max="255" value="255" id="b" oninput="update()">
            </div>
        </div>

        <div class="text-input">
            <label for="text">Текст:</label>
            <input type="text" id="text" placeholder="Привет, Мир!" value="Привет, Мир!" oninput="update()">
        </div>

        <div class="format-options">
            <label><input type="checkbox" id="bold" oninput="update()"> Жирный (<code>§l</code>)</label>
            <label><input type="checkbox" id="italic" oninput="update()"> Курсив (<code>§o</code>)</label>
            <label><input type="checkbox" id="underline" oninput="update()"> Подчёркивание (<code>§n</code>)</label>
            <label><input type="checkbox" id="strikethrough" oninput="update()"> Зачёркивание (<code>§m</code>)</label>
            <label><input type="checkbox" id="reset" oninput="update()" checked> Добавить сброс (<code>§r</code>)</label>
        </div>

        <div class="chat-preview" id="chat-preview">Привет, Мир!</div>

        <div class="output">
            <div id="hex">HEX: #FFFFFF</div>
            <div id="rgb">RGB: 255, 255, 255</div>
            <div id="mc">Minecraft: §x§F§F§F§F§F§F</div>
            <button onclick="copyText()">Копировать</button>
        </div>

        <!-- Подпись с ссылкой -->
        <div style="text-align: center; margin-top: 30px; color: #777; font-size: 14px;">
            by <a href="https://bio.site/kristallik_mal" target="_blank" style="color: #bb86fc; font-weight: bold; text-decoration: none;">
                kristallik_mal
            </a>
        </div>
    </div>

    <script>
        function update() {
            const r = parseInt(document.getElementById("r").value);
            const g = parseInt(document.getElementById("g").value);
            const b = parseInt(document.getElementById("b").value);
            const text = document.getElementById("text").value || "Пример";

            const isBold = document.getElementById("bold").checked;
            const isItalic = document.getElementById("italic").checked;
            const isUnderline = document.getElementById("underline").checked;
            const isStrikethrough = document.getElementById("strikethrough").checked;
            const addReset = document.getElementById("reset").checked;

            const color = `rgb(${r}, ${g}, ${b})`;
            document.getElementById("preview").style.background = color;

            const hex = "#" + 
                ((1 << 24) + (r << 16) + (g << 8) + b)
                .toString(16).slice(1).toUpperCase();
            document.getElementById("hex").textContent = "HEX: " + hex;
            document.getElementById("rgb").textContent = `RGB: ${r}, ${g}, ${b}`;

            let mcCode = "§x";
            for (const char of hex.slice(1)) {
                mcCode += `§${char}`;
            }
            if (isBold) mcCode += "§l";
            if (isItalic) mcCode += "§o";
            if (isUnderline) mcCode += "§n";
            if (isStrikethrough) mcCode += "§m";
            if (addReset) mcCode += "§r";

            document.getElementById("mc").textContent = "Minecraft: " + mcCode;

            document.getElementById("chat-preview").textContent = text;
            document.getElementById("chat-preview").style.color = color;
            document.getElementById("chat-preview").style.fontWeight = isBold ? "bold" : "normal";
            document.getElementById("chat-preview").style.fontStyle = isItalic ? "italic" : "normal";
            document.getElementById("chat-preview").style.textDecoration = 
                (isUnderline ? "underline " : "") + (isStrikethrough ? "line-through" : "");
        }

        function copyText() {
            const mcText = document.getElementById("mc").textContent.replace("Minecraft: ", "");
            navigator.clipboard.writeText(mcText).then(() => {
                alert("Скопировано: " + mcText);
            }).catch(err => {
                alert("Ошибка копирования: " + err);
            });
        }

        update();
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)