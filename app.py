rom flask import Flask, request, redirect, render_template_string, abort
import base64
import hashlib
import hmac
import os
import time

app = Flask(__name__)

# MISMO SECRET que uses en auto_post_V12_PRO.py / toc_config.json
GATE_SECRET = os.environ.get("GATE_SECRET", "TOC2026")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TOC Secure Gate</title>
<style>
body{background:#090d18;color:#fff;font-family:Arial;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
.box{background:#111827;border:1px solid rgba(0,255,255,.25);border-radius:18px;padding:34px;text-align:center;box-shadow:0 0 35px rgba(0,255,255,.18)}
h1{margin:0 0 12px;font-size:30px}
p{opacity:.75}
.wrap{width:330px;height:66px;background:#1f2937;border-radius:15px;overflow:hidden;position:relative;margin-top:24px}
.bar{position:absolute;left:0;top:0;height:100%;width:0;background:linear-gradient(90deg,#00e5ff,#7b61ff,#ff00aa)}
.btn{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;cursor:pointer;user-select:none}
</style>
</head>
<body>
<div class="box">
<h1>🔒 TOC Secure Gate</h1>
<p>Human verification required</p>
<div class="wrap">
<div class="bar" id="bar"></div>
<div class="btn" id="btn">HOLD TO UNLOCK</div>
</div>
</div>
<script>
let btn=document.getElementById("btn");
let bar=document.getElementById("bar");
let p=0,t=null;

function start(){
 if(t) return;
 t=setInterval(function(){
  p+=2;
  bar.style.width=p+"%";
  if(p>=100){
   clearInterval(t);
   window.location.href="/unlock?t={{token}}";
  }
 },70);
}

function stop(){
 clearInterval(t);
 t=null;
 p=0;
 bar.style.width="0%";
}

btn.addEventListener("mousedown",start);
btn.addEventListener("touchstart",start);
btn.addEventListener("mouseup",stop);
btn.addEventListener("mouseleave",stop);
btn.addEventListener("touchend",stop);
</script>
</body>
</html>
"""

def verify_token(token: str):
    try:
        payload_b64, sig = token.rsplit(".", 1)
    except ValueError:
        return None

    expected_sig = hmac.new(
        GATE_SECRET.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, sig):
        return None

    try:
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload = base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8")
        expires_ts_str, real_url = payload.split("|", 1)
        expires_ts = int(expires_ts_str)
    except Exception:
        return None

    if time.time() > expires_ts:
        return None

    if not real_url.startswith("http"):
        return None

    return real_url

@app.route("/")
def home():
    return "TOC Secure Gate Online - HMAC Mode"

@app.route("/access")
def access():
    token = request.args.get("t", "")
    if not token:
        return "Missing token", 400

    # Validamos antes de mostrar el gate
    if not verify_token(token):
        return "Access denied: invalid or expired token", 403

    return render_template_string(HTML, token=token)

@app.route("/unlock")
def unlock():
    token = request.args.get("t", "")
    if not token:
        return "Missing token", 400

    real_url = verify_token(token)
    if not real_url:
        return "Access denied: invalid or expired token", 403

    return redirect(real_url, code=302)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
