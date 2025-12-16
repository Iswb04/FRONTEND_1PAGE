from flask import Flask, request, redirect, render_template, session
import sqlite3
import re

REGEX_SENHA = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#._-])[A-Za-z\d@$!%*?&#._-]{8,}$"

app = Flask(__name__)
app.secret_key = "secret-key"

DB_PATH = "login.db"


def conectar():
    return sqlite3.connect(DB_PATH)


# ---------- PAGE 1 ----------
@app.route("/", methods=["GET", "POST"])
def page_into1():
    if request.method == "POST":
        email = request.form["email"]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email=?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return redirect(f"/senha?email={email}")
        else:
            return redirect(f"/cadastro?email={email}")

    return render_template("1page.html")


# ---------- PAGE 2 ----------
@app.route("/senha", methods=["GET", "POST"])
def page_into2():
    email = request.args.get("email")

    if request.method == "POST":
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE email=? AND senha=?",
            (email, senha)
        )
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session["logado"] = True
            session["email"] = email
            return redirect("/full")

        # ❌ erro → mesma página
        return render_template("2page.html", email=email, erro=True), 401

    return render_template("2page.html", email=email)


# ---------- PAGE 3 ----------
@app.route("/cadastro", methods=["GET", "POST"])
def page_into3():
    email = request.args.get("email")

    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        if not re.match(REGEX_SENHA, senha):
            return render_template("3page.html", email=email, erro=True), 400

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )
        conn.commit()
        conn.close()

        session["logado"] = True
        session["email"] = email
        return redirect("/full")

    return render_template("3page.html", email=email)


# ---------- FULL (PROTEGIDA) ----------
@app.route("/full")
def full_page():
    if not session.get("logado"):
        return redirect("/")
    return render_template("fpage.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)





# http://127.0.0.1:5000/