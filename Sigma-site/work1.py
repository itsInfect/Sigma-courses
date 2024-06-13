from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3

app = Flask(__name__)  
app.secret_key = '9f5e4b7e1b4a6c8f0e1d2c3b4a5e6f7d'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/roadtosigma')
def roadtosigma():
    return render_template('roadtosigma.html')

@app.route('/final')
def final():
    return render_template('final.html')

@app.route("/profile/<username>")
def profile(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return render_template('prof.html', username=username, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('profile', username=username))
        else:
            return redirect(url_for('register'))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        if password == repeat_password:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                conn.close()
                return 'Пользователь с таким именем уже существует'
        else:
            return 'Пароли не совпадают'
    else:
        return render_template('register.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if request.method == 'POST':
        email = request.form['email']
        bio = request.form['bio']
        conn.execute('UPDATE users SET email = ?, bio = ? WHERE username = ?', (email, bio, username))
        conn.commit() 
        conn.close()
        return redirect(url_for('profile', username=username))

    conn.close()
    return render_template('editprofile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()