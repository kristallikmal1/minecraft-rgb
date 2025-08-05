from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>RGB для Pisya</title>
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
            margin-bottom: 10px;
            font-size: 40px;
            font-weight: bold;
            color: #007bff;
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
        .gradient-preview {
            width: 100%;
            height: 50px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
        .color-palette {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 5px;
            margin: 15px 0;
        }
        .color-swatch {
            width: 100%;
            height: 30px;
            border-radius: 4px;
            cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.2s, border-color 0.2s;
        }
        .color-swatch:hover {
            transform: scale(1.1);
            border-color: white;
        }
        .gradient-controls {
            margin: 15px 0;
            padding: 15px;
            background: #252525;
            border-radius: 8px;
        }
        .gradient-controls label {
            display: block;
            margin-bottom: 5px;
        }
        .tab-buttons {
            display: flex;
            margin-bottom: 15px;
        }
        .tab-button {
            padding: 8px 15px;
            background: #333;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
        }
        .tab-button.active {
            background: #bb86fc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>RGB для Pisya</h1>
        <p class="subtitle">Создай цветной и форматированный текст для Minecraft</p>

        <div class="tab-buttons">
            <button class="tab-button active" onclick="switchTab('solid')">Один цвет</button>
            <button class="tab-button" onclick="switchTab('gradient')">Градиент</button>
        </div>

        <!-- Solid Color Tab -->
        <div id="solid-tab">
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
        </div>

        <!-- Gradient Tab -->
        <div id="gradient-tab" style="display: none;">
            <div class="gradient-preview" id="gradient-preview"></div>
            
            <div class="gradient-controls">
                <label>Начальный цвет:</label>
                <div class="sliders">
                    <div class="slider-group">
                        <label>R: <span id="r1-value">255</span></label>
                        <input type="range" min="0" max="255" value="255" id="r1" oninput="updateGradient()">
                    </div>
                    <div class="slider-group">
                        <label>G: <span id="g1-value">0</span></label>
                        <input type="range" min="0" max="255" value="0" id="g1" oninput="updateGradient()">
                    </div>
                    <div class="slider-group">
                        <label>B: <span id="b1-value">0</span></label>
                        <input type="range" min="0" max="255" value="0" id="b1" oninput="updateGradient()">
                    </div>
                </div>
                
                <label>Конечный цвет:</label>
                <div class="sliders">
                    <div class="slider-group">
                        <label>R: <span id="r2-value">0</span></label>
                        <input type="range" min="0" max="255" value="0" id="r2" oninput="updateGradient()">
                    </div>
                    <div class="slider-group">
                        <label>G: <span id="g2-value">255</span></label>
                        <input type="range" min="0" max="255" value="255" id="g2" oninput="updateGradient()">
                    </div>
                    <div class="slider-group">
                        <label>B: <span id="b2-value">0</span></label>
                        <input type="range" min="0" max="255" value="0" id="b2" oninput="updateGradient()">
                    </div>
                </div>
            </div>
        </div>

        <!-- Палитра цветов -->
        <div class="color-palette">
            <div class="color-swatch" style="background: #FF0000;" onclick="setColor(255, 0, 0)"></div>
            <div class="color-swatch" style="background: #00FF00;" onclick="setColor(0, 255, 0)"></div>
            <div class="color-swatch" style="background: #0000FF;" onclick="setColor(0, 0, 255)"></div>
            <div class="color-swatch" style="background: #FFFF00;" onclick="setColor(255, 255, 0)"></div>
            <div class="color-swatch" style="background: #FF00FF;" onclick="setColor(255, 0, 255)"></div>
            <div class="color-swatch" style="background: #00FFFF;" onclick="setColor(0, 255, 255)"></div>
            <div class="color-swatch" style="background: #FFFFFF;" onclick="setColor(255, 255, 255)"></div>
            <div class="color-swatch" style="background: #FFA500;" onclick="setColor(255, 165, 0)"></div>
            <div class="color-swatch" style="background: #A52A2A;" onclick="setColor(165, 42, 42)"></div>
            <div class="color-swatch" style="background: #008000;" onclick="setColor(0, 128, 0)"></div>
            <div class="color-swatch" style="background: #000080;" onclick="setColor(0, 0, 128)"></div>
            <div class="color-swatch" style="background: #800080;" onclick="setColor(128, 0, 128)"></div>
            <div class="color-swatch" style="background: #FFC0CB;" onclick="setColor(255, 192, 203)"></div>
            <div class="color-swatch" style="background: #40E0D0;" onclick="setColor(64, 224, 208)"></div>
            <div class="color-swatch" style="background: #FF6347;" onclick="setColor(255, 99, 71)"></div>
            <div class="color-swatch" style="background: #7CFC00;" onclick="setColor(124, 252, 0)"></div>
        </div>

        <!-- Ввод текста -->
        <div class="text-input">
            <label for="text">Текст:</label>
            <input type="text" id="text" placeholder="Привет, Pisya!" value="Привет, Pisya!" oninput="update()">
        </div>

        <!-- Форматирование -->
        <div class="format-options">
            <label><input type="checkbox" id="bold" oninput="update()"> Жирный (<code>&l</code>)</label>
            <label><input type="checkbox" id="italic" oninput="update()"> Курсив (<code>&o</code>)</label>
            <label><input type="checkbox" id="underline" oninput="update()"> Подчёркивание (<code>&n</code>)</label>
            <label><input type="checkbox" id="strikethrough" oninput="update()"> Зачёркивание (<code>&m</code>)</label>
            <label><input type="checkbox" id="reset" oninput="update()" checked> Добавить сброс (<code>&r</code>)</label>
        </div>

        <!-- Превью чата -->
        <div class="chat-preview" id="chat-preview">Привет, Pisya!</div>

        <!-- Вывод кода -->
        <div class="output">
            <div id="hex">HEX: #FFFFFF</div>
            <div id="rgb">RGB: 255, 255, 255</div>
            <div id="mc">Minecraft: &x&F&F&F&F&F&F</div>
            <button onclick="copyText()">Копировать</button>
        </div>

        <!-- Подпись -->
        <div style="text-align: center; margin-top: 30px; color: #777; font-size: 14px;">
            by <a href="https://bio-36t7.onrender.com" target="_blank" style="color: #bb86fc; font-weight: bold; text-decoration: none;">
                kristallik_mal
            </a>
        </div>
    </div>

    <script>
        let currentTab = 'solid';
        
        function switchTab(tab) {
            currentTab = tab;
            document.getElementById('solid-tab').style.display = tab === 'solid' ? 'block' : 'none';
            document.getElementById('gradient-tab').style.display = tab === 'gradient' ? 'block' : 'none';
            
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.toggle('active', btn.textContent === (tab === 'solid' ? 'Один цвет' : 'Градиент'));
            });
            
            update();
        }
        
        function setColor(r, g, b) {
            document.getElementById("r").value = r;
            document.getElementById("g").value = g;
            document.getElementById("b").value = b;
            document.getElementById("r-value").textContent = r;
            document.getElementById("g-value").textContent = g;
            document.getElementById("b-value").textContent = b;
            update();
        }
        
        function rgbToHex(r, g, b) {
            return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase();
        }
        
        function generateMinecraftCode(hex) {
            let mcCode = "&x";
            for (const char of hex.slice(1)) {
                mcCode += `&${char}`;
            }
            return mcCode;
        }
        
        function update() {
            if (currentTab === 'solid') {
                updateSolidColor();
            } else {
                updateGradient();
            }
        }
        
        function updateSolidColor() {
            const r = parseInt(document.getElementById("r").value);
            const g = parseInt(document.getElementById("g").value);
            const b = parseInt(document.getElementById("b").value);
            const text = document.getElementById("text").value || "Пример";
            
            document.getElementById("r-value").textContent = r;
            document.getElementById("g-value").textContent = g;
            document.getElementById("b-value").textContent = b;
            
            const color = `rgb(${r}, ${g}, ${b})`;
            document.getElementById("preview").style.background = color;
            
            const hex = rgbToHex(r, g, b);
            document.getElementById("hex").textContent = "HEX: " + hex;
            document.getElementById("rgb").textContent = `RGB: ${r}, ${g}, ${b}`;
            
            const isBold = document.getElementById("bold").checked;
            const isItalic = document.getElementById("italic").checked;
            const isUnderline = document.getElementById("underline").checked;
            const isStrikethrough = document.getElementById("strikethrough").checked;
            const addReset = document.getElementById("reset").checked;
            
            let mcCode = generateMinecraftCode(hex);
            if (isBold) mcCode += "&l";
            if (isItalic) mcCode += "&o";
            if (isUnderline) mcCode += "&n";
            if (isStrikethrough) mcCode += "&m";
            if (addReset) mcCode += "&r";
            
            document.getElementById("mc").textContent = "Minecraft: " + mcCode + text;
            
            document.getElementById("chat-preview").textContent = text;
            document.getElementById("chat-preview").style.background = "none";
            document.getElementById("chat-preview").style.color = color;
            document.getElementById("chat-preview").style.fontWeight = isBold ? "bold" : "normal";
            document.getElementById("chat-preview").style.fontStyle = isItalic ? "italic" : "normal";
            document.getElementById("chat-preview").style.textDecoration = 
                (isUnderline ? "underline " : "") + (isStrikethrough ? "line-through" : "");
        }
        
        function updateGradient() {
            const r1 = parseInt(document.getElementById("r1").value);
            const g1 = parseInt(document.getElementById("g1").value);
            const b1 = parseInt(document.getElementById("b1").value);
            const r2 = parseInt(document.getElementById("r2").value);
            const g2 = parseInt(document.getElementById("g2").value);
            const b2 = parseInt(document.getElementById("b2").value);
            const text = document.getElementById("text").value || "Пример";
            
            document.getElementById("r1-value").textContent = r1;
            document.getElementById("g1-value").textContent = g1;
            document.getElementById("b1-value").textContent = b1;
            document.getElementById("r2-value").textContent = r2;
            document.getElementById("g2-value").textContent = g2;
            document.getElementById("b2-value").textContent = b2;
            
            const color1 = `rgb(${r1}, ${g1}, ${b1})`;
            const color2 = `rgb(${r2}, ${g2}, ${b2})`;
            document.getElementById("gradient-preview").style.background = 
                `linear-gradient(to right, ${color1}, ${color2})`;
            
            const hex1 = rgbToHex(r1, g1, b1);
            const hex2 = rgbToHex(r2, g2, b2);
            document.getElementById("hex").textContent = `HEX: ${hex1} → ${hex2}`;
            document.getElementById("rgb").textContent = `RGB: ${r1},${g1},${b1} → ${r2},${g2},${b2}`;
            
            const isBold = document.getElementById("bold").checked;
            const isItalic = document.getElementById("italic").checked;
            const isUnderline = document.getElementById("underline").checked;
            const isStrikethrough = document.getElementById("strikethrough").checked;
            const addReset = document.getElementById("reset").checked;
            
            let mcCode = generateGradientCode(text, {r: r1, g: g1, b: b1}, {r: r2, g: g2, b: b2});
            
            if (isBold) mcCode += "&l";
            if (isItalic) mcCode += "&o";
            if (isUnderline) mcCode += "&n";
            if (isStrikethrough) mcCode += "&m";
            if (addReset) mcCode += "&r";
            
            document.getElementById("mc").textContent = "Minecraft: " + mcCode;
            
            // Update chat preview with gradient
            let gradientText = '';
            for (let i = 0; i < text.length; i++) {
                const ratio = i / (text.length - 1);
                const r = Math.round(r1 + ratio * (r2 - r1));
                const g = Math.round(g1 + ratio * (g2 - g1));
                const b = Math.round(b1 + ratio * (b2 - b1));
                gradientText += `<span style="color: rgb(${r},${g},${b})">${text[i]}</span>`;
            }
            
            document.getElementById("chat-preview").innerHTML = gradientText;
            document.getElementById("chat-preview").style.fontWeight = isBold ? "bold" : "normal";
            document.getElementById("chat-preview").style.fontStyle = isItalic ? "italic" : "normal";
            document.getElementById("chat-preview").style.textDecoration = 
                (isUnderline ? "underline " : "") + (isStrikethrough ? "line-through" : "");
        }
        
        function generateGradientCode(text, startColor, endColor) {
            let result = "";
            const steps = text.length;
            
            for (let i = 0; i < steps; i++) {
                const ratio = i / (steps - 1);
                const r = Math.round(startColor.r + ratio * (endColor.r - startColor.r));
                const g = Math.round(startColor.g + ratio * (endColor.g - startColor.g));
                const b = Math.round(startColor.b + ratio * (endColor.b - startColor.b));
                
                const hex = rgbToHex(r, g, b);
                result += generateMinecraftCode(hex) + text[i];
            }
            
            return result;
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
    app.run(host='0.0.0.0', port=10000)
