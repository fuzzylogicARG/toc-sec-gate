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

<title>TOC Secure Access</title>

<style>

body{
background:#0b1020;
color:white;
font-family:Arial;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
margin:0;
overflow:hidden;
}

.box{
width:420px;
background:#12192b;
border-radius:18px;
padding:30px;
text-align:center;
border:1px solid rgba(0,255,255,.2);
box-shadow:0 0 40px rgba(0,255,255,.15);
}

.title{
font-size:30px;
font-weight:bold;
margin-bottom:10px;
}

.sub{
opacity:.7;
margin-bottom:25px;
}

.wrap{
width:100%;
height:64px;
background:#1a2238;
border-radius:14px;
overflow:hidden;
position:relative;
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
font-weight:bold;
cursor:pointer;
user-select:none;
z-index:2;
}

.note{
margin-top:18px;
font-size:13px;
opacity:.6;
}

</style>
</head>

<body>

<div class="box">

<div class="title">
🔒 TOC Secure Gate
</div>

<div class="sub">
Human verification required
</div>

<div class="wrap">

<div class="progress" id="progress"></div>

<div class="btn" id="holdBtn">
HOLD TO UNLOCK
</div>

</div>

<div class="note">
Anti scraper protection enabled
</div>

</div>

<script>

let progress = document.getElementById("progress");
let holdBtn = document.getElementById("holdBtn");

let percent = 0;
let timer;

function startHold(){

timer = setInterval(function(){

percent += 2;

progress.style.width = percent + "%";

if(percent >= 100){

clearInterval(timer);

window.location.href="/unlock?t={{token}}";

}

},70);

}

function stopHold(){

clearInterval(timer);

percent = 0;

progress.style.width="0%";

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

def encode(url):

    raw = SECRET + "|" + url

    return base64.urlsafe_b64encode(raw.encode()).decode()

def decode(token):

    raw = base64.urlsafe_b64decode(token.encode()).decode()

    return raw.split("|",1)[1]

@app.route("/")
def home():

    return "TOC Secure Gate Online"

@app.route("/gate")
def gate():

    url = request.args.get("url")

    if not url:
        return "Missing URL"

    token = encode(url)

    return render_template_string(
        HTML,
        token=token
    )

@app.route("/unlock")
def unlock():

    token = request.args.get("t")

    if not token:
        return "Missing token"

    url = decode(token)

    return redirect(url)

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
