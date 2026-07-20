from flask import Flask, render_template, request
from models.restaurante import Restaurante
from models.avaliacao import Avaliacao

# 
restaurante1 = Restaurante('Verona', 'Italiana')
restaurante1.delivery('25-35', 0)

restaurante2 = Restaurante('Sabor Caseiro', 'Brasileira')
restaurante2.delivery('30-40', 5.0)

restaurante3 = Restaurante('Sushi House', 'Japonesa')
restaurante3.delivery('20-30', 0)

restaurante4 = Restaurante('Los Burguer', 'Hamburgueria')
restaurante4.delivery('25-35', 7.0)

restaurante1.avaliar('Thiago', 4.3, 'Muito bom, ótimo!')
restaurante1.avaliar('Maria', 4.8, 'Excelente comida!')
restaurante1.avaliar('João', 4.5, 'Ótimo atendimento!')
restaurante2.avaliar('Ana', 4.0, 'Comida caseira deliciosa!')
restaurante2.avaliar('Carlos', 3.8, 'Bom, mas poderia melhorar.')

categorias = ['Todos','Italiana', 'Brasileira', 'Japonesa', 'Hamburgueria']

restaurantes = [restaurante1, restaurante2, restaurante3, restaurante4]
# 

app = Flask(__name__)

@app.route("/")
def index():
    categoria_selecionada = request.args.get('categoria')
    return render_template('home.html', restaurantes=restaurantes, categorias=categorias, categoria_selecionada=categoria_selecionada)

if __name__ == "__main__":
    app.run(debug=True)


