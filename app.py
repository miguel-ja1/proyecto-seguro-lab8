# app.py
from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# VULNERABILIDAD 1: Clave secreta hardcodeada (B105)
SECRET_KEY = "clave_secreta_123"

# VULNERABILIDAD 2: Uso de md5 débil (B324)
import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABILIDAD 3: SQL Injection (B608)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        # SQL sin parámetros seguros
        query = f"SELECT * FROM usuarios WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return "Login exitoso"
        return "Login fallido"
    return '''
        <form method="POST">
            Usuario: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Ingresar">
        </form>
    '''

# VULNERABILIDAD 4: debug=True en producción (B201)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")