from flask import Flask, redirect, render_template, flash, url_for, session, request
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
normal = Usuario("usuario1", "usuario123")
usuarios_cadastrados[admin._usuario] = admin
usuarios_cadastrados[normal._usuario] = normal

app = Flask(__name__) # Inicia a aplicação com Flask
app.secret_key = "bsd534534634$!@#$!Fsdnjgsiobjfbfjkffsdgsdkospvs" # Define a secret_key para uso de sessões (c/ cookies)

@app.route("/") 
def index():
    """
    
    """
    admin_logado = False
    usuario_logado = session.get('usuario_logado')
    if usuario_logado == "useradmin":
        admin_logado = True

    categoria_selecionada = request.args.get('categoria') # ?categoria={resultado}
    filtro_restaurantes.clear() # Limpa o filtro quando recarregada a página
    if not categoria_selecionada or categoria_selecionada == "Todos":
        return render_template('main/home.html', 
                               restaurantes=restaurantes, 
                               categorias=categorias, 
                               categoria_selecionada=categoria_selecionada, 
                               usuario_logado=usuario_logado, 
                               admin_logado=admin_logado
                               )
    else:
        for restaurante in restaurantes:
            if restaurante._categoria == categoria_selecionada:
                filtro_restaurantes.append(restaurante)
        return render_template('main/home.html', 
                               restaurantes=filtro_restaurantes, 
                               categorias=categorias, 
                               categoria_selecionada=categoria_selecionada, 
                               usuario_logado=usuario_logado, 
                               admin_logado=admin_logado
                               ) 

@app.route("/login")
def login():
    return render_template('auth/login.html')

@app.route("/login/auth", methods=['GET', 'POST'])
def autenticar_login():
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

    if usuario_encontrado and usuario_encontrado.verificar_senha(form_senha): 
        # Caso usuário esteja no dicionário "usuarios_cadastrados" e,
        # Caso o verificar_senha() retorne True.
        session['usuario_logado'] = usuario_encontrado._usuario
        flash(f"Login realizado com sucesso!", "sucesso")
        return redirect(url_for('index'))
    
    if not usuario_encontrado: 
        flash("Usuário incorreto ou não existe!", "erro")
    else:
        flash("Senha incorreta, tente novamente...", "erro")
    return redirect(url_for('login'))

@app.route("/signin")
def signin():
    return render_template("auth/signin.html")

@app.route("/signin/auth", methods=['GET', 'POST'])
def autenticar_signin():
    if request.method == "GET":
        return redirect(url_for('signin'))
    
    form_usuario = request.form['usuario'].strip().lower()
    form_senha = request.form['senha'].strip()

    usuario_existe = usuarios_cadastrados.get(form_usuario)

    if usuario_existe:
        flash("Este usuário já existe, tente outro nome de usuário...", "erro")
        return redirect(url_for("signin"))

    try:
        novo_usuario = Usuario(form_usuario, form_senha)
        usuarios_cadastrados[novo_usuario._usuario] = novo_usuario
        flash("Usuário cadastrado com sucesso! Faça log-in para continuar...", "sucesso")
        return redirect(url_for("login"))
    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for('signin'))
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/restaurante")
def restaurante():
    return render_template("/restaurant_page.html")


if __name__ == "__main__":
    app.run(debug=True)


