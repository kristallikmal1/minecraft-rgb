

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
            margin-bottom: 10px;
            font-size: 40px;
            font-weight: bold;
            background: linear-gradient(to right, #007bff, #00bfff); /* Сине-голубой градиент */
            -webkit-background-clip: text; /* Для Chrome, Safari */
            background-clip: text; /* Современные браузеры */
            color: transparent; /* Сделаем текст прозрачным, чтобы показывался только градиент */
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
        <h1>RGBO → Minecraft §x.</h1>
        <p class="subtitle">Создай цветной и форматированный текст для Minecraft</p>

        <!-- Остальной код сайта -->
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
