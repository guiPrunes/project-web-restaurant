from models.avaliacao import Avaliacao
from models.delivery import Delivery

class Restaurante:
    def __init__(self, nome:str, categoria:str):
        self._nome = nome
        self._categoria = categoria
        self.__lista_avaliacoes = []
        self._delivery = None

    def delivery(self, tempo_entrega:str, taxa_entrega:float):
        self._delivery = Delivery(tempo_entrega, taxa_entrega)

    def avaliar(self, cliente, nota, comentario): # restaurante.avaliar('Thiago', 4.3, 'Muito bom, ótimo!')
        avaliacao_recebida = Avaliacao(cliente, nota, comentario)
        self.__lista_avaliacoes.append(avaliacao_recebida)

    @property
    def media_avaliacoes(self):
        if len(self.__lista_avaliacoes) == 0:
            return 0
        else:
            soma = 0
            for avaliacao in self.__lista_avaliacoes:
                soma += avaliacao.nota
                media = soma / len(self.__lista_avaliacoes)
            return round(media, 2)
    
    @property
    def qntd_estrelas(self):
        media = self.media_avaliacoes
        estrelas = '★' * int(media) + '☆' * (5 - int(media))
        return estrelas

    @property
    def total_avaliacoes(self):
        return len(self.__lista_avaliacoes)
    
    def __str__(self):
        return f"""Nome: {self._nome}\nCategoria: {self._categoria}"""


