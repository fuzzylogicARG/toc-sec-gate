from flask import Flask, request, redirect, render_template_string
                window.location.href = "/unlock?t={{ token }}";
            },700);
        }
    },80);
}

function stopHold(){
    if(completed) return;

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


@app.route("/access")
def access_gate():
    token = request.args.get("t", "")

    if not token:
        return "Missing token", 400

    return render_template_string(HTML_PAGE, token=token)


@app.route("/unlock")
def unlock():
    token = request.args.get("t", "")

    try:
        url = decode_token(token)
        return redirect(url)

    except Exception as e:
        return f"Access denied: {str(e)}", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)