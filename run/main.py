import os

serviceAccount = r'focused-mote-361402-ac24139c4873.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import base64
import qrcode
from utils_gcp import save_html, get_html, save_bigquery
from matplotlib.pyplot import get
from datetime import datetime


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        text = request.form["data"]

        # Crear QR
        path = f"{request.base_url}/img?name={text}"
        print(path)
        img = qrcode.make(path)
        qrPath = os.path.join("static", "some_file.png")
        img.save(qrPath)

        with open(qrPath, 'rb') as fd:
            image_as_base64_html = base64.encodebytes(fd.read()).decode()

        # Obtener imagen
        imagen = request.files["img"]
        imagen.save('im-received.png')
        with open('im-received.png', 'rb') as fd:
            imageUser = base64.encodebytes(fd.read()).decode()
        print(imagen)

        #   Guardar html con texto/imagen en gcp
        save_html(text, imageUser)

        # Registrar entrada
        fila = [
            {
                "ip":str(request.remote_addr),
                "nombre":str(text),
                "imagen":imageUser,
                "fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        save_bigquery("focused-mote-361402.registro_app_dataset.imagenes_registro",fila)
        print("Ok")
        return render_template("qrcode.html", image_as_base64_html=image_as_base64_html)
    return render_template("index.html")


@app.route('/img')
def img():
    imgPath = request.args.get('name')
    print(imgPath)
    html = get_html(imgPath)

    # Registrar entrada
    fila = [
            {
                "ip":str(request.remote_addr),
                "nombre":str(imgPath),
                "fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    save_bigquery("focused-mote-361402.registro_app_dataset.vistas_registro",fila)
    return render_template("imagen.html", image_as_base64_html=html)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('port', 8080)))
