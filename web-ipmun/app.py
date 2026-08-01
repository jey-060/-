from flask import Flask, render_template, request, redirect, url_for, session, flash
import urllib.parse
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATABASE = 'app_data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trait_text TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

if not os.path.exists(DATABASE):
    init_db()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT traits.id, traits.trait_text, users.username FROM traits LEFT JOIN users ON traits.user_id = users.id')
    traits_list = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', traits_list=traits_list)

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('회원가입이 완료되었습니다! 로그인해주세요.')
            conn.close()
            return redirect(url_for('login_page'))
        except sqlite3.IntegrityError:
            flash('이미 존재하는 아이디입니다.')
            conn.close()
            return redirect(url_for('register_page'))

    return redirect(url_for('register_page'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('index'))
    else:
        flash('아이디 또는 비밀번호가 올바르지 않습니다.')
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_wikipedia():
    if not session.get('user_id'):
        flash('로그인이 필요한 기능입니다.')
        return redirect(url_for('login_page'))

    animal_name = request.args.get('animal')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT traits.id, traits.trait_text, users.username FROM traits LEFT JOIN users ON traits.user_id = users.id')
    traits_list = cursor.fetchall()
    conn.close()

    if animal_name:
        base_url = "https://ko.wikipedia.org/wiki/"
        encoded_name = urllib.parse.quote(animal_name)
        wikipedia_url = base_url + encoded_name
        return render_template('index.html', wikipedia_url=wikipedia_url, animal_name=animal_name, traits_list=traits_list)
    
    return render_template('index.html', traits_list=traits_list)

@app.route('/add_trait', methods=['POST'])
def add_trait():
    user_id = session.get('user_id')
    if not user_id:
        flash('로그인이 필요한 기능입니다.')
        return redirect(url_for('login_page'))

    new_trait = request.form.get('trait')

    if new_trait:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO traits (trait_text, user_id) VALUES (?, ?)', (new_trait, user_id))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

@app.route('/edit_trait/<int:trait_id>', methods=['POST'])
def edit_trait(trait_id):
    updated_text = request.form.get('updated_trait')
    user_id = session.get('user_id')

    if updated_text and user_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE traits SET trait_text = ? WHERE id = ? AND user_id = ?', (updated_text, trait_id, user_id))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

@app.route('/delete_trait/<int:trait_id>', methods=['POST'])
def delete_trait(trait_id):
    user_id = session.get('user_id')

    if user_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM traits WHERE id = ? AND user_id = ?', (trait_id, user_id))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)