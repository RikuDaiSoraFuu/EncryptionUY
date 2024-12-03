from flask import Flask, request, render_template, send_file
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ENCRYPTED_FOLDER = './encrypted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

# ホームページ（Web GUI）
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Encryption Service</title>
    </head>
    <body>
        <h2>File Encryption Service</h2>
        <form action="/encrypt" method="POST" enctype="multipart/form-data">
            <label for="key">Enter Secret Key:</label><br>
            <input type="text" name="key" id="key" required><br><br>
            <label for="file">Upload File:</label><br>
            <input type="file" name="file" id="file" required><br><br>
            <button type="submit">Encrypt File</button>
        </form>
    </body>
    </html>
    '''

# ファイル暗号化エンドポイント
@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    secret_key = request.form.get('key')
    file = request.files['file']

    if not secret_key or not file:
        return "Missing secret key or file.", 400

    # 暗号化準備
    fernet = Fernet(secret_key.encode())
    input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    encrypted_file_path = os.path.join(ENCRYPTED_FOLDER, file.filename + '.enc')

    # ファイル保存と暗号化
    file.save(input_file_path)
    with open(input_file_path, 'rb') as f:
        data = f.read()
    encrypted_data = fernet.encrypt(data)

    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)

    # 暗号化されたファイルをダウンロードとして提供
    return send_file(encrypted_file_path, as_attachment=True, download_name=file.filename + '.enc')

if __name__ == '__main__':
    app.run(debug=True)
