from models.restaurante import Restaurante
from models.usuario import Usuario

# * Restaurantes adicionados para teste
restaurante1 = Restaurante('Verona', 'Italiana')
restaurante1.delivery('25-35', 0)

restaurante2 = Restaurante('Sabor Caseiro', 'Brasileira')
restaurante2.delivery('30-40', 5.0)

restaurante3 = Restaurante('Sushi House', 'Japonesa')
restaurante3.delivery('20-30', 0)

restaurante4 = Restaurante('Los Burguer', 'Hamburgueria')
restaurante4.delivery('25-35', 7.0)

lista_restaurantes = {
    restaurante1._nome : restaurante1,
    restaurante2._nome : restaurante2,
    restaurante3._nome : restaurante3,
    restaurante4._nome : restaurante4,
}

# * Categorias criadas para filtragem
categorias = ['Todos','Italiana', 'Brasileira', 'Japonesa', 'Hamburgueria']

# * Avaliações dadas para conferência de feature
restaurante1.avaliar('Thiago', 4.3, 'Muito bom, ótimo!')
restaurante1.avaliar('Maria', 4.8, 'Excelente comida!')
restaurante4.avaliar('João', 4.5, 'Ótimo atendimento!')
restaurante2.avaliar('Ana', 4.0, 'Comida caseira deliciosa!')
restaurante3.avaliar('Shay', 2, 'Comida ruim')

# * Usuários cadastrados para teste
admin = Usuario("administrador", "admin123")
usuario = Usuario("usuario", "usuario123")

usuarios_cadastrados = {
    admin._usuario : admin,
    usuario._usuario : usuario 
}
