from flask import Flask, request, send_file
import base64
import os

app = Flask(__name__)

# 固定の秘密鍵（必要に応じて変更してください）
SECRET_KEY = "qzd8M1VrOvYb9NiPlNxaT_vZQlBcOxj8W-FpkYv5lwY="

def xor_encrypt(data: bytes, key: str) -> bytes:
    key = key * (len(data) // len(key) + 1)  # キーを繰り返してデータ長に合わせる
    return bytes([byte ^ ord(key_char) for byte, key_char in zip(data, key)])

@app.route('/')
def home():
    return """
    <h1>File Encryption Service</h1>
    <form action="/encrypt" method="post" enctype="multipart/form-data">
        <label for="file">Upload a file:</label>
        <input type="file" name="file" id="file">
        <button type="submit">Encrypt</button>
    </form>
    """

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return "No file uploaded.", 400
    
    file = request.files['file']
    file_data = file.read()
    encrypted_data = xor_encrypt(file_data, SECRET_KEY)
    encrypted_b64 = base64.b64encode(encrypted_data)  # Base64エンコード

    # 暗号化ファイルを保存
    encrypted_file_path = "encrypted_file.txt"
    with open(encrypted_file_path, "wb") as f:
        f.write(encrypted_b64)

    return send_file(
        encrypted_file_path,
        as_attachment=True,
        download_name="encrypted_file.txt",
        mimetype="text/plain"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

# from flask import Flask, request, render_template, send_file
# from cryptography.fernet import Fernet
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = './uploads'
# ENCRYPTED_FOLDER = './encrypted'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

# # ホームページ（Web GUI）
# @app.route('/')
# def index():
#     return '''
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Encryption Service</title>
#     </head>
#     <body>
#         <h2>File Encryption Service</h2>
#         <form action="/encrypt" method="POST" enctype="multipart/form-data">
#             <label for="key">Enter Secret Key:</label><br>
#             <input type="text" name="key" id="key" required><br><br>
#             <label for="file">Upload File:</label><br>
#             <input type="file" name="file" id="file" required><br><br>
#             <button type="submit">Encrypt File</button>
#         </form>
#     </body>
#     </html>
#     '''

# # ファイル暗号化エンドポイント
# @app.route('/encrypt', methods=['POST'])
# def encrypt_file():
#     secret_key = request.form.get('key')
#     file = request.files['file']

#     if not secret_key or not file:
#         return "Missing secret key or file.", 400

#     # 暗号化準備
#     fernet = Fernet(secret_key.encode())
#     input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     encrypted_file_path = os.path.join(ENCRYPTED_FOLDER, file.filename + '.enc')

#     # ファイル保存と暗号化
#     file.save(input_file_path)
#     with open(input_file_path, 'rb') as f:
#         data = f.read()
#     encrypted_data = fernet.encrypt(data)

#     with open(encrypted_file_path, 'wb') as f:
#         f.write(encrypted_data)

#     # 暗号化されたファイルをダウンロードとして提供
#     return send_file(encrypted_file_path, as_attachment=True, download_name=file.filename + '.enc')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
