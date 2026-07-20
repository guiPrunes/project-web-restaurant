class Delivery:
    def __init__(self, tempo_entrega:str, taxa_entrega:float):
        self._tempo_entrega = f"{tempo_entrega} min"
        self._taxa_entrega = round(taxa_entrega, 2)
        if self._taxa_entrega == 0:
            self._taxa_entrega = 'Grátis'
        else:
            self._taxa_entrega = str(f"R$ {self._taxa_entrega:.2f}".replace('.', ','))
