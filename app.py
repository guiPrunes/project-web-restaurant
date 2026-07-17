from flask import Flask, render_template
from models.restaurante import Restaurante
from models.avaliacao import RestauranteAvaliacao

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

restaurante1 = Restaurante('Verona', 'Italiana')
print(restaurante1)

if __name__ == "__main__":
    app.run()


