import os
from flask import Flask, render_template

app = Flask(__name__)

# RUTA PRINCIPAL (Inicio)
@app.route('/')
def home():
    return render_template('index.html')

# RUTA DE VIDEOS
@app.route('/videos')
def videos():
    # Renderizamos la misma página pero el JS se encargará de bajar a la sección
    return render_template('index.html')

# RUTA DE COMUNIDAD / SOCIALS
@app.route('/comunidad')
def comunidad():
    return render_template('index.html')

# CONFIGURACIÓN PARA DESPLIEGUE REAL (RENDER)
if __name__ == '__main__':
    # Render asigna dinámicamente un puerto a través de la variable de entorno PORT
    # Si no existe (como en tu PC), usará el 704 por defecto
    port = int(os.environ.get("PORT", 704))
    
    # host='0.0.0.0' es obligatorio para que el servidor sea accesible desde afuera
    app.run(host='0.0.0.0', port=port)
