from flask import Flask, request, redirect, url_for, session, render_template
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
app.secret_key = 'hzgp549212h56'
CORS(app, supports_credentials=True)  # Add this line to enable CORS

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Jaisonjoseph007"
    )
    return conn

@app.route('/')
def index():
    if 'username' in session:
        if session['website_version'] == 'visual':
            return redirect('http://127.0.0.1:5001')
        else:
            return "Cognitively oriented homepage not implemented."
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['username'] = username
            session['website_version'] = user[4]  # Assuming website_version is the 5th column

            if session['website_version'] == 'visual':
                return redirect('http://127.0.0.1:5001')
            else:
                return "Cognitively oriented homepage not implemented."
        else:
            return "Invalid username or password"
    return render_template('login_page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['newUsername']
        new_email = request.form['newEmail']
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']
        website_version = request.form['websiteVersion']

        if new_password == confirm_password:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password, website_version) VALUES (%s, %s, %s, %s)", 
                        (new_username, new_email, new_password, website_version))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('login'))
        else:
            return "Passwords do not match"
    return render_template('sign_in_page.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('website_version', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
