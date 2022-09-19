import json

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, analyse_text, distribute_words

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///text_analysis.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    global results, word_distribution, words_sorted, text
    if request.method == "POST":
        # Get text to be analyzed
        text = request.form.get('text')
        # Check "Ignore "zero-length words" option
        w1 = request.form.get('w1')
        if not w1:
            w1=''
        # Check "Split compound words" option
        w2 = request.form.get('w2')
        if not w2:
            w2 = ''
        # Check syllables counting option
        sy_option = request.form.get('sy_option')
        # Check sentences counting option
        s_option = request.form.get('s_option')
        # Check number processing option
        n_option = request.form.get('n_option')
        # Analyse text
        results = analyse_text(text, w1, w2, sy_option, s_option, n_option)
        word_distribution = distribute_words(results[2])
        return render_template("index.html", results = results, word_distribution = word_distribution, text = text)
    else:
        return render_template("index.html", text_length = 0)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensure username exists and password is correct
        if len(rows) !=1:
            username_error = "Invalid username!"
            return render_template("login.html", username_error = username_error)
        elif not check_password_hash(rows[0]["hash"], password):
            password_error = "Invalid password!"
            return render_template("login.html", password_error = password_error)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        session["username"] = rows[0]["username"]


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        user = db.execute("SELECT username FROM users WHERE username = ?", username)
        # Ensure unique username
        if user:
            username_error = "User with such username already exists!"
        else:
            username_error = ""
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure password was confirmed
        if confirmation != password:
            confirmation_error = "Passwords do not match!"
        else:
            confirmation_error = ""
        # Show input errors
        if username_error or confirmation_error:
            return render_template("register.html", username_error = username_error, confirmation_error = confirmation_error)
        else:
            # Calculate password hash
            hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            # Record user data into database
            db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, hash)
            # Redirect user to home page
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/save", methods=["POST"])
@login_required
def save():
    """Save text analysis results"""
    # Get text name
    textname = request.form.get('textname')
    # Ensure the text name is unique for the user
    text_name = db.execute("SELECT textname FROM texts WHERE user_id = ? AND textname = ?", session["user_id"], textname)
    if text_name:
        textname_error = 'Such text name already exists!'
        return render_template("index.html", results = results, word_distribution = word_distribution, text = text, textname_error = textname_error)
    # Save text analysis results into database
    db.execute("INSERT INTO texts (user_id, textname) VALUES(?, ?)", session["user_id"], textname)
    text_id = db.execute("SELECT text_id FROM texts WHERE textname = ? AND user_id = ?", textname, session["user_id"])[0]["text_id"]
    db.execute("INSERT INTO statistics (text_id, Words, 'Words adjusted', Syllables, Sentences, Characters, 'Characters without spaces', Letters, Digits, 'Letters per word', 'Syllables per word', 'Words per sentence', 'Analysis options') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", text_id, results[0][0][1], results[0][1][1], results[0][2][1], results[0][3][1], results[0][4][1], results[0][5][1], results[0][6][1], results[0][7][1], results[0][8][1], results[0][9][1], results[0][10][1], results[0][11][1])
    db.execute("INSERT INTO readability (text_id, Summary, 'Reading time', rt_inter, 'Speaking time', st_inter, 'Different words', dw_inter, 'Long words', lw_inter, 'Complex words', cw_inter, 'Gunning Fog Index', gfi_inter, 'Coleman Liau Grade', clg_inter, 'Flesch Kincaid Grade Level', fkgl_inter, 'Flesch Reading Ease', fre_inter, 'Automated Readability Index', ari_inter, 'SMOG Grade', smog_inter, 'LIX (Laesbarhedsindex)', lix_inter) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", text_id, results[3], results[1][0][1][0], results[1][0][1][1], results[1][1][1][0], results[1][1][1][1], results[1][2][1][0], results[1][2][1][1], results[1][3][1][0], results[1][3][1][1], results[1][4][1][0], results[1][4][1][1], results[1][5][1][0], results[1][5][1][1], results[1][6][1][0], results[1][6][1][1], results[1][7][1][0], results[1][7][1][1], results[1][8][1][0], results[1][8][1][1], results[1][9][1][0], results[1][9][1][1], results[1][10][1][0], results[1][10][1][1], results[1][11][1][0], results[1][11][1][1])
    db.execute("INSERT INTO words (text_id, words) VALUES(?, ?)", text_id, json.dumps(results[2]))
    return redirect("/texts")


@app.route("/texts")
@login_required
def texts():
    """Show saved texts"""
    saved = db.execute("SELECT * FROM texts WHERE user_id = ? ORDER BY recorded_on DESC", session["user_id"])
    return render_template("texts.html", saved = saved)


@app.route("/show_words", methods=["POST"])
def show_words():
    """Show sorted words from text analysis results"""
    global results, word_distribution, words_sorted
    # Get number of words to be shown
    wnum = request.form.get("wnum")
    if wnum == "num":
        num = request.form.get("num")
        if num:
            num = int(num)
        else:
            num = 1
    else:
        num = len(results[2])
    # Get sort criterion
    sort_by = request.form.get("sort_by")
    if sort_by == "occurrence":
        i = 0
    elif sort_by == "length":
        i = 1
    else:
        i = 2
    # Get sort order
    sort_order = request.form.get("sort_order")
    # Get sorted word list
    if sort_order == "ascending":
        if sort_by == "alphabet":
            words_sorted = sorted(results[2], key = lambda j: j[0])[0:num]
        else:
            words_sorted = sorted(results[2], key = lambda j: j[1][i])[0:num]
    else:
        if sort_by == "alphabet":
            words_sorted = sorted(results[2], key = lambda j: j[0], reverse = True)[0:num]
        else:
            words_sorted = sorted(results[2], key = lambda j: j[1][i], reverse = True)[0:num]

    return render_template("index.html", results = results, word_distribution = word_distribution, words_sorted = words_sorted)


@app.route("/show_saved")
@login_required
def show_saved():
    """Show saved text analysis results"""
    global results, word_distribution
    # Get text_id
    results = []
    text_id = request.args["text_id"]
    # Get text analysis results from database
    a = db.execute("SELECT * FROM statistics WHERE text_id = ?", text_id)
    results.append(list(a[0].items())[1:])
    b = db.execute("SELECT * FROM readability WHERE text_id = ?", text_id)
    b1 = list(b[0].items())
    results.append([(b1[j][0], (b1[j][1], b1[j+1][1])) for j in range(2, len(b1), 2)])
    c = db.execute("SELECT * FROM words WHERE text_id = ?", text_id)
    results.append(json.loads(c[0]["words"]))
    summary = (db.execute("SELECT Summary FROM readability WHERE text_id = ?", text_id))[0]["Summary"]
    results.append(summary)
    # Get words distribution
    word_distribution = distribute_words(results[2])
    return render_template("index.html", results = results, word_distribution = word_distribution)

@app.route("/delete")
@login_required
def delete():
    """Delete text from database"""
    # Get text_id
    text_id = request.args["text_id"]
    # Delete records
    db.execute("DELETE FROM readability WHERE text_id = ?", text_id)
    db.execute("DELETE FROM statistics WHERE text_id = ?", text_id)
    db.execute("DELETE FROM texts WHERE text_id = ?", text_id)
    return redirect("/texts")