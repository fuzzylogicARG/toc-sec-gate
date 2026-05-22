from flask import Flask, request, redirect, render_template_string
import base64
import hashlib
import hmac
import os
import time

app = Flask(__name__)

GATE_SECRET = os.environ.get("GATE_SECRET", "TOC2026")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>TOC — New Era Access</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
}

body{
background:
radial-gradient(circle at top,#132547 0%,#090d18 45%,#05070d 100%);
font-family:Arial,Helvetica,sans-serif;
color:white;
overflow-x:hidden;
min-height:100vh;
}

.bg1{
position:fixed;
width:900px;
height:900px;
background:radial-gradient(circle,#00e5ff22 0%,transparent 70%);
top:-350px;
left:-250px;
pointer-events:none;
}

.bg2{
position:fixed;
width:700px;
height:700px;
background:radial-gradient(circle,#ff00aa18 0%,transparent 70%);
bottom:-250px;
right:-200px;
pointer-events:none;
}

.container{
position:relative;
z-index:5;
max-width:1250px;
margin:auto;
padding:60px 20px;
}

.hero{
text-align:center;
margin-bottom:45px;
}

.hero h1{
font-size:56px;
font-weight:900;
line-height:1;
margin-bottom:18px;
background:linear-gradient(90deg,#00e5ff,#7b61ff,#ff00aa);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
text-shadow:0 0 40px rgba(0,229,255,.3);
}

.hero p{
max-width:950px;
margin:auto;
font-size:18px;
line-height:1.6;
opacity:.9;
color:#d8d8d8;
}

.grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:28px;
margin-top:45px;
}

.card{
background:rgba(14,20,36,.82);
border:1px solid rgba(0,229,255,.16);
border-radius:24px;
padding:34px;
backdrop-filter:blur(12px);
box-shadow:
0 0 40px rgba(0,229,255,.08),
0 0 80px rgba(123,97,255,.06);
}

.card h2{
font-size:28px;
margin-bottom:20px;
font-weight:900;
}

.section-title{
font-size:13px;
letter-spacing:.2em;
text-transform:uppercase;
opacity:.6;
margin-bottom:18px;
}

.list{
display:flex;
flex-direction:column;
gap:14px;
margin-top:20px;
}

.item{
padding:14px 18px;
border-radius:14px;
background:rgba(255,255,255,.04);
border:1px solid rgba(255,255,255,.06);
font-weight:700;
}

.stats{
display:grid;
grid-template-columns:1fr 1fr;
gap:14px;
margin-top:25px;
}

.stat{
padding:20px;
border-radius:16px;
text-align:center;
background:linear-gradient(135deg,#00e5ff22,#7b61ff22);
border:1px solid rgba(255,255,255,.08);
}

.stat strong{
display:block;
font-size:26px;
margin-bottom:6px;
}

.notice{
margin-top:25px;
padding:18px;
border-radius:16px;
background:rgba(255,0,170,.08);
border:1px solid rgba(255,0,170,.22);
line-height:1.6;
}

.links{
display:grid;
grid-template-columns:1fr 1fr;
gap:14px;
margin-top:24px;
}

.linkbtn{
display:flex;
align-items:center;
justify-content:center;
text-decoration:none;
padding:16px;
border-radius:16px;
font-weight:900;
font-size:15px;
background:linear-gradient(90deg,#00e5ff,#7b61ff);
color:white;
transition:.25s;
}

.linkbtn:hover{
transform:translateY(-3px);
box-shadow:0 0 30px rgba(0,229,255,.3);
}

.unlock{
margin-top:45px;
text-align:center;
}

.unlock h3{
font-size:30px;
margin-bottom:18px;
}

.wrap{
width:360px;
height:72px;
background:#1f2937;
border-radius:18px;
overflow:hidden;
position:relative;
margin:22px auto 0;
border:1px solid rgba(255,255,255,.08);
}

.bar{
position:absolute;
left:0;
top:0;
height:100%;
width:0;
background:linear-gradient(90deg,#00e5ff,#7b61ff,#ff00aa);
}

.btn{
position:absolute;
inset:0;
display:flex;
align-items:center;
justify-content:center;
font-weight:900;
cursor:pointer;
user-select:none;
font-size:18px;
letter-spacing:.06em;
}

.footer{
margin-top:55px;
text-align:center;
font-size:13px;
opacity:.45;
}

@media(max-width:900px){

.hero h1{
font-size:42px;
}

.grid{
grid-template-columns:1fr;
}

.links{
grid-template-columns:1fr;
}

.wrap{
width:100%;
}

}

</style>
</head>

<body>

<div class="bg1"></div>
<div class="bg2"></div>

<div class="container">

<div class="hero">

<h1>WELCOME TO THE NEW ERA OF TOC</h1>

<p>
TOC is rebuilding into a stronger, safer, and highly automated platform focused on protecting content, improving stability, and expanding one of the largest candid libraries online.
</p>

</div>

<div class="grid">

<div class="card">

<div class="section-title">Content Network</div>

<h2>Massive Automated Library</h2>

<div class="list">
<div class="item">📸 Candid</div>
<div class="item">🎬 Staged</div>
<div class="item">🎥 Self Shot</div>
<div class="item">❤️ Amateur Couples</div>
</div>

<div class="stats">
<div class="stat">
<strong>40,000+</strong>
Titles
</div>

<div class="stat">
<strong>100+</strong>
Daily Uploads
</div>

<div class="stat">
<strong>24/7</strong>
Automation
</div>

<div class="stat">
<strong>VIP</strong>
Private Access
</div>
</div>

<div class="notice">
⚠️ Access is no longer free.<br><br>

All users must activate at least a $4.99 Access Plan to enter the ecosystem.
</div>

</div>

<div class="card">

<div class="section-title">Preview & Access</div>

<h2>Platform Expansion</h2>

<div class="list">
<div class="item">🔥 Telegram Preview</div>
<div class="item">🔥 Erome Preview #1</div>
<div class="item">🔥 Erome Preview #2</div>
<div class="item">🔥 TheCandidVerse.com</div>
</div>

<div class="links">

<a class="linkbtn" href="https://www.erome.com/Theoriginalcandid" target="_blank">
EROME #1
</a>

<a class="linkbtn" href="https://www.erome.com/Therealcandidverse" target="_blank">
EROME #2
</a>

<a class="linkbtn" href="https://thecandidverse.com" target="_blank">
THECANDIDVERSE
</a>

<a class="linkbtn" href="https://theoriginalcandid.com" target="_blank">
ENTER TOC
</a>

</div>

<div class="notice">
💳 Supported Payments:<br><br>

Cash App • BTC • XRP • ETH • USDC (Solana)
</div>

</div>

</div>

<div class="unlock">

<h3>Human Verification Required</h3>

<p>Hold to unlock secure access</p>

<div class="wrap">

<div class="bar" id="bar"></div>

<div class="btn" id="btn">
HOLD TO UNLOCK
</div>

</div>

</div>

<div class="footer">
TOC Secure Access • Automated Gateway • Legacy + HMAC
</div>

</div>

<script>

let btn=document.getElementById("btn");
let bar=document.getElementById("bar");

let p=0;
let t=null;

function start(){

 if(t) return;

 t=setInterval(function(){

  p+=2;

  bar.style.width=p+"%";

  if(p>=100){

   clearInterval(t);

   window.location.href="/unlock?t={{token}}";

  }

 },60);

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

def verify_hmac_token(token: str):
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

        payload = base64.urlsafe_b64decode(
            padded.encode("utf-8")
        ).decode("utf-8")

        expires_ts_str, real_url = payload.split("|", 1)

        expires_ts = int(expires_ts_str)

    except Exception:
        return None

    if time.time() > expires_ts:
        return None

    if not real_url.startswith("http"):
        return None

    return real_url

def verify_legacy_token(token: str):

    try:
        padded = token.strip() + "=" * (-len(token.strip()) % 4)

        raw = base64.urlsafe_b64decode(
            padded.encode()
        ).decode()

        secret, url = raw.split("|", 1)

    except Exception:
        return None

    if not hmac.compare_digest(secret, GATE_SECRET):
        return None

    if not url.startswith("http"):
        return None

    return url

def verify_any_token(token: str):

    return verify_hmac_token(token) or verify_legacy_token(token)

@app.route("/")
def home():
    return "TOC Secure Gate Online - Dual Mode (Legacy + HMAC)"

@app.route("/access")
def access():

    token = request.args.get("t", "")

    if not token:
        return "Missing token", 400

    if not verify_any_token(token):
        return "Access denied: invalid or expired token", 403

    return render_template_string(HTML, token=token)

@app.route("/unlock")
def unlock():

    token = request.args.get("t", "")

    if not token:
        return "Missing token", 400

    real_url = verify_any_token(token)

    if not real_url:
        return "Access denied: invalid or expired token", 403

    return redirect(real_url, code=302)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
