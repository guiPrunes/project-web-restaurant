from avaliacao import Avaliacao

class Restaurante:
    def __init__(self, nome:str, categoria:str):
        self._nome = nome
        self._categoria = categoria
        self.__lista_avaliacoes = []

    def avaliar(self, cliente, nota, comentario): # restaurante.avaliar('Thiago', 4.3, 'Muito bom, ótimo!')
        avaliacao_recebida = Avaliacao(cliente, nota, comentario) # 
        self.__lista_avaliacoes.append(avaliacao_recebida)

    def __str__(self):
        return f"""Nome: {self._nome}\nCategoria: {self._categoria}"""
    
restauranteteste = Restaurante('Verona', 'Italiana')
restauranteteste.avaliar('Thiago', 4, 'Muito bom, ótimo!')
print(restauranteteste)

