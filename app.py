from flask import Flask, redirect, render_template, flash, url_for, session, request
from models.usuario import Usuario
from tests.ex_testes import restaurantes, categorias

usuarios_cadastrados = {}

admin = Usuario("administrador", "admin123")
usuario = Usuario("usuario", "usuario123")
usuarios_cadastrados[admin._usuario] = admin
usuarios_cadastrados[usuario._usuario] = usuario

app = Flask(__name__) # Inicia a aplicação com Flask
app.secret_key = "bsd534534634$!@#$!Fsdnjgsiobjfbfjkffsdgsdkospvs" # Define a secret_key para uso de sessões (c/ cookies)

@app.route("/") 
def index():
    """
    Renderiza a página inicial do site com a listagem de restaurantes disponíveis.
    
    Vefica via sessão se há um administrador logado, e permite a filtragem de restaurantes por categoria via query string.

    Query Params:
        categoria (str, optional): Nome da categoria selecionada para filtragem dos restaurantes, caso ausente ou igual a todos, exibe todos os restaurantes disponíveis.

    Returns:
        Response: Template 'home.html' renderizado com context:
            - restaurantes (list): Lista de restaurantes cadastrados com ou sem filtro.
            - categorias (list): Lista de categorias cadastradas.
            - categoria_selecionada (str): Categoria atualmente selecionada.
            - usuario_logado (str | None): Nome do usuário logado na sessão.
            - admin_logado (bool): True se o usuário logado for um administrador. False caso contrário.
    """

    filtro_restaurantes = []

    admin_logado = False 
    usuario_logado = session.get('usuario_logado') # Retorna o nome do usuário caso encontre (True), caso contrário retorna None (False).
    if usuario_logado == "administrador": # Caso usuário logado seja o administrador de teste
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
    """
    Renderiza a página de log-in com formulário para preenchimento.

    Returns:
        Response: Template 'login.html'
    """

    return render_template('auth/login.html')

@app.route("/login/auth", methods=['GET', 'POST'])
def autenticar_login():
    """
    Autentica o acesso de um usuário para log-in.
   
    GET: Retorna à página de log-in (acesso à página pela URL não é permitido).  
    POST: Recebe os dados do formulário de log-in como usuário e senha, valida com a base de usuários cadastrados. Caso sucesso, efetua log-in.

    Form Data (POST):
        usuário (str): Nome de usuário, min. 6 caracteres, sem especiais.
        senha (str): Senha de usuário, min. 6 caracteres.

    Returns:
        Response: Redirect para 'index' com flash de sucesso, se autenticado.
        Response: Redirect para 'login' com flash de erro caso usuário esteja incorreto ou não exista, ou senha seja inválida/incorreta.

    Session:
        usuario_logado (str): Definido com o nome do usuário autenticado.
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
    """
    Renderiza a página de sign-in com formulário para preenchimento.
    
    Returns:
        Response: Template 'sigin.html'
    """
    return render_template("auth/signin.html")

@app.route("/signin/auth", methods=['GET', 'POST'])
def autenticar_signin():
    """
    Processa o cadastro de um novo usuário.
   
    GET: Retorna à página de sign-in (acesso à página pela URL não é permitido).  
    POST: Recebe usuario e senha do formulário e valida se o usuário já existe na base de usuários. Caso não exista, tenta criar uma nova instância da classe Usuário, caso sucesso, cadastra um novo usuário. Caso contrário, retorna um flash de erro para a página de cadastro.

    Form Data (POST):
        usuário (str): nome de usuário, min. 6 caracteres, sem especiais.
        senha (str): senha de usuário, min. 6 caracteres.

    Returns:
        Response: Redirect para 'login' com flash de sucesso, caso usuário for cadastrado.
        Response: Redirect para 'signin' com flash de erro caso usuário já exista ou não respeite as normas de criação da classe Usuário.
    """    

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
    """
    Remove o usuário logado.
    
    Limpa a sessão removendo o usuário logado e redireciona para página principal.
    """
    session.clear()
    return redirect(url_for("index"))

@app.route("/restaurante")
def restaurante():
    return render_template("main/restaurant.html")

if __name__ == "__main__":
    app.run(debug=True)


