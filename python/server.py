from flask import Flask
from flask import request
from flask import jsonify
from Crypto.Cipher import AES
import random
import string
import base64
import json
import requests

app = Flask(__name__)

BLOCK_SIZE = 16
PADDING = '*'
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
# generating initialization vector needed for CBC mode
iv = lambda length: ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(length))
# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
encryption_key = "1234567890123456"
vector = iv(BLOCK_SIZE)
cipher = AES.new(encryption_key, AES.MODE_CBC, vector)

# Download and run https://github.com/marinho/notification-center
NOTIFICATION_ENABLED = True
NOTIFICATION_CENTER_SECURITY_TOKEN = "VeraLeniLeticia"
NOTIFICATION_CENTER_URL = "http://localhost:5030/notification"
NOTIFICATION_CHANNEL = "fromTDispatch"


@app.route("/calculate-price", methods=['POST'])
def price_service():
    decrypted = DecodeAES(cipher, request.form["payload"])[16:]
    json_payload = json.loads(decrypted)
    new_price = json_payload["calculatedPrice"]
    new_price["fareNarrative"].append({
        "snippet": "custom",
        "description": "Extra fee",
        "value": 5,
        "subtotal": new_price["fareNarrative"][-1]["subtotal"] + 5,
        })
    new_price["cost"] += 5

    if NOTIFICATION_ENABLED:
        send_notification(new_price)

    return jsonify(new_price)

    
@app.route("/test-webhook", methods=['POST'])
def test_webhook():
    decrypted = DecodeAES(cipher, request.form["payload"])[16:]
    json_payload = json.loads(decrypted)

    if NOTIFICATION_ENABLED:
        send_notification(json_payload)

    return jsonify(json_payload)


def send_notification(body):
    data = {}
    data.update(body)
    data["channel"] = NOTIFICATION_CHANNEL
    data["securityToken"] = NOTIFICATION_CENTER_SECURITY_TOKEN

    requests.post(NOTIFICATION_CENTER_URL,
                  data=json.dumps(data),
                  headers={"Content-Type": "application/json"})


if __name__ == "__main__":
    app.run(port=5040, debug=True)
