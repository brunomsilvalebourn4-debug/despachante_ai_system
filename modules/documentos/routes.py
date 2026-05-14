import os
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import sqlite3

documentos_bp = Blueprint('documentos', __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def salvar_db(processo_id, filename, path, tipo):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documentos (processo_id, nome_arquivo, caminho, tipo)
        VALUES (?, ?, ?, ?)
    """, (processo_id, filename, path, tipo))

    conn.commit()
    conn.close()


@documentos_bp.route("/processo/<int:processo_id>/upload", methods=["GET", "POST"])
def upload(processo_id):

    if request.method == "POST":

        file = request.files["file"]
        tipo = request.form.get("tipo")

        if file:

            filename = secure_filename(file.filename)

            pasta = os.path.join(UPLOAD_FOLDER, str(processo_id))
            os.makedirs(pasta, exist_ok=True)

            caminho = os.path.join(pasta, filename)
            file.save(caminho)

            salvar_db(processo_id, filename, caminho, tipo)

            return redirect(f"/processo/{processo_id}/upload")

    return render_template("upload.html", processo_id=processo_id)