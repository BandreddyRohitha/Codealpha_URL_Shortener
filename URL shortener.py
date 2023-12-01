from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)
conn = sqlite3.connect('urls.db')
c = conn.cursor()

# Create table to store URLs
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY AUTOINCREMENT, original_url TEXT, short_code TEXT)''')
conn.commit()

def generate_short_code():
    # Changed string.ascii_letters + string.digits to string.digits to generate unique short codes with only digits
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_code = generate_short_code()

    c.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, short_code))
    conn.commit()

    # Updated the short URL format to include the current host domain dynamically
    return render_template('shortened.html', short_url=f"http://{request.host}/{short_code}")

@app.route('/<short_code>')
def redirect_to_url(short_code):
    c.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,))
    row = c.fetchone()
    if row:
        original_url = row[0]
        return redirect(original_url)
    return "URL not found"

if __name__ == '__main__':
    app.run(debug=True)
