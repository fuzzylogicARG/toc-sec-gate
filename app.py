from flask import Flask, request, redirect, render_template_string
from flask import Flask, request, redirect, render_template_string
import base64
import os

app = Flask(__name__)

SECRET = "TOC2026"

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

def decode_token(token):
    token = token.strip()
    token += "=" * (-len(token) % 4)
    raw = base64.urlsafe_b64decode(token.encode()).decode()
    secret, url = raw.split("|", 1)
    if secret != SECRET:
        raise Exception("Invalid secret")
    return url

@app.route("/")
def home():
    return "TOC Secure Gate Online"

@app.route("/access")
def access():
    token = request.args.get("t", "")
    if not token:
        return "Missing token", 400
    return render_template_string(HTML, token=token)

@app.route("/unlock")
def unlock():
    token = request.args.get("t", "")
    if not token:
        return "Missing token", 400
    try:
        url = decode_token(token)
        return redirect(url)
    except Exception as e:
        return "Access denied: Invalid token", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
