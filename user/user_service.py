# user_service.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # セッションのための秘密キー
CORS(app)

# インメモリデータベース（ユーザー用）
# {88: {id:88,username:mickey,password:pass}, 55: {id:55,...}
users_db = {}

@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    user_id = data.get('id')
    username = data.get('username')
    password = data.get('password')

    if not user_id or not username or not password:
        return jsonify({'error': 'ユーザーID、ユーザー名、またはパスワードが不足しています'}), 400

    if user_id in users_db:
        return jsonify({'error': 'ユーザーは既に存在します'}), 400

    hashed_password = generate_password_hash(password)  # パスワードのハッシュ化
    users_db[user_id] = {'id': user_id, 'username': username, 'password': hashed_password}
    return jsonify({'message': 'ユーザー登録が成功しました'}), 201


@app.route('/login', methods=['POST'])
def login_user():
    # data { id: 88, password: pass }
    data = request.json
    user_id = data.get('id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({'error': 'ユーザーIDまたはパスワードが不足しています'}), 400

    user = users_db.get(user_id)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': '無効なユーザーIDまたはパスワードです'}), 401

    # セッション(session: Flaskの辞書のようなオブジェクト)にユーザーを追加
    session['user_id'] = user_id

    # ログイン成功時にユーザー情報を返す(data変数に格納するやつ)
    return jsonify({'message': 'ログイン成功', 'user': {'id': user['id'], 'username': user['username']}}), 200


# すべてのユーザーを取得するためのエンドポイント
@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(list(users_db.values())), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
