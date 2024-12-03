import os
from flask import Flask, request, send_file, jsonify
from cryptography.fernet import Fernet
import io

app = Flask(__name__)

key = Fernet.generate_key()
cipher = Fernet(key)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Encryption Service!",
        "instruction": "POST a file to /encrypt to get it encrypted.",
        "key": key.decode()
    })

@app.route("/encrypt", methods=["POST"])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    data = file.read()

    encrypted_data = cipher.encrypt(data)
    encrypted_file = io.BytesIO(encrypted_data)
    encrypted_file.name = "encrypted_file.enc"

    return send_file(encrypted_file, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
