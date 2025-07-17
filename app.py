from flask import Flask, render_template_string, request
import requests
import json

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dify Chat Web</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8fafc; }
        .container { max-width: 800px; margin-top: 60px; background: #fff; border-radius: 12px; box-shadow: 0 2px 16px #0001; padding: 32px; }
        h2 { font-weight: 700; margin-bottom: 24px; }
        .form-label { font-weight: 500; }
        .result-block { background: #f4f4f4; border-radius: 8px; padding: 16px; margin-top: 16px; font-size: 1rem; }
        .btn-primary { min-width: 100px; }
    </style>
</head>
<body>
<div class="container">
    <h2 class="text-center">Dify Chat Web Demo</h2>
    <form method="post" class="mb-3">
        <div class="mb-3">
            <label for="query" class="form-label">请输入问题：</label>
            <input type="text" class="form-control" id="query" name="query" value="{{ query }}" placeholder="如：1000人的活动" required>
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary">提交</button>
        </div>
    </form>
    {% if result %}
    <div>
        <h5>返回结果：</h5>
        <pre class="result-block">{{ result }}</pre>
    </div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    query = ''
    if request.method == 'POST':
        query = request.form.get('query', '')
        url = "https://aigov-dify.bytebroad.com.cn/v1/chat-messages"
        payload = {
            "inputs": {},
            "response_mode": "blocking",
            "auto_generate_name": True,
            "query": query,
            "user": "a",
            "conversation_id": "884ea56b-9663-49aa-9538-517aca3fa03e"
        }
        headers = {
            "Authorization": "Bearer app-PjZrMyjcK0vM5DMOpdphDW4H",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            data = response.json()
            result = json.dumps(data, ensure_ascii=False, indent=4)
        except Exception as e:
            result = f"请求失败: {e}"
    return render_template_string(HTML, result=result, query=query)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
