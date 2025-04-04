from flask import Flask, render_template, request, redirect, url_for 
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    description TEXT,
                    amount REAL,
                    category TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route('/')
def index():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = c.fetchall()
    total = sum([t[3] for t in transactions])
    conn.close()
    return render_template('index.html', transactions=transactions, total=total)

@app.route('/add', methods=['POST'])
def add_transaction():
    date = request.form['date']
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']

    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (date, description, amount, category) VALUES (?, ?, ?, ?)",
              (date, description, amount, category))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
