from flask import Flask, request, redirect, render_template_string
import base64
import os

app = Flask(__name__)

# Must match SECURE_GATE_SECRET in the Python uploader/repair scripts.
SECRET = os.getenv("GATE_SECRET", "TOC2026")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TOC Secure Access</title>
<style>
body{
  background:#0b1020;
  color:white;
  font-family:Arial,Helvetica,sans-serif;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
  margin:0;
  overflow:hidden;
}
body:before{
  content:"";
  position:fixed;
  inset:0;
  background:radial-gradient(circle at top left,rgba(0,229,255,.18),transparent 32%),radial-gradient(circle at bottom right,rgba(255,0,170,.18),transparent 32%),linear-gradient(135deg,#070b12,#111827);
}
.box{
  position:relative;
  width:92%;
  max-width:460px;
  background:rgba(18,25,43,.92);
  border-radius:22px;
  padding:34px 28px;
  text-align:center;
  border:1px solid rgba(0,255,255,.25);
  box-shadow:0 0 40px rgba(0,255,255,.16),0 0 50px rgba(255,0,170,.10);
}
.badge{
  display:inline-block;
  padding:7px 16px;
  border-radius:999px;
  background:linear-gradient(90deg,#ff00aa,#00e5ff);
  font-size:11px;
  font-weight:900;
  letter-spacing:.15em;
  margin-bottom:18px;
}
.title{
  font-size:31px;
  font-weight:900;
  margin-bottom:10px;
}
.sub{
  opacity:.78;
  margin-bottom:26px;
  line-height:1.45;
}
.wrap{
  width:100%;
  height:68px;
  background:#1a2238;
  border-radius:16px;
  overflow:hidden;
  position:relative;
  border:1px solid rgba(255,255,255,.10);
  box-shadow:0 0 24px rgba(0,229,255,.12);
}
.progress{
  position:absolute;
  top:0;
  left:0;
  height:100%;
  width:0%;
  background:linear-gradient(90deg,#00e5ff,#7b61ff,#ff00aa);
  transition:width .08s linear;
}
.btn{
  position:absolute;
  inset:0;
  display:flex;
  justify-content:center;
  align-items:center;
  font-size:18px;
  font-weight:900;
  cursor:pointer;
  user-select:none;
  z-index:2;
}
.note{
  margin-top:19px;
  font-size:13px;
  opacity:.62;
}
</style>
</head>
<body>
<div class="box">
  <div class="badge">SECURE HUMAN ACCESS</div>
  <div class="title">🔒 TOC Secure Gate</div>
  <div class="sub">Human verification required.<br>Hold the button to unlock secure access.</div>
  <div class="wrap">
    <div class="progress" id="progress"></div>
    <div class="btn" id="holdBtn">HOLD TO UNLOCK</div>
  </div>
  <div class="note">Anti-scraper protection enabled.</div>
</div>
<script>
var progress = document.getElementById("progress");
var holdBtn = document.getElementById("holdBtn");
var percent = 0;
var timer = null;
var completed = false;
function startHold(){
  if(completed){return;}
  if(timer){return;}
  timer = setInterval(function(){
    percent += 2;
    progress.style.width = percent + "%";
    if(percent >= 100){
      clearInterval(timer);
      timer = null;
      completed = true;
      holdBtn.innerHTML = "ACCESS GRANTED";
      setTimeout(function(){
        window.location.href = "/unlock?t={{ token }}";
      }, 500);
    }
  }, 70);
}
function stopHold(){
  if(completed){return;}
  clearInterval(timer);
  timer = null;
  percent = 0;
  progress.style.width = "0%";
}
holdBtn.addEventListener("mousedown", startHold);
holdBtn.addEventListener("touchstart", startHold);
holdBtn.addEventListener("mouseup", stopHold);
holdBtn.addEventListener("mouseleave", stopHold);
holdBtn.addEventListener("touchend", stopHold);
</script>
</body>
</html>
"""

def decode_token(token):
    raw = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
    secret, url = raw.split("|", 1)
    if secret != SECRET:
        raise Exception("Invalid token")
    if not url.startswith("https://toc2.cloud/"):
        raise Exception("Invalid destination")
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
        return "Access denied: " + str(e), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
