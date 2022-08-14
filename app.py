import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Initialize symbols list allowing to get multiple quotes
symbols = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Check shares available
    stock = db.execute("SELECT symbol, SUM(shares) FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    # Make portfolio
    portfolio = []
    subtotal = 0
    for i in stock:
        # Get current quotes for available shares
        get_quote = lookup(i["symbol"])
        # Make portfolio of shares
        # Exluding entries with zero sum of shares
        if i["SUM(shares)"] == 0:
            continue
        get_quote["shares"] = i["SUM(shares)"]
        get_quote["total"] = get_quote["price"] * get_quote["shares"]
        # Calculate subtotal as a running sum
        subtotal += get_quote["total"]
        get_quote["total"] = usd(get_quote["total"])
        get_quote["price"] = usd(get_quote["price"])
        portfolio.append(get_quote)
    # Check cash available
    cash = (db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"]))
    # Make total
    total = usd(cash[0]["cash"] + subtotal)
    # Show portfolio
    return render_template("index.html", portfolio = portfolio, cash = usd(cash[0]["cash"]), total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        # Get quote
        get_quote = lookup(symbol)
        # Ensure symbol was valid
        if not get_quote:
            return apology("invalid symbol", 400)
        # Ensure number of shares was submitted
        shares = request.form.get("shares")
        if not shares:
            return apology("must provide number of shares", 400)
        # Ensure number of shares was valid:
        if not re.fullmatch(r'[1-9]+\d*', shares):
            return apology("invalid number", 400)
        shares = int(shares)
        # Calculate the cost of shares
        cost = get_quote["price"] * shares
        # Check if user has enough money
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if cash[0]["cash"] < cost:
            return apology("not enough money", 400)
        # Create table "transactions" if it doesn't exist
        # db.execute("CREATE TABLE IF NOT EXISTS transactions (tr_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price FLOAT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        # Record the purchase
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], get_quote["symbol"], shares, get_quote["price"])
        # Update cash in "users" table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash[0]["cash"] - cost, session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    entries = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    for i in entries:
        # Get current quote
        get_quote = lookup(i["symbol"])
        # Find delta
        i["delta"] = get_quote["price"] - i["price"]
        if i["delta"] > 0:
            i["status"] ="pos"
            i["delta"] = "\u2191 " + usd(i["delta"])
        elif i["delta"] < 0:
            i["status"] = "neg"
            i["delta"] ="\u2193 " + usd(abs(i["delta"]))
        else:
            i["status"] = "zero"
            i["delta"] = i["delta"]

        i["price"] = usd(i["price"])
    return render_template("history.html", entries = entries)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Get quote
        get_quote = lookup(symbol)
        # Ensure symbol was valid
        if not get_quote:
            return apology("invalid symbol", 400)
        # Add symbol of interest to the symbols list allowing to get multiple quotes
        symbols.append(get_quote["symbol"])
        # Initialize quotes list allowing to get multiple quotes
        quotes = []
        # Fill in the quotes list
        for i in symbols:
            get_quote = lookup(i)
            quotes.append(get_quote)
        # Show quotes list from last quote to first one
        quotes = quotes[::-1]
        return render_template("quoted.html", quotes = quotes)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # User reached route via POST (as by submitting a form via POST)
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        user = db.execute("SELECT username FROM users WHERE username = ?", username)
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)
        # Ensure username is unique
        elif user:
            return apology("such username already exists", 400)
        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)
        elif confirmation != password:
            return apology ("passwords do not match", 400)

        # Register user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Ensure symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol or symbol == "Select symbol":
            return apology("must provide symbol", 400)
        get_quote = lookup(symbol)
        # Check available number of shares
        stock = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = ? GROUP BY symbol", symbol)
        # Ensure number of shares was submitted
        shares = request.form.get("shares")
        if not shares:
            return apology("must provide number of shares", 400)
        # Ensure number of shares was valid:
        if not re.fullmatch(r'[1-9]+\d*', shares):
            return apology("invalid number", 400)
        shares = int(shares)
        # Ensure user has enough shares:
        if shares > stock[0]["SUM(shares)"]:
            return apology("it's more than available", 400)
        # Calculate the cost of shares
        cost = get_quote["price"] * shares
        # Record the sell
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], get_quote["symbol"], -shares, get_quote["price"])
        # Update cash in "users" table
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash[0]["cash"] + cost, session["user_id"])
        return redirect("/")
    else:
        # Check shares available
        symbols = db.execute("SELECT symbol, SUM(shares) FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) !=0", session["user_id"])
        return render_template("sell.html", symbols = symbols)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Add cash to user account"""
    if request.method == "POST":
        # Ensure deposit was submitted
        deposit = request.form.get("deposit")
        if not deposit:
            return apology("must provide deposit", 400)
        # Ensure deposit was valid:
        if not re.fullmatch(r'\d+\.*\d*', deposit):
            return apology("invalid number", 400)
        deposit = round(float(deposit), 2)
        # Check user's current cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        # Record deposit
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash[0]["cash"] + deposit, session["user_id"])
        return redirect("/")
    else:
        # Check user's current cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        return render_template("deposit.html", cash = usd(cash[0]["cash"]))
