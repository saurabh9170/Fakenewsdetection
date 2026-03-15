from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle, re, nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import mysql.connector
import bcrypt

nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load model
model, vectorizer = pickle.load(open("fake_news_model.pkl", "rb"))

# Preprocessing
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = [stemmer.stem(word) for word in text.split() if word not in stop_words]
    return " ".join(words)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="fake_news_db"
)
cursor = conn.cursor(dictionary=True)

# ----------------- DEFAULT ROUTE -----------------
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('register_page'))

# ----------------- REGISTER -----------------
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    popup_message = None
    show_buttons = False

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['repeat_password']

        if password != repeat_password:
            popup_message = "Passwords do not match!"
            show_buttons = True
            return render_template('register.html', popup_message=popup_message, show_buttons=show_buttons)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            popup_message = "Email already registered!"
            show_buttons = True
            return render_template('register.html', popup_message=popup_message, show_buttons=show_buttons)

        # New user → insert
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login_page'))

    return render_template('register.html', popup_message=popup_message, show_buttons=show_buttons)

# ----------------- LOGIN -----------------
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                error = "Incorrect password."
        else:
            flash("Email not registered. Please register first.", "danger")
            return redirect(url_for('register_page'))

    return render_template('login.html', error=error)

# ----------------- DASHBOARD -----------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    prediction_text = None
    confidence = None

    if request.method == 'POST':
        news = request.form['news']
        clean_news = preprocess_text(news)
        vect = vectorizer.transform([clean_news])

        prediction = model.predict(vect)[0]
        probability = model.predict_proba(vect)[0]

        if prediction == 1:
            prediction_text = "Real News ✅"
            confidence = round(probability[1] * 100, 2)
        else:
            prediction_text = "Fake News ❌"
            confidence = round(probability[0] * 100, 2)

        cursor.execute(
            "INSERT INTO predictions (user_id, news_text, prediction, probability) VALUES (%s, %s, %s, %s)",
            (session['user_id'], news, prediction_text, confidence)
        )
        conn.commit()

    return render_template(
        "index.html",
        prediction_text=prediction_text,
        confidence=confidence
    )

# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('register_page'))

# ----------------- RUN -----------------
if __name__ == "__main__":
    app.run(debug=True)