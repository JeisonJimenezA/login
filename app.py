import pyodbc
from flask import Flask, render_template, redirect, request, url_for, session
from flask_cors import  CORS
import secrets

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)


def conectar_bd():
    server = "(localdb)\\Lucy"
    db_name = "login_user"
    user = "lucy"
    password = "123456"
    try:
        conexion = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db_name};UID={user};PWD={password}"
        )
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje_error = None

    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["password"]

        cur = conectar_bd().cursor()
        sql = f"SELECT * FROM usuarios WHERE email=? AND contraseña=?;"
        rows = cur.execute(sql, (email, contrasena)).fetchall()

        if len(rows) > 0:
            session["usuario"] = {"id": rows[0][0], "nombre": rows[0][1]}
            return redirect(url_for("chat"))
        else:
            mensaje_error = "Usuario o Contraseña incorrectos."

    return render_template("login.html", mensaje_error=mensaje_error)


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))


@app.route("/layout", methods=["GET", "POST"])
def layout():
    session.clear()
    return render_template("home.html")


@app.route("/chat")
def chat():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(debug=True)
