from flask import Flask,session, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = "D3tvn426"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)  # 例: セッションの有効期限を60分に設定


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
    return "Welcome to MyApp! Please use the appropriate endpoints."

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user_id = data.get("user_id")
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")
    email_opt_in = data.get("email_opt_in")
    birth_date = data.get("birth_date")
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    hashed_password = hash_password(password)

    connection = connect_db()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (user_name, user_id, email, password, email_opt_in, birth_date, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_name, user_id, email, hashed_password, email_opt_in, birth_date, created_at))
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
        # デバック用
        print(f"Database returned: {user_record}")
        
    finally:
        cursor.close()
        connection.close()

    if user_record and check_password_hash(user_record[4], password): # type: ignore
        user_id = user_record[0] # type: ignore
        session["user_id"] = user_id
        return jsonify({"message": "Login successful!","user_id": user_id}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


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
                users.user_id AS user_id, 
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
            JOIN users ON posts.user_id = users.id
            WHERE posts.is_deleted = 0
            ORDER BY posts.created_at DESC 
        """)

        # 結果を取得
        posts = cursor.fetchall()
        print("Fetched posts: ", posts)  # デバッグ用に取得した投稿を表示

        # 取得したデータをJSONで返す
        return jsonify(posts), 200
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return jsonify({"message": "Failed to fetch posts", "error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()



@app.route("/post", methods=["POST"])
def create_post():
    data = request.get_json()
    
    user_id = data.get("user_id")
    content = data.get("content")
    parent_post_id = data.get("parent_post_id")
    media_url = data.get("media_url")

    if not user_id or not content:
        return jsonify({"message": "User ID and content are required"}), 400
    
    connection = connect_db()
    cursor = connection.cursor()

    try:
        # SQLクエリの構築
        query = """
            INSERT INTO posts (user_id,content,parent_post_id,media_url)
            VALUES (%s,%s,%s,%s)
        """

        # 値をタプルとして準備
        values = (user_id, content, parent_post_id, media_url)
        
        # 実行
        cursor.execute(query,values)
        connection.commit()

        return jsonify({"message": "Post created successfully!"}),201
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return jsonify({"message": "Post creation failed", "error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/user/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = "SELECT user_id, user_name, icon_url, bio, created_at FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return jsonify({"message": "Error fetching user data"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")