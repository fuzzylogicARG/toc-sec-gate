from flask import Flask, request, redirect, render_template_string
import base64
import os
import time

app = Flask(__name__)

SECRET = os.getenv("GATE_SECRET", "TOC_ULTRA_SECRET_2026")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TOC Secure Access</title>

<style>
body{
    background:#0b0f19;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}

.box{
    width:420px;
    background:#121826;
    border:1px solid rgba(0,255,255,.25);
    border-radius:18px;
    padding:30px;
    text-align:center;
    box-shadow:0 0 40px rgba(0,255,255,.15);
}

.title{
    font-size:28px;
    font-weight:bold;
    margin-bottom:10px;
}

.sub{
    opacity:.7;
    margin-bottom:25px;
}

.holdWrap{
    width:100%;
    height:60px;
    background:#1b2436;
    border-radius:14px;
    overflow:hidden;
    position:relative;
    border:1px solid rgba(255,255,255,.08);
}

.progress{
    position:absolute;
    top:0;
    left:0;
    height:100%;
    width:0%;
    background:linear-gradient(90deg,#00e5ff,#7a5cff,#ff00c8);
    transition:width .08s linear;
}

.holdBtn{
    position:absolute;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:center;
    z-index:2;
    font-size:18px;
    font-weight:bold;
    cursor:pointer;
    user-select:none;
}

.note{
    margin-top:18px;
    opacity:.6;
    font-size:13px;
}
</style>

</head>
<body>

<div class="box">

    <div class="title">
        🔒 TOC Secure Access
    </div>

    <div class="sub">
        Human verification required
    </div>

    <div class="holdWrap">

        <div class="progress" id="progress"></div>

        <div class="holdBtn" id="holdBtn">
            HOLD TO UNLOCK
        </div>

    </div>

    <div class="note">
        Anti scraper protection enabled
    </div>

</div>

<script>

const holdBtn = document.getElementById("holdBtn");
const progress = document.getElementById("progress");

let percent = 0;
let timer = null;

function startHold(){

    timer = setInterval(() => {

        percent += 2;

        progress.style.width = percent + "%";

        if(percent >= 100){

            clearInterval(timer);

            window.location.href = "/unlock?t={{ token }}";
        }

    }, 80);
}

function stopHold(){

    clearInterval(timer);

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

def encode_url(url):

    data = f"{SECRET}|{url}|{int(time.time())}"

    return base64.urlsafe_b64encode(data.encode()).decode()

def decode_token(token):

    raw = base64.urlsafe_b64decode(token.encode()).decode()

    secret, url, created = raw.split("|", 2)

    if secret != SECRET:
        raise Exception("Invalid token")

    return url

@app.route("/")
def home():

    return "TOC Secure Gate Online"

@app.route("/gate")
def gate():

    url = request.args.get("url")

    if not url:
        return "Missing URL"

    token = encode_url(url)

    return render_template_string(
        HTML_PAGE,
        token=token
    )

@app.route("/unlock")
def unlock():

    token = request.args.get("t")

    if not token:
        return "Missing token"

    try:

        url = decode_token(token)

        return redirect(url)

    except Exception as e:

        return f"Invalid request: {e}"

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
