from flask import Flask, session, request, jsonify
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# 各種画像の保存先フォルダを定義
UPLOAD_FOLDER_ICONS = 'uploads/icons'
UPLOAD_FOLDER_POSTS = 'uploads/posts'

# フォルダが存在しない場合、作成する
for folder in [UPLOAD_FOLDER_ICONS, UPLOAD_FOLDER_POSTS]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key") 
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)  

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="D3tvn426",
        database="myapp_db"
    )

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')

@app.route('/')
def home():
    return "MyApp へようこそ！適切なエンドポイントを使用してください。"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    any_user_id = data.get("any_user_id")
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")
    email_opt_in = data.get("email_opt_in")
    birth_date = data.get("birth_date")
    created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') 

    hashed_password = hash_password(password)

    connection = connect_db()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (user_name, any_user_id, email, password, email_opt_in, birth_date, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_name, any_user_id, email, hashed_password, email_opt_in, birth_date, created_at))

        connection.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return jsonify({"message": "Registration failed", "error": str(err)}), 500
    
    finally:
        cursor.close()
        connection.close()

@app.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")

    connection = connect_db()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user_record = cursor.fetchone()
        # デバッグ用
        print(f"Database returned: {user_record}")
        
    finally:
        cursor.close()
        connection.close()

    if user_record and check_password_hash(user_record[4], password): 
        any_user_id = user_record[1] 
        session["any_user_id"] = any_user_id  # セッションに保存するキーを変更
        return jsonify({"message": "ログインに成功しました！", "any_user_id": any_user_id}), 200  
    else:
        return jsonify({"message": "認証情報が無効です"}), 401

@app.route("/timeline", methods=["GET"])
def get_timeline():
    # データベースに接続
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    try:
        # 投稿を取得するクエリ
        cursor.execute("""
            SELECT 
                posts.post_id, 
                users.any_user_id AS any_user_id,
                posts.content, 
                posts.created_at, 
                posts.updated_at, 
                posts.likes_count, 
                posts.repost_count, 
                posts.replies_count, 
                posts.parent_post_id, 
                posts.media_url, 
                users.user_name
            FROM posts
            JOIN users ON posts.user_id = users.user_id 
            WHERE posts.is_deleted = 0
            ORDER BY posts.created_at DESC 
        """)

        # 結果を取得
        posts = cursor.fetchall()

        # 取得したデータをJSONで返す
        return jsonify(posts), 200
    except mysql.connector.Error as err:
        print("問題が発生しました: {}".format(err))
        return jsonify({"message": "投稿の取得に失敗しました", "error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/user/<any_user_id>/posts', methods=['GET'])
def get_user_posts(any_user_id):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    try:
        # any_user_id に対応する user_id を取得する
        user_query = "SELECT user_id FROM users WHERE any_user_id = %s"
        cursor.execute(user_query, (any_user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "ユーザーが見つかりません"}), 404

        user_id = user['user_id']

        # その user_id を使用してユーザーの投稿を取得する
        posts_query = """
            SELECT 
                posts.post_id, 
                posts.content, 
                posts.created_at, 
                posts.updated_at, 
                posts.likes_count, 
                posts.repost_count, 
                posts.replies_count, 
                posts.parent_post_id, 
                posts.media_url,
                users.user_name,
                users.any_user_id
            FROM posts
            JOIN users ON posts.user_id = users.user_id
            WHERE posts.user_id = %s AND posts.is_deleted = 0
            ORDER BY posts.created_at DESC
        """
        cursor.execute(posts_query, (user_id,))
        posts = cursor.fetchall()

        return jsonify(posts), 200
    except mysql.connector.Error as err:
        print("問題が発生しました: {}".format(err))
        return jsonify({"message": "投稿の取得に失敗しました", "error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()
        
@app.route("/post", methods=["POST"])
def create_post():
    data = request.get_json()
    
    any_user_id = data.get("any_user_id")
    content = data.get("content")
    parent_post_id = data.get("parent_post_id")
    media_url = data.get("media_url")

    if not any_user_id or not content:
        return jsonify({"message": "ユーザーIDとコンテンツが必要です"}), 400
    
    connection = connect_db()
    cursor = connection.cursor()

    try:
        # user_idを取得するためのクエリを追加
        cursor.execute("SELECT user_id FROM users WHERE any_user_id = %s", (any_user_id,))
        user_record = cursor.fetchone()
        
        if not user_record:
            return jsonify({"message": "無効なユーザーID"}), 400
        
        user_id = user_record[0]

        # SQLクエリの構築
        query = """
            INSERT INTO posts (user_id, content, parent_post_id, media_url)
            VALUES (%s, %s, %s, %s)
        """

        # 値をタプルとして準備
        values = (user_id, content, parent_post_id, media_url) 
        
        # 実行
        cursor.execute(query, values)
        connection.commit()

        return jsonify({"message": "投稿が正常に作成されました"}), 201
    except mysql.connector.Error as err:
        print("問題が発生しました: {}".format(err))
        return jsonify({"message": "投稿の作成に失敗しました", "error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()
@app.route('/user/<any_user_id>', methods=['GET']) 
def get_user_profile(any_user_id): 
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = "SELECT any_user_id, user_name, icon_path, bio, created_at FROM users WHERE any_user_id = %s"  
        cursor.execute(query, (any_user_id,))  
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "ユーザーが見つかりませんでした"}), 404
        
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return jsonify({"message": "ユーザーデータの取得中にエラーが発生しました"}), 500
    
    finally:
        cursor.close()
        connection.close()
        
@app.route('/upload_icon/<any_user_id>', methods=['POST'])
def upload_icon(any_user_id):
    if 'file' not in request.files:
        return jsonify({"message": "ファイルが存在しません"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "選択されたファイルがありません"}), 400

    if file:
        # 保存するディレクトリを作成
        if not os.path.exists(UPLOAD_FOLDER_ICONS):
            os.makedirs(UPLOAD_FOLDER_ICONS)

        # ファイル名をuser_id + "_icon"に設定
        file_ext = os.path.splitext(file.filename)[1]
        new_file_name = f"{any_user_id}_icon{file_ext}"
        save_path = os.path.join(UPLOAD_FOLDER_ICONS, new_file_name)

        # ファイルを保存
        file.save(save_path)
        return jsonify({"message": "ファイルのアップロードに成功しました", "save_path": save_path}), 200

    
@app.route('/update_user/<any_user_id>', methods=['POST'])  
def update_user_profile(any_user_id): 

    data = request.json  # JSONデータを取得
    
    # JSONからデータを取得
    user_name = data.get("user_name")
    bio = data.get("bio")
    icon_path = data.get("icon_path") 

    # 提供されていないデータをデータベースから取得
    if not user_name or not bio or not icon_path:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT user_name, bio, icon_path FROM users WHERE any_user_id = %s", (any_user_id,))
            user_record = cursor.fetchone()
            if user_record:
                user_name = user_name or user_record['user_name']
                bio = bio or user_record['bio']
                icon_path = icon_path or user_record['icon_path']
            else:
                return jsonify({"message": "ユーザーが見つかりません"}), 404
        finally:
            cursor.close()
            connection.close()

    # データベースに接続してユーザ情報を更新
    connection = connect_db()
    cursor = connection.cursor()
    
    try:
        update_query = """
            UPDATE users 
            SET user_name = %s, bio = %s, icon_path = %s  # icon_pathも更新
            WHERE any_user_id = %s 
        """
        cursor.execute(update_query, (user_name, bio, icon_path, any_user_id))
        connection.commit()

        return jsonify({"message": "ユーザーが正常に更新されました"}), 200
    except mysql.connector.Error as err:
        print(f"ユーザー情報の更新に失敗: {err}")
        return jsonify({"message": "ユーザーデータの更新中にエラーが発生しました", "error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
