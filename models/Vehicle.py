class Veiculo:
    _proximo_id = 1   

    def __init__(self, marca: str, modelo: str, ano: int, preco: float, quilometragem: int, anunciante=None):
        self._id = Veiculo._proximo_id
        Veiculo._proximo_id += 1

        self._marca = marca
        self._modelo = modelo
        self._ano = ano
        self._preco = preco
        self._quilometragem = quilometragem
        # cada veículo pode pertencer a um anunciante (ou None)
        self._anunciante = anunciante

    @property
    def id(self) -> int:
        return self._id

    @property
    def marca(self) -> str:
        return self._marca

    @marca.setter
    def marca(self, valor: str):
        self._marca = valor

    @property
    def modelo(self) -> str:
        return self._modelo

    @modelo.setter
    def modelo(self, valor: str):
        self._modelo = valor

    @property
    def ano(self) -> int:
        return self._ano

    @ano.setter
    def ano(self, valor: int):
        self._ano = valor

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float):
        self._preco = valor

    @property
    def quilometragem(self) -> int:
        return self._quilometragem

    @quilometragem.setter
    def quilometragem(self, valor: int):
        self._quilometragem = valor

    @property
    def anunciante(self):
        return self._anunciante

    @anunciante.setter
    def anunciante(self, valor):
        self._anunciante = valor

    def exibirInformacoes(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Marca: {self.marca}\n"
            f"Modelo: {self.modelo}\n"
            f"Ano: {self.ano}\n"
            f"Preço: R${self.preco:.2f}\n"
            f"Quilometragem: {self.quilometragem} km\n"
            f"Anunciante: {getattr(self.anunciante, 'nome', 'Nenhum')}"
        )
