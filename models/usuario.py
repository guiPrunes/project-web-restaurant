from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    """
    Representa um usuário cadastrado.

    O usuário possui nome e senha correspondentes, com validação delegada aos métodos validar_usuario e validar_senha.

    Attributes:
        _usuario (str): Nome de usuário, sem espaços nas extremidades.
        _senha (str): Hash da senha, gerado via werkzeug.
    """
    def __init__(self, usuario:str, senha:str):
        """
        Inicializa um usuário .

        Args:
            usuario (str): Nome do usuário cadastrado.
            senha (str): Senha vinculada ao nome do usuario.
        """
        self._usuario = usuario.strip()
        senha = senha.strip()

        self.validar_usuario()
        self.validar_senha(senha)

        self._senha = generate_password_hash(senha)

    def validar_usuario(self):
        """
        Valida a string armazenada em self_usuario.

        Raises:
            ValueError: Se o usuário estiver vazio, tiver menos que 6 caracteres ou contiver caracteres especiais.
        """
        if self._usuario == "":
            raise ValueError("Usuário não pode estar vazio")
        if len(self._usuario) < 6:
            raise ValueError("Usuário deve ter no mínimo 6 caracteres")
        if any(c in "!@#$%^&*()_+=-[]{}|;:'\",.<>?/\\`~" for c in self._usuario):
            raise ValueError("Usuário não pode conter caracteres especiais")

    def validar_senha(self, senha:str):
        """
        Valida a string armazenada em senha antes de gerar o hash.

        Args:
            senha (str): Senha em texto ser validada.

        Raises:
            ValueError: Se a senha estiver vazia ou tiver menos que 6 caracteres.
        """
        if senha == "":
            raise ValueError("Senha não pode estar vazio")
        if len(senha) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
        
    def verificar_senha(self, senha:str):
        """
        Compara a senha informada com o hash armazenado.

        Args:
            senha (str) : Senha em texto para comparação.

        Returns:
            bool: True, se a hash e a senha correspoderem. False caso o contrário.
        """
        return check_password_hash(self._senha, senha)
        

