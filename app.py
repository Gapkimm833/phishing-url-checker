from flask import Flask, request, render_template
from urllib.parse import urlparse

app = Flask(__name__)

def is_phishing(url):
    # คำต้องสงสัยที่ใช้ในเว็บ phishing
    keywords = ['login', 'secure', 'update', 'verify', 'bank']
    
    # คำที่พบบ่อยในเว็บพนัน
    gambling_keywords = ['bet', 'casino', 'slot', 'หวย', 'แทงบอล', 'บาคาร่า', 'สล็อต', 'พนัน']

    domain = urlparse(url).netloc.lower()
    full_url = url.lower()

    # ตรวจหา keyword ของ phishing
    if any(k in full_url for k in keywords):
        return True

    # ตรวจหา keyword ของเว็บพนัน
    if any(g in full_url for g in gambling_keywords):
        return True

    # ตรวจความยาว domain ว่ายาวผิดปกติไหม
    if len(domain) > 30:
        return True

    return False

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        if is_phishing(url):
            result = "⚠️ URL นี้อาจเป็นเว็บไซต์หลอกลวงหรือเว็บพนัน"
        else:
            result = "✅ URL นี้ดูปลอดภัย"
    return render_template("index.html", result=result)

import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)