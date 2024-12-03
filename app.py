from flask import Flask, request, send_file, jsonify
from cryptography.fernet import Fernet
import io

app = Flask(__name__)

# 固定された暗号化キー（教師ごとに個別の鍵を利用する場合、管理を別途考慮する必要があります）
key = Fernet.generate_key()  # 必要に応じて固定の鍵を使用してください
cipher = Fernet(key)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Encryption Service!",
        "instruction": "POST a file to /encrypt to get it encrypted.",
        "key": key.decode()  # 教師が鍵を知る必要がある場合のみ表示
    })

@app.route("/encrypt", methods=["POST"])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    data = file.read()

    # ファイルを暗号化
    encrypted_data = cipher.encrypt(data)
    encrypted_file = io.BytesIO(encrypted_data)
    encrypted_file.name = "encrypted_file.enc"

    return send_file(encrypted_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
