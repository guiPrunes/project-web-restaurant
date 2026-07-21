from flask import Flask, redirect, render_template, flash, url_for, request
from models.restaurante import Restaurante
from models.avaliacao import Avaliacao
from models.usuario import Usuario

# 
restaurante1 = Restaurante('Verona', 'Italiana')
restaurante1.delivery('25-35', 0)

restaurante2 = Restaurante('Sabor Caseiro', 'Brasileira')
restaurante2.delivery('30-40', 5.0)

restaurante3 = Restaurante('Sushi House', 'Japonesa')
restaurante3.delivery('20-30', 0)

restaurante4 = Restaurante('Los Burguer', 'Hamburgueria')
restaurante4.delivery('25-35', 7.0)

restaurante5 = Restaurante('Skibidi Toilet Simulator', 'Italiana')

restaurante1.avaliar('Thiago', 4.3, 'Muito bom, ótimo!')
restaurante1.avaliar('Maria', 4.8, 'Excelente comida!')
restaurante4.avaliar('João', 4.5, 'Ótimo atendimento!')
restaurante2.avaliar('Ana', 4.0, 'Comida caseira deliciosa!')
restaurante5.avaliar('Carlos', 3.8, 'Bom, mas poderia melhorar.')

# 
categorias = ['Todos','Italiana', 'Brasileira', 'Japonesa', 'Hamburgueria']
restaurantes = [restaurante1, restaurante2, restaurante3, restaurante4, restaurante5]
filtro_restaurantes = []
usuarios_cadastrados = {}

admin = Usuario("useradmin", "admin123")
usuarios_cadastrados[admin._usuario] = admin

app = Flask(__name__) # Inicia a aplicação com Flask
app.secret_key = "bsd534534634$!@#$!Fsdnjgsiobjfbfjkffsdgsdkospvs" # Define a secret_key para uso de sessões (c/ cookies)

@app.route("/") 
def index():
    """
    
    """
    categoria_selecionada = request.args.get('categoria')
    filtro_restaurantes.clear()
    if not categoria_selecionada or categoria_selecionada == "Todos":
        return render_template('home.html', restaurantes=restaurantes, categorias=categorias, categoria_selecionada=categoria_selecionada)
    else:
        for restaurante in restaurantes:
            if restaurante._categoria == categoria_selecionada:
                filtro_restaurantes.append(restaurante)
        return render_template('home.html', restaurantes=filtro_restaurantes, categorias=categorias, categoria_selecionada=categoria_selecionada) 

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/auth", methods=['GET', 'POST'])
def autenticar():
    """
    Autentica um usuário existente
   
    GET: retorna à página de log-in.  
    POST: recebe os dados do formulário de log-in como usuário e senha, valida-os e 

    Form data esperado:
        usuário (str): nome de usuário, min. 6 caracteres, sem especiais.
        senha (str): senha de usuário, min. 6 caracteres.

    Returns:
        Redirect para 'login' caso usuário já exista ou forem inválidos. Redirect para 'index' caso sucesso.
    """

    if request.method == "GET": # Caso seja acessado pela URL
        return redirect(url_for("login")) # Redireciona para a página de log-in
    
    # Extraindo dados do formulário de log-in
    form_usuario = request.form['usuario'].strip().lower() # Recebe o usuário (name="usuario")
    form_senha = request.form['senha'].strip() # Recebe a senha do usuário do (name="senha")

    # Busca por form_usuario no usuarios_cadastrados, retorna o objeto Usuário caso encontrar
    # Caso não encontrar, retorna None
    usuario_encontrado = usuarios_cadastrados.get(form_usuario)
    # Ex: form_usuario = "coordenador1"
    # usuarios_cadastrados = {"coordenador1" : <class Usuário> }
    # usuario_encontrado = <class Usuário> | Se não encontrar: usuario_encontrado = None

    if usuario_encontrado and usuario_encontrado.verificar_senha(form_senha): 
        # Caso usuário esteja no dicionário "usuarios_cadastrados" e,
        # Caso o verificar_senha() retorne True.
        flash("Login realizado com sucesso!", "sucesso")
        return redirect(url_for('index'))
    
    if not usuario_encontrado: 
        flash("Usuário incorreto ou não existe!", "erro")
    else:
        flash("Senha incorreta, tente novamente...", "erro")
    return redirect(url_for('login'))

# @app.route("/cadastro")
# def cadastrar():
#     try:
#         usuario_cadastrado = Usuario(usuario_form, senha_form)
#     except ValueError as erro: 
#         flash(str(erro), "erro")
#         return redirect(url_for("login")) 
#     usuarios_cadastrados[usuario_cadastrado._usuario] = usuario_cadastrado

if __name__ == "__main__":
    app.run(debug=True)


